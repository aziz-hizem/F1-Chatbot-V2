import logging
import os
import re
import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "f1_database.db")

logging.info("Using database path: %s", DB_PATH)

# The SQL is written by an LLM from user input, so it must never be able to change data
READ_ONLY_QUERY = re.compile(r"^\s*(SELECT|WITH)\b", re.IGNORECASE)


def execute_sql(query: str):
    if not READ_ONLY_QUERY.match(query):
        return {"error": "Only read-only SELECT queries are allowed."}

    try:
        # mode=ro makes SQLite itself reject any write, whatever the query contains
        uri = Path(DB_PATH).resolve().as_uri() + "?mode=ro"
        with closing(sqlite3.connect(uri, uri=True)) as conn:
            cursor = conn.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row)) for row in rows]
    except Exception as e:
        return {"error": str(e)}
