from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from llm_query import get_sql_from_llama, PROMPT_TEMPLATE, DB_SCHEMA, API_KEY, RESULT_FORMATTING_PROMPT, FINAL_PROMPT, FAILED_SQL_PROMPT
from database import execute_sql
import requests
import json
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later restrict this to your frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the F1 Chatbot API! Please use the frontend to interact with the chatbot."}

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")
    selected_responses = data.get("selectedResponses", {})

    sql_query = get_sql_from_llama(question)

    # Check if the SQL query generation failed
    if sql_query.startswith("Error"):
        # MADE IT MYSELFFFFFFFFFFFFFFFFFFFFFF !!!!!!!!!!!
        failed_sql_prompt = FAILED_SQL_PROMPT.format(
            question=question
        )

        responses = []  # Ensure responses list is defined

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": failed_sql_prompt}],
                "temperature": 0.3
            }
        )

        if "choices" in response.json():
            refined_response = response.json()["choices"][0]["message"]["content"]
            responses.append({"type": "refined", "content": refined_response})

        return {
                "question": question,
                "responses": responses
            }

    result = execute_sql(sql_query)

    # Essential logging for the query and the result
    logging.info("Generated SQL Query: %s", sql_query)
    logging.info("Query Results: %s", json.dumps(result, indent=2))

    # Limit the length of the query results sent to the LLM
    if len(json.dumps(result)) > 1000:  # Example threshold
        result = result  # Limit to the first 5 results for brevity by doing this result = result[:5] but i took it off
        logging.warning("Query results truncated due to length.")

    responses = []

    # Add SQL query response if selected
    if selected_responses.get("Response 1 (SQL)", False):
        responses.append({"type": "sql", "content": json.dumps(result, indent=2)})

    # Generate refined responses if selected
    if selected_responses.get("Response 2 (Best)", False):
        formatting_prompt = RESULT_FORMATTING_PROMPT.format(
            question=question,
            results=json.dumps(result, indent=2)
        )

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": formatting_prompt}],
                "temperature": 0.3
            }
        )

        if "choices" in response.json():
            refined_response = response.json()["choices"][0]["message"]["content"]
            responses.append({"type": "refined", "content": refined_response})

    if selected_responses.get("Response 3 (Test)", False):
        final_prompt = FINAL_PROMPT.format(
            question=question,
            results=json.dumps(result, indent=2)
        )

        final_response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": final_prompt}],
                "temperature": 0.3
            }
        )

        if "choices" in final_response.json():
            final_filtered_response = final_response.json()["choices"][0]["message"]["content"]
            responses.append({"type": "final", "content": final_filtered_response})

    return {
        "question": question,
        "responses": responses
    }