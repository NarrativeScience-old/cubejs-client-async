"""Contains tests for the query module"""

import unittest

from cubejsclient import Cube, DateRange, Order, Query, TimeDimension, TimeGranularity


class QueryTests(unittest.TestCase):
    """Tests Query"""

    def test_basic(self):
        """Should serialize a query"""
        cube = Cube("c__app-123__us_accidents")
        q = Query(
            measures=[cube.measure("foo")],
            dimensions=[cube.dimension("bar")],
            time_dimensions=[
                TimeDimension(
                    cube.dimension("time"),
                    DateRange(relative="last year"),
                    granularity=TimeGranularity.month,
                )
            ],
            order=[(cube.dimension("bar"), Order.asc)],
        )
        self.assertEqual(
            q.serialize(),
            {
                "measures": ["c__app-123__us_accidents.foo"],
                "time_dimensions": [
                    {
                        "dimension": "c__app-123__us_accidents.time",
                        "dateRange": "last year",
                        "granularity": "month",
                    }
                ],
                "limit": 10000,
                "offset": 0,
                "timezone": "UTC",
                "ungrouped": False,
                "dimensions": ["c__app-123__us_accidents.bar"],
                "order": [("c__app-123__us_accidents.bar", "asc")],
            },
        )
