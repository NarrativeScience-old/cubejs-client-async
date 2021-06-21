"""Contains tests for the client module"""

import asyncio
import unittest

from cubejsclient import (
    Cube,
    CubeClient,
    DateRange,
    Filter,
    FilterOperator,
    Order,
    Query,
    TimeDimension,
)


class CubeClientTests(unittest.TestCase):
    """Tests CubeClient"""

    def test_init(self):
        """Should set base url"""
        self.assertEqual(
            CubeClient()._http_client.base_url, "http://localhost:4000/cubejs-api/"
        )


if __name__ == "__main__":
    cube = Cube("wshn2mul")
    q = Query(
        measures=[cube.measure("count")],
        dimensions=[cube.dimension("state"), cube.dimension("county")],
        time_dimensions=[
            TimeDimension(cube.dimension("start_time"), DateRange(relative="last year"))
        ],
        filters=[Filter(cube.dimension("state"), FilterOperator.equals, ["WA"])],
        order=[(cube.dimension("count"), Order.desc)],
    )
    client = CubeClient()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(client.load(q))
    print(result)  # noqa: T001
