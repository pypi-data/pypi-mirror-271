"""
Base module to provide main package class
"""

from datetime import datetime, timedelta


class Epochrony:
    """
    Main application class
    """

    def __init__(self) -> None:
        """
        Initial class
        """
        self.start_date = datetime.now()

    def get_recurring_dates(
        self,
        increment_days: int = 7,
        start_date: datetime | None = None,
        limit: int | None = 100,
        end_date: datetime | None = None,
    ):
        """
        Given an initial date, calculate recurring dates in the future
        """

        if limit is None:
            limit = 7

        if start_date is not None:
            self.start_date = start_date

        loop_date = self.start_date

        output = []

        while len(output) < limit:
            output.append(loop_date)
            loop_date += timedelta(increment_days)

            # Exit if an end date was provided
            if end_date is not None and loop_date > end_date:
                break

        return output

    def get_grouped_dates(self):
        """
        Group a number of different start dates
        """
