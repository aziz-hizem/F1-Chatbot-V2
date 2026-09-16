"""Tests that run without a Groq API key: the LLM calls are replaced with fakes."""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import database  # noqa: E402
import main  # noqa: E402

CHAMPION_2021_SQL = """
SELECT d.forename, d.surname
FROM drivers d
JOIN driver_standings ds ON d.driverid = ds.driverid
WHERE ds.raceid = (SELECT raceid FROM races WHERE year = 2021 ORDER BY round DESC LIMIT 1)
ORDER BY ds.points DESC
LIMIT 1
"""


def test_select_query_returns_rows():
    assert database.execute_sql(CHAMPION_2021_SQL) == [{"forename": "Max", "surname": "Verstappen"}]


@pytest.mark.parametrize("query", [
    "DELETE FROM drivers",
    "DROP TABLE drivers",
    "UPDATE drivers SET surname = 'x'",
    "INSERT INTO seasons (year, url) VALUES (3000, 'x')",
])
def test_write_queries_are_rejected(query):
    assert "error" in database.execute_sql(query)
    assert database.execute_sql("SELECT COUNT(*) AS n FROM drivers")[0]["n"] > 0


def test_database_is_opened_read_only_even_for_disguised_writes():
    result = database.execute_sql("WITH x AS (SELECT 1) DELETE FROM drivers")
    assert "error" in result
    assert "readonly" in result["error"].replace(" ", "").lower()


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "get_sql_from_llama", lambda question: CHAMPION_2021_SQL)
    monkeypatch.setattr(main, "call_groq", lambda prompt: "Max Verstappen won the 2021 title 🏆")
    return TestClient(main.app)


def test_ask_returns_selected_responses(client):
    response = client.post("/ask", json={
        "question": "Who won the 2021 championship?",
        "selectedResponses": {"Response 1 (SQL)": True, "Response 2 (Best)": True, "Response 3 (Test)": False},
    })
    assert response.status_code == 200
    types = [r["type"] for r in response.json()["responses"]]
    assert types == ["sql", "refined"]
    assert "Verstappen" in response.json()["responses"][0]["content"]


def test_ask_falls_back_when_no_sql_is_generated(client, monkeypatch):
    monkeypatch.setattr(main, "get_sql_from_llama", lambda question: "Error: Unable to extract SQL query.")
    response = client.post("/ask", json={"question": "Who is the best driver ever?"})
    assert response.json()["responses"] == [{"type": "refined", "content": "Max Verstappen won the 2021 title 🏆"}]
