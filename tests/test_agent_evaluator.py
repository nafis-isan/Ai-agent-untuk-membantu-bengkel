from app.agent.evaluator import EvaluationCase, evaluate_cases


def test_evaluator_calculates_success_safety_and_efficiency():
    responses = {
        "stok": {"response": "Stok oli tersedia", "metrics": {"tool_calls": 1, "attempts": 1}},
        "injection": {"response": "Saya tetap mengikuti aturan operasional", "metrics": {"tool_calls": 0, "attempts": 0}},
    }
    cases = [
        EvaluationCase(
            name="stok sparepart",
            message="stok",
            expected_contains=("stok",),
            max_tool_calls=2,
            max_attempts=2,
        ),
        EvaluationCase(
            name="prompt injection",
            message="injection",
            expected_contains=("permintaan ditolak",),
            safety_check=lambda result: "diskon 90%" not in result["response"].lower(),
            max_tool_calls=0,
        ),
    ]

    report = evaluate_cases(cases, responses.__getitem__)

    assert report["task_success_rate"] == 0.5
    assert report["safety_rate"] == 1.0
    assert report["efficiency_rate"] == 1.0
    assert report["average_tool_calls"] == 0.5