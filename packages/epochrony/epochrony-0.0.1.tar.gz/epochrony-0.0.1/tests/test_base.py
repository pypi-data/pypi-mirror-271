"""
Test base class
"""

from datetime import datetime
from epochrony import Epochrony


def test_recurring_dates_by_end_date():
    """
    Test dates in the future are correctly calculated when an end date is
    specified
    """

    service = Epochrony()
    dates = service.get_recurring_dates(
        start_date=datetime(2020, 1, 1),
        end_date=datetime(2020, 1, 10),
        increment_days=2,
        limit=None,
    )

    assert dates == [
        datetime(2020, 1, 1),
        datetime(2020, 1, 3),
        datetime(2020, 1, 5),
        datetime(2020, 1, 7),
        datetime(2020, 1, 9),
    ]


def test_recurring_dates_by_limit():
    """
    Test dates in the future are correctly calculated when a limit is specified
    """

    service = Epochrony()
    dates = service.get_recurring_dates(
        start_date=datetime(2024, 1, 30),
        end_date=None,
        increment_days=2,
        limit=2,
    )

    assert dates == [
        datetime(2024, 1, 30),
        datetime(2024, 2, 1),
    ]
