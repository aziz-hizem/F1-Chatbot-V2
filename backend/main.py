import json
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from database import execute_sql
from llm_query import (
    FAILED_SQL_PROMPT,
    FINAL_PROMPT,
    RESULT_FORMATTING_PROMPT,
    call_groq,
    get_sql_from_llama,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def ask_llm(prompt: str) -> str | None:
    try:
        return call_groq(prompt)
    except Exception as e:
        logging.error("Exception occurred while calling LLM API: %s", str(e))
        return None


@app.get("/")
def root():
    return {"message": "Welcome to the F1 Chatbot API! Please use the frontend to interact with the chatbot."}


@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")
    selected_responses = data.get("selectedResponses", {})

    sql_query = get_sql_from_llama(question)

    # No usable SQL: fall back to answering from the model's own knowledge
    if sql_query.startswith("Error"):
        responses = []
        answer = ask_llm(FAILED_SQL_PROMPT.format(question=question))
        if answer:
            responses.append({"type": "refined", "content": answer})
        return {"question": question, "responses": responses}

    result = execute_sql(sql_query)
    results_json = json.dumps(result, indent=2)

    logging.info("Generated SQL Query: %s", sql_query)
    logging.info("Query Results: %s", results_json)

    responses = []

    # Raw query results
    if selected_responses.get("Response 1 (SQL)", False):
        responses.append({"type": "sql", "content": results_json})

    # Conversational answer built from the results
    if selected_responses.get("Response 2 (Best)", False):
        answer = ask_llm(RESULT_FORMATTING_PROMPT.format(question=question, results=results_json))
        if answer:
            responses.append({"type": "refined", "content": answer})

    # Experimental answer that keeps only the part answering the question
    if selected_responses.get("Response 3 (Test)", False):
        answer = ask_llm(FINAL_PROMPT.format(question=question, results=results_json))
        if answer:
            responses.append({"type": "final", "content": answer})

    return {"question": question, "responses": responses}
