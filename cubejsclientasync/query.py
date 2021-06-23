"""Contains Query builder class"""

from typing import Any, Dict, List, Optional, Tuple, Union

from .enums import Order
from .filters import Filter, TimeDimension
from .objects import Dimension, Measure, Segment


class Query:
    """Class to build Cube.js queries"""

    def __init__(
        self,
        measures: List[Measure],
        time_dimensions: List[TimeDimension],
        dimensions: Optional[List[Dimension]] = None,
        filters: Optional[List[Filter]] = None,
        segments: Optional[List[Segment]] = None,
        limit: int = 10_000,
        offset: int = 0,
        order: Optional[List[Tuple[Union[Dimension, Measure], Order]]] = None,
        timezone: str = "UTC",
        ungrouped: bool = False,
    ) -> None:
        """Initializer

        Args:
            measures: List of measures
            time_dimensions: List of time dimensions for filtering/grouping
            dimensions: List of dimensions for grouping
            filters: List of filters
            segments: List of segments
            limit: Limit the result set
            offset: Offset to control pagination
            order: Ordering configuration for the result set
            timezone: Local timezone to reflect in the data
            ungrouped: Whether to not GROUP BY in the query

        """
        self.measures = measures
        self.time_dimensions = time_dimensions
        self.dimensions = dimensions
        self.filters = filters
        self.segments = segments
        self.limit = limit
        self.offset = offset
        self.order = order
        self.timezone = timezone
        self.ungrouped = ungrouped

    def serialize(self) -> Dict[str, Any]:
        """Serialize the object for building a query

        Returns:
            query dict

        """
        result = {
            "measures": [m.serialize() for m in self.measures],
            "timeDimensions": [d.serialize() for d in self.time_dimensions],
            "limit": self.limit,
            "offset": self.offset,
            "timezone": self.timezone,
            "ungrouped": self.ungrouped,
        }
        if self.dimensions:
            result["dimensions"] = [d.serialize() for d in self.dimensions]
        if self.filters:
            result["filters"] = [f.serialize() for f in self.filters]
        if self.segments:
            result["segments"] = [s.serialize() for s in self.segments]
        if self.order:
            result["order"] = [
                (obj.serialize(), order.value) for obj, order in self.order
            ]

        return result
