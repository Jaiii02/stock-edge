from app.services.recommendation import calculate_overall_confidence


def test_insufficient_component_confidence_is_reported():
    result = calculate_overall_confidence(
        {"confidence": 0.0},
        {"confidence": 40.0},
    )

    assert result["level"] == "Insufficient Data"
