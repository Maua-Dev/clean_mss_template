import json
from typing import Any, Optional

import urllib3


class MicrosoftGraphClient:
    """Thin HTTP client for Microsoft Graph /me (or configured endpoint)."""

    def __init__(self, graph_endpoint: str, http: Optional[urllib3.PoolManager] = None):
        self.graph_endpoint = graph_endpoint
        self.http = http or urllib3.PoolManager()

    def get_user_profile(self, access_token: str) -> dict[str, Any]:
        """
        Fetch the signed-in user profile from Microsoft Graph.

        Args:
            access_token: Bearer token (without the "Bearer " prefix).

        Returns:
            Parsed JSON user payload from Graph.

        Raises:
            Exception: If Graph returns a non-200 status.
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.http.request("GET", self.graph_endpoint, headers=headers)

        if response.status != 200:
            raise Exception(
                f"Failed to fetch user information from Microsoft Graph - status: {response.status}"
            )

        return json.loads(response.data.decode("utf-8"))
