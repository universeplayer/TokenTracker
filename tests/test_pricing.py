"""Tests for pricing estimation."""

from tokentracker.pricing import estimate_cost


def test_known_model():
    cost = estimate_cost("gpt-4o", input_tokens=1000, output_tokens=500)
    assert cost is not None
    # 1000 * 2.50/1M + 500 * 10.00/1M = 0.0025 + 0.005 = 0.0075
    assert abs(cost - 0.0075) < 0.0001


def test_unknown_model():
    cost = estimate_cost("some-random-model", input_tokens=1000, output_tokens=500)
    assert cost is None


def test_openrouter_prefix():
    cost = estimate_cost("openai/gpt-4o", input_tokens=1000, output_tokens=500)
    assert cost is not None
    assert cost > 0


def test_zero_tokens():
    cost = estimate_cost("gpt-4o", input_tokens=0, output_tokens=0)
    assert cost == 0.0
