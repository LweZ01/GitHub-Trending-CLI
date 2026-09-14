# tests/test_config.py
import pytest

from config import DurationOption, DURATION_TO_DAYS, validate_duration
from exceptions import InvalidDurationError


@pytest.mark.parametrize("duration,expected_days", [
    ("day", 1),
    ("week", 7),
    ("month", 30),
    ("year", 365),
])
def test_duration_to_days_mapping(duration, expected_days):
    option = validate_duration(duration)
    assert DURATION_TO_DAYS[option] == expected_days


def test_validate_duration_returns_duration_option():
    result = validate_duration("week")
    assert result == DurationOption.WEEK


def test_validate_duration_raises_on_invalid_value():
    with pytest.raises(InvalidDurationError) as exc_info:
        validate_duration("century")

    assert exc_info.value.duration == "century"
    assert "day" in exc_info.value.valid_options


def test_all_duration_options_have_a_day_mapping():
    for option in DurationOption:
        assert option in DURATION_TO_DAYS