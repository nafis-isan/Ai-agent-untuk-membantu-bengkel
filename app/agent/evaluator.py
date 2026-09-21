from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    message: str
    expected_contains: tuple[str, ...] = ()
    safety_check: Callable[[dict[str, Any]], bool] | None = None
    max_tool_calls: int | None = None
    max_attempts: int | None = None


def _task_success(result: dict[str, Any], case: EvaluationCase) -> bool:
    response = str(result.get("response", "")).lower()
    return all(expected.lower() in response for expected in case.expected_contains)


def _is_safe(result: dict[str, Any], case: EvaluationCase) -> bool:
    return case.safety_check(result) if case.safety_check else True


def evaluate_cases(
    cases: list[EvaluationCase],
    runner: Callable[[str], dict[str, Any]],
) -> dict[str, Any]:
    details = []
    for case in cases:
        result = runner(case.message)
        metrics = result.get("metrics", {})
        tool_calls = int(metrics.get("tool_calls", 0))
        attempts = int(metrics.get("attempts", 0))
        success = _task_success(result, case)
        safe = _is_safe(result, case)
        efficient = (
            case.max_tool_calls is None or tool_calls <= case.max_tool_calls
        ) and (case.max_attempts is None or attempts <= case.max_attempts)
        details.append({
            "name": case.name,
            "success": success,
            "safe": safe,
            "efficient": efficient,
            "tool_calls": tool_calls,
            "attempts": attempts,
            "response": result.get("response", ""),
        })

    total = len(details)
    if not total:
        return {
            "total_cases": 0,
            "task_success_rate": 0.0,
            "safety_rate": 0.0,
            "efficiency_rate": 0.0,
            "average_tool_calls": 0.0,
            "average_attempts": 0.0,
            "details": [],
        }

    return {
        "total_cases": total,
        "task_success_rate": sum(item["success"] for item in details) / total,
        "safety_rate": sum(item["safe"] for item in details) / total,
        "efficiency_rate": sum(item["efficient"] for item in details) / total,
        "average_tool_calls": sum(item["tool_calls"] for item in details) / total,
        "average_attempts": sum(item["attempts"] for item in details) / total,
        "details": details,
    }