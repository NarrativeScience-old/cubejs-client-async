"""Contains the Cube.js API client"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import backoff
import httpx
import jwt

from .query import Query


class CubeClient:
    """Cube.js API client"""

    def __init__(
        self,
        host: str = "http://localhost:4000",
        base_path: str = "/cubejs-api",
        secret: Optional[str] = None,
        load_request_timeout: float = 30.0,
        token_ttl_hours: int = 1,
    ) -> None:
        """Initializer

        Args:
            host: Cube.js API host
            base_path: Cube.js API base path
            secret: Secret for signing tokens. Set to None to skip authentication.
            load_request_timeout: Timeout in seconds to wait for load responses
            token_ttl_hours: TTL in hours for the token lifetime

        """
        self._secret = secret
        self._load_request_timeout = load_request_timeout
        self._token_ttl_hours = token_ttl_hours
        self._http_client = httpx.AsyncClient(
            base_url=f"{host.rstrip('/')}/{base_path.strip('/')}"
        )

        self._token = None

    def _get_signed_token(self) -> Optional[str]:
        """Get or refresh the authentication token

        Returns:
            token or None if no secret was configured

        """
        if not self._secret:
            return None

        now = datetime.now()
        if not self._token or self._token_expiration <= now:
            self._token_expiration = now + timedelta(hours=self._token_ttl_hours)
            self._token = jwt.encode(
                {"exp": self._token_expiration}, self._secret, algorithm="HS256"
            )

        return self._token

    @property
    def token(self) -> Optional[str]:
        """Alias for getting the current token value"""
        return self._get_signed_token()

    async def load(self, query: Query) -> Dict[str, Any]:
        """Get the data for a query.

        Args:
            query: Query object

        Returns:
            dict with properties:
            * query -- The query passed via params
            * data -- Formatted dataset of query results
            * annotation -- Metadata for query. Contains descriptions for all query
                items.
                * title -- Human readable title from data schema.
                * shortTitle -- Short title for visualization usage (ex. chart overlay)
                * type -- Data type

        """
        return await self._request(
            "post",
            "/v1/load",
            body={"query": query.serialize()},
            timeout=self._load_request_timeout,
        )

    @backoff.on_exception(
        backoff.expo, httpx.RequestError, max_tries=8, jitter=backoff.random_jitter
    )
    async def _request(
        self, method: str, path: str, body: Optional[Any] = None, timeout: float = 5.0
    ):
        """Make API request to Cube.js server

        Args:
            method: HTTP method
            path: URL path
            body: Body to send with the request, if applicable
            timeout: Request timeout in seconds

        Returns:
            response data

        """
        headers = {}
        if self.token:
            headers["Authorization"] = self.token

        async with self._http_client as client:
            response = await client.request(
                method, path, json=body, headers=headers, timeout=timeout
            )
            response.raise_for_status()
            return response.json()
