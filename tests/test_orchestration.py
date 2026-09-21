from app.agent import orchestration


def test_supervisor_routes_bengkel_requests():
    assert orchestration.select_specialist("Suku cadang dengan stok rendah") == "inventory"
    assert orchestration.select_specialist("Cari kendaraan dengan plat D 1234 ABC") == "customer_vehicle"
    assert orchestration.select_specialist("Ubah status servis menjadi selesai") == "service"
    assert orchestration.select_specialist("Apa SOP pemeriksaan rem?") == "knowledge"


def test_planner_creates_ordered_multi_step_plan():
    plan = orchestration.build_plan("Cek kendaraan B 1234 ABC dan stok oli untuk servis")

    assert [step["specialist"] for step in plan] == ["customer_vehicle", "inventory", "service"]


def test_graph_delegates_to_selected_specialist(monkeypatch):
    calls = []

    def fake_run_agent(**kwargs):
        calls.append(kwargs)
        return {"response": "ok", "actions": []}

    monkeypatch.setattr(orchestration, "run_agent", fake_run_agent)
    result = orchestration.run_orchestrated_agent(
        "Suku cadang dengan stok rendah",
        db=object(),
        session_id="test-session",
    )

    assert result == {
        "response": "ok",
        "actions": [],
        "metrics": {"steps": 1, "tool_calls": 0, "attempts": 0},
    }
    assert calls[0]["system_prompt"] == orchestration.SPECIALIST_PROMPTS["inventory"]