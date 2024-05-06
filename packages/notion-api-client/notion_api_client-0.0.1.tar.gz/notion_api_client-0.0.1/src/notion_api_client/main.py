import requests
import json


class Notion:
    def __init__(self, bearer_token: str, notion_version: str):
        self.base_url = "https://api.notion.com/v1/"
        self.bearer_token = bearer_token
        self.notion_version = notion_version


class NotionDatabase:
    def __init__(self, notion: Notion, database_id: str):
        self.notion = notion
        self.database_id = database_id

    def retrieve_database(self) -> dict:
        headers = {"Authorization": f"Bearer {self.notion.bearer_token}",
                   "Notion-Version": f"{self.notion.notion_version}"}
        url = f"{self.notion.base_url}databases/{self.database_id}"
        r = requests.get(url, headers=headers)
        return json.loads(r.text)

    def query_database(self, query: str) -> dict:
        headers = {"Authorization": f"Bearer {self.notion.bearer_token}",
                   "Content-Type": "application/json",
                   "Notion-Version": f"{self.notion.notion_version}"}
        url = f"{self.notion.base_url}databases/{self.database_id}/query"
        r = requests.post(url, headers=headers, data=query)
        return json.loads(r.text)

    def query_database_results(self, query: str) -> list[dict]:
        return self.query_database(query)["results"]
