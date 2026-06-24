import os
from typing import Type

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class SearchInput(BaseModel):
    query: str = Field(..., description="The search query to look up on the web")


class SearchTool(BaseTool):
    name: str = "Web Search"
    description: str = (
        "Search the web for current information on any topic. "
        "Returns titles, links, and snippets from top search results."
    )
    args_schema: Type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Error: SERPER_API_KEY not set in environment variables."

        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
        }
        payload = {"q": query, "num": 10}

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return f"Search failed: {e}"

        results = []

        if "answerBox" in data:
            box = data["answerBox"]
            answer = box.get("answer") or box.get("snippet", "")
            if answer:
                results.append(f"FEATURED ANSWER: {answer}\n")

        for item in data.get("organic", []):
            title = item.get("title", "No title")
            link = item.get("link", "")
            snippet = item.get("snippet", "No description available")
            results.append(f"Title: {title}\nURL: {link}\nSummary: {snippet}\n")

        if not results:
            return "No results found for the given query."

        return "\n---\n".join(results)
