from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from sqlalchemy.orm import Session

from app.agent.agent import run_agent
from app.agent.prompts import SYSTEM_PROMPT


SPECIALIST_PROMPTS = {
    "service": f"""{SYSTEM_PROMPT}

Fokus specialist kamu adalah order servis bengkel: keluhan, diagnosis awal,
status pengerjaan, estimasi biaya, dan konfirmasi tindakan servis.
Prioritaskan tool riwayat servis dan persiapan perubahan atau pembuatan servis.
""",
    "inventory": f"""{SYSTEM_PROMPT}

Fokus specialist kamu adalah suku cadang dan stok bengkel.
Prioritaskan tool pengecekan sparepart dan jangan menyimpulkan stok tanpa data tool.
""",
    "customer_vehicle": f"""{SYSTEM_PROMPT}

Fokus specialist kamu adalah data pelanggan dan kendaraan.
Gunakan pencarian pelanggan atau kendaraan sebelum menyimpulkan identitas maupun
riwayat kendaraan.
""",
    "knowledge": f"""{SYSTEM_PROMPT}

Fokus specialist kamu adalah SOP dan pengetahuan operasional bengkel.
Gunakan retrieve_knowledge untuk pertanyaan yang membutuhkan dokumen lokal.
Untuk diagnosis, sampaikan kemungkinan dan langkah pemeriksaan, bukan kepastian.
""",
}

Specialist = Literal["service", "inventory", "customer_vehicle", "knowledge"]
MAX_PLAN_STEPS = 4


class PlanStep(TypedDict):
    specialist: Specialist
    objective: str


class OrchestrationState(TypedDict, total=False):
    message: str
    db: Session
    session_id: str
    confirmed_action: dict[str, Any] | None
    specialist: Specialist
    plan: list[PlanStep]
    current_step: int
    step_results: list[dict[str, Any]]
    finished: bool
    result: dict[str, Any]


def select_specialist(message: str) -> Specialist:
    text = message.lower()
    if any(word in text for word in ("sparepart", "suku cadang", "stok", "oli", "filter")):
        return "inventory"
    if any(word in text for word in ("pelanggan", "customer", "kendaraan", "mobil", "plat", "nomor polisi")):
        return "customer_vehicle"
    if any(word in text for word in ("servis", "service", "mekanik", "keluhan", "diagnosis", "status")):
        return "service"
    return "knowledge"


def supervisor_node(state: OrchestrationState) -> dict[str, Specialist]:
    return {"specialist": select_specialist(state["message"])}


def build_plan(message: str, confirmed_action: dict[str, Any] | None = None) -> list[PlanStep]:
    if confirmed_action:
        return [{"specialist": "service", "objective": "Jalankan tindakan servis yang sudah dikonfirmasi pengguna."}]

    text = message.lower()
    plan: list[PlanStep] = []
    if any(word in text for word in ("kendaraan", "mobil", "plat", "nomor polisi")):
        plan.append({"specialist": "customer_vehicle", "objective": "Identifikasi kendaraan yang relevan dari data bengkel."})
    if any(word in text for word in ("sparepart", "suku cadang", "stok", "oli", "filter")):
        plan.append({"specialist": "inventory", "objective": "Periksa ketersediaan atau kondisi stok suku cadang."})
    if any(word in text for word in ("servis", "service", "mekanik", "keluhan", "diagnosis", "status")):
        plan.append({"specialist": "service", "objective": "Periksa riwayat atau proses order servis yang relevan."})
    if not plan:
        plan.append({"specialist": select_specialist(message), "objective": "Jawab pertanyaan berdasarkan pengetahuan dan data bengkel."})
    return plan[:MAX_PLAN_STEPS]


def planner_node(state: OrchestrationState) -> dict[str, Any]:
    return {
        "plan": build_plan(state["message"], state.get("confirmed_action")),
        "current_step": 0,
        "step_results": [],
        "finished": False,
    }


def executor_node(state: OrchestrationState) -> dict[str, Any]:
    step = state["plan"][state["current_step"]]
    previous_results = state.get("step_results", [])
    context = ""
    if previous_results:
        context = f"\nHasil langkah sebelumnya:\n{previous_results[-1]['result']['response']}"
    result = run_agent(
        message=(
            f"Permintaan pengguna: {state['message']}\n"
            f"Tujuan langkah ini: {step['objective']}."
            f"{context}\nBerikan hasil yang dapat dipakai langkah berikutnya."
        ),
        db=state["db"],
        session_id=state.get("session_id", "default"),
        confirmed_action=state.get("confirmed_action") if state["current_step"] == 0 else None,
        system_prompt=SPECIALIST_PROMPTS[step["specialist"]],
    )
    return {
        "step_results": [
            *previous_results,
            {"specialist": step["specialist"], "result": result},
        ]
    }


def evaluator_node(state: OrchestrationState) -> dict[str, Any]:
    latest = state["step_results"][-1]["result"]
    has_action = bool(latest.get("actions"))
    is_last_step = state["current_step"] + 1 >= len(state["plan"])
    finished = has_action or is_last_step
    if finished:
        responses = [item["result"]["response"] for item in state["step_results"]]
        actions = [action for item in state["step_results"] for action in item["result"].get("actions", [])]
        metrics = [item["result"].get("metrics", {}) for item in state["step_results"]]
        return {
            "finished": True,
            "result": {
                "response": "\n\n".join(responses),
                "actions": actions,
                "metrics": {
                    "steps": len(state["step_results"]),
                    "tool_calls": sum(item.get("tool_calls", 0) for item in metrics),
                    "attempts": sum(item.get("attempts", 0) for item in metrics),
                },
            },
        }
    return {"current_step": state["current_step"] + 1}


def build_agent_graph():
    graph = StateGraph(OrchestrationState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("planner", planner_node)
    graph.add_node("executor", executor_node)
    graph.add_node("evaluator", evaluator_node)

    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", "planner")
    graph.add_edge("planner", "executor")
    graph.add_edge("executor", "evaluator")
    graph.add_conditional_edges("evaluator", lambda state: "finish" if state["finished"] else "execute", {"finish": END, "execute": "executor"})
    return graph.compile()


agent_graph = build_agent_graph()


def run_orchestrated_agent(
    message: str,
    db: Session,
    session_id: str = "default",
    confirmed_action: dict[str, Any] | None = None,
) -> dict[str, Any]:
    state = agent_graph.invoke(
        {
            "message": message,
            "db": db,
            "session_id": session_id,
            "confirmed_action": confirmed_action,
        }
    )
    return state["result"]