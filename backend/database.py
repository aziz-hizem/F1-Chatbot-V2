import os
import sqlite3
import logging

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "f1_database.db")

logging.info("Using database path: %s", DB_PATH)

def execute_sql(query: str):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row)) for row in rows]
    except Exception as e:
        return {"error": str(e)}





