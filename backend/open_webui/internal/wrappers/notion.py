"""
Simple Notion API client wrapper for basic database and page queries.
"""
import requests

class NotionClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

    def list_databases(self) -> dict:
        """List databases available in the integration"""
        url = f"{self.base_url}/databases"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def query_database(
        self,
        database_id: str,
        filter: dict = None,
        sorts: list = None,
        start_cursor: str = None,
        page_size: int = 100
    ) -> dict:
        """Query a Notion database to retrieve pages (rows)"""
        url = f"{self.base_url}/databases/{database_id}/query"
        body: dict = {"page_size": page_size}
        if filter is not None:
            body["filter"] = filter
        if sorts is not None:
            body["sorts"] = sorts
        if start_cursor:
            body["start_cursor"] = start_cursor
        resp = requests.post(url, headers=self.headers, json=body)
        resp.raise_for_status()
        return resp.json()

    def get_page(self, page_id: str) -> dict:
        """Retrieve a single Notion page by its ID"""
        url = f"{self.base_url}/pages/{page_id}"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()