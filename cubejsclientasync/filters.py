"""Contains classes for working with filters"""

from typing import Any, Dict, List, Optional, Union

from .enums import FilterOperator, TimeGranularity
from .objects import Dimension, Measure

__ALL__ = ["DateRange", "TimeDimension", "Filter", "Or", "And"]


class DateRange:
    """Represents an absolute or relative date range for filtering"""

    def __init__(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        relative: Optional[str] = None,
    ) -> None:
        """Initializer

        Args:
            start_date: Start date for the absolute range. Format `YYYY-MM-DD`
                or `YYYY-MM-DDTHH:mm:ss.SSS`.
            end_date: End date for the absolute range. Format `YYYY-MM-DD`
                or `YYYY-MM-DDTHH:mm:ss.SSS`.
            relative: Relative date range, e.g. "this month"

        """
        assert (start_date is not None and end_date is not None) or (
            relative is not None
        )
        self.start_date = start_date
        self.end_date = end_date
        self.relative = relative

    def serialize(self) -> Union[List[str], str]:
        """Serialize the object for building a query

        Raises:
            ValueError: if the start and end date or relative date range was not provided

        Returns:
            list of (start date, end date) or the relative date range

        """
        if self.start_date is not None and self.end_date is not None:
            return [self.start_date, self.end_date]
        elif self.relative:
            return self.relative
        else:
            raise ValueError("Expected (start date, end date) or relative")


class TimeDimension:
    """Represents the combo of a time dimension and filter"""

    def __init__(
        self,
        dimension: Dimension,
        date_range: DateRange,
        compare_date_range: Optional[List[DateRange]] = None,
        granularity: TimeGranularity = TimeGranularity.null,
    ) -> None:
        """Initializer

        Args:
            dimension: Time dimension reference
            date_range: Absolute or relative date range
            compare_date_range: An array of date ranges to compare a measure change over
                previous period
            granularity: A granularity for a time dimension

        """
        self.dimension = dimension
        self.date_range = date_range
        self.compare_date_range = compare_date_range
        self.granularity = granularity

    def serialize(self) -> Dict[str, Any]:
        """Serialize the object for building a query

        Returns:
            dict of properties

        """
        result = {
            "dimension": self.dimension.serialize(),
            "dateRange": self.date_range.serialize(),
            "granularity": self.granularity.value,
        }
        if self.compare_date_range:
            result["compareDateRange"] = [
                dr.serialize() for dr in self.compare_date_range
            ]

        return result


class Filter:
    """Represents a data filter"""

    def __init__(
        self,
        member: Union[Dimension, Measure],
        operator: FilterOperator,
        values: Optional[List[Any]] = None,
    ) -> None:
        """Initializer

        Args:
            member: Dimension or measure to be used in the filter
                * When you filter on a dimension, you are restricting the raw data
                  before any calculations are made.
                * When you filter on a measure, you are restricting the results after
                  the measure has been calculated.
            operator: An operator to be used in the filter.
            values: An array of values for the filter.

        """
        self.member = member
        self.operator = operator
        self.values = values

    def serialize(self) -> Dict[str, Any]:
        """Serialize the object for building a query

        Returns:
            dict of properties

        """
        return {
            "member": self.member.serialize(),
            "operator": self.operator.value,
            "values": [str(value) for value in self.values],
        }


class BooleanExpression:
    """Represents a boolean operator in a filter"""

    operator: str

    def __init__(self, *operands: Union["BooleanExpression", Filter]) -> None:
        """Initializer

        Args:
            operands: An array with two or more filters or other boolean operators

        """
        self.operands = operands

    def serialize(self) -> Dict[str, List[Any]]:
        """Serialize the object for building a query

        Returns:
            dict of properties

        """
        return {self.operator: [o.serialize() for o in self.operands]}


class Or(BooleanExpression):
    """Boolean operator for `or`"""

    operator = "or"


class And(BooleanExpression):
    """Boolean operator for `and`"""

    operator = "and"
