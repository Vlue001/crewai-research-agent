from unittest.mock import MagicMock, patch

import pytest
import requests

from src.tools.search_tool import SearchTool


@pytest.fixture
def tool():
    return SearchTool()


def test_returns_formatted_results(tool, mock_serper_response, monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "test-key")

    with patch("src.tools.search_tool.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_serper_response
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = tool._run(query="test query")

    assert "Test Result 1" in result
    assert "https://example.com/1" in result
    assert "test snippet for result 1" in result


def test_includes_answer_box(tool, mock_serper_response_with_answer_box, monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "test-key")

    with patch("src.tools.search_tool.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_serper_response_with_answer_box
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = tool._run(query="what is the answer")

    assert "FEATURED ANSWER" in result
    assert "42 is the answer to everything" in result


def test_missing_api_key_returns_error(tool, monkeypatch):
    monkeypatch.delenv("SERPER_API_KEY", raising=False)

    result = tool._run(query="test query")

    assert "Error" in result
    assert "SERPER_API_KEY" in result


def test_handles_connection_error(tool, monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "test-key")

    with patch("src.tools.search_tool.requests.post") as mock_post:
        mock_post.side_effect = requests.exceptions.ConnectionError("Connection failed")

        result = tool._run(query="test query")

    assert "Search failed" in result


def test_empty_results(tool, monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "test-key")

    with patch("src.tools.search_tool.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = {"organic": []}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        result = tool._run(query="very obscure query")

    assert "No results found" in result


def test_sends_correct_headers(tool, mock_serper_response, monkeypatch):
    monkeypatch.setenv("SERPER_API_KEY", "my-secret-key")

    with patch("src.tools.search_tool.requests.post") as mock_post:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_serper_response
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        tool._run(query="test")

    _, kwargs = mock_post.call_args
    assert kwargs["headers"]["X-API-KEY"] == "my-secret-key"
    assert kwargs["json"]["q"] == "test"
