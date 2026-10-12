import pytest
import pandas as pd

from analytics import (
    calculate_ts,
    calculate_per36,
    calculate_consistency,
    calculate_rolling_average
)

def test_calculate_ts():
    # Arrange: Create sample basketball statistics
    test_data = pd.DataFrame({
        "PTS": [20, 10],
        "FGA": [12, 8],
        "FTA": [4, 6]
    })

    # Act: Call our function
    result = calculate_ts(test_data)

    # Assert: Verify the calculated value
    assert result == pytest.approx(61.4754, abs=0.001)

def test_calculate_ts_zero_attempts():
    # Arrange: Create sample basketball statistics with zero attempts
    test_data = pd.DataFrame({
        "PTS": [0, 0],
        "FGA": [0, 0],
        "FTA": [0, 0]
    })

    # Act: Call our function
    result = calculate_ts(test_data)

    # Assert: Verify the calculated value is NaN
    assert pd.isna(result)


def test_calculate_per36():
    # Arrange: Create sample basketball statistics
    test_data = pd.DataFrame({
        "PTS": [20, 10],
        "MIN": [30, 20]
    })

    # Act: Call our function
    result = calculate_per36(test_data, "PTS")

    # Assert: Verify the calculated value
    assert result == pytest.approx(21.6, abs=0.001)

def test_calculate_per36_zero_minutes():
    # Arrange: Create sample basketball statistics with zero minutes
    test_data = pd.DataFrame({
        "PTS": [20, 10],
        "MIN": [0, 0]
    })

    # Act: Call our function
    result = calculate_per36(test_data, "PTS")

    # Assert: Verify the calculated value is NaN
    assert pd.isna(result)

def test_calculate_consistency():
    # Arrange: Create sample basketball statistics
    test_data = pd.DataFrame({
        "PTS": [20, 10, 15, 25, 30]
    })

    # Act: Call our function
    result = calculate_consistency(test_data, "PTS")

    # Assert: Verify the calculated value
    assert result == pytest.approx(7.9057, abs=0.001)

def test_calculate_consistency_single_game():
    # Arrange: Create sample basketball statistics with a single game
    test_data = pd.DataFrame({
        "PTS": [25]
    })

    # Act: Call our function
    result = calculate_consistency(test_data, "PTS")

    # Assert: Verify the calculated value is NaN
    assert pd.isna(result)

def test_calculate_rolling_average():
    # Arrange: Create six games of scoring data
    test_data = pd.DataFrame({
    "PTS": [10, 20, 30, 40, 50, 60]
    })
    # Act: Calculate a 3-game rolling average
    result = calculate_rolling_average(test_data, "PTS", 3)
    # Assert: Verify the results
    expected = pd.Series([None, None, 20.0, 30.0, 40.0, 50.0])
    pd.testing.assert_series_equal(result, expected, check_names=False)

def test_calculate_rolling_average_insufficient_games():
    # Arrange: Create two games of scoring data
    test_data = pd.DataFrame({
        "PTS": [10, 20]
    })

    # Act: Calculate a 3-game rolling average
    result = calculate_rolling_average(test_data, "PTS", 3)

    # Assert: Verify every result is NaN
    assert len(result) == 2
    assert result.isna().all()