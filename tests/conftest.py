import pytest


@pytest.fixture
def mock_serper_response():
    return {
        "organic": [
            {
                "title": "Test Result 1",
                "link": "https://example.com/1",
                "snippet": "This is a test snippet for result 1.",
            },
            {
                "title": "Test Result 2",
                "link": "https://example.com/2",
                "snippet": "This is a test snippet for result 2.",
            },
        ]
    }


@pytest.fixture
def mock_serper_response_with_answer_box():
    return {
        "answerBox": {
            "answer": "42 is the answer to everything.",
        },
        "organic": [
            {
                "title": "The Answer",
                "link": "https://example.com/answer",
                "snippet": "Douglas Adams wrote about this.",
            }
        ],
    }
