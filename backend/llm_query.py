import os
import requests
import logging
import re
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")

# Log the loaded API key for debugging
logging.info("Loaded API Key: %s", API_KEY)

with open("schema.md", "r") as f:
    DB_SCHEMA = f.read()

PROMPT_TEMPLATE = """You are an intelligent assistant for F1 racing data. Your task is to answer user questions conversationally based on the database schema and query results provided. Strictly follow the schema provided below and do not make assumptions about columns or tables that are not explicitly listed.

### Database schema
{schema}

### Example Queries:
1. To find the driver champion in a specific season:
```sql
SELECT d.forename, d.surname, ds.points AS total_points
FROM drivers d
JOIN driver_standings ds ON d.driverid = ds.driverid
WHERE ds.raceid = (
  SELECT raceid FROM races WHERE year = <year> ORDER BY round DESC LIMIT 1
)
ORDER BY total_points DESC
LIMIT 1;
```

2. To find the constructor champion for a specific season:
```sql
SELECT c.name, cs.points AS total_points
FROM constructors c
JOIN constructor_standings cs ON c.constructorid = cs.constructorid
WHERE cs.raceid = (
  SELECT raceid FROM races WHERE year = <year> ORDER BY round DESC LIMIT 1
)
ORDER BY total_points DESC
LIMIT 1;
```

3. To find the winner of a specific race:
```sql
SELECT r.name, d.forename, d.surname, res.positionorder AS finishing_position
FROM races r
JOIN results res ON r.raceid = res.raceid
JOIN drivers d ON res.driverid = d.driverid
WHERE r.name LIKE '%Monaco Grand Prix%' AND r.year = 2024
ORDER BY res.positiontext ASC
LIMIT 1;
```

4. To count the number of championships won by a driver:
```sql
SELECT COUNT(*) AS championships
FROM (
  SELECT r.year
  FROM races r
  JOIN driver_standings ds ON r.raceid = ds.raceid
  WHERE r.raceid IN (
    SELECT MAX(raceid)
    FROM races
    GROUP BY year
  )
  AND ds.driverid = (
    SELECT driverid FROM drivers WHERE forename = '<forename>' AND surname = '<surname>'
  )
  AND ds.position = 1
  GROUP BY r.year
) AS championship_years;
```

5. To count the number of championships won by a constructor/team :
```sql
SELECT COUNT(*) AS championships
FROM (
  SELECT r.year
  FROM races r
  JOIN constructor_standings cs ON r.raceid = cs.raceid
  WHERE r.raceid IN (
    SELECT MAX(raceid)
    FROM races
    GROUP BY year
  )
  AND cs.constructorid = (
    SELECT constructorid FROM constructors WHERE name = '<name>'
  )
  AND cs.position = 1
  GROUP BY r.year
) AS championship_years;
```



### Notice :
In Results tables :
- Grid column is for starting positions.
- Positiontext column is for finishing positions and they contain drivers who did not finish the race.


### Question
{question}

### SQL query:
Generate an accurate SQL query to answer the question based on the schema. Ensure the query only references columns and tables that exist in the schema.

### Query results
{results}

### Response:
Generate a conversational response based on the query results. If the results are empty, do not mention the query or its execution. Instead, explain why the results might be empty and suggest alternative queries or approaches. Format the response clearly and concisely.
"""

RESULT_FORMATTING_PROMPT = """You are an intelligent assistant for F1 racing data. Your task is to generate a conversational response based on the raw query results provided. Do not mention the query or its execution. Focus solely on providing a clear and concise answer to the user's question.

### Question
{question}

### Query results
{results}

### Rule :
If the results are empty, try to answer yourself but only if you're absolutely sure about the answer. Otherwise, explain why the results might be empty and suggest alternative queries or approaches.

### Response:
Generate a human conversation like response based on the query results. Format the response clearly and concisely.
Use one or two emojis to make the response more engaging and friendly.
"""

FINAL_PROMPT = """
You are an intelligent assistant for F1 racing data. Your task is to generate a conversational response based on the raw query results provided. Do not mention the query or its execution. Focus solely on providing a clear and concise answer to the user's question.

### Question
{question}

### Result
{results}

### Response:
Filter the response and only take the part specific to answering the question and remove all other parts.
Generate a human conversation like response.
Use one or two emojis to make the response more engaging and friendly.
"""

FAILED_SQL_PROMPT= """

### Question:
{question}

### Response:
You are an intelligent assistant for F1 racing data. Your task is to generate a conversational response to this question.
Focus solely on providing a clear and concise answer to the user's question.
Make sure your information is correct.
"""

def get_sql_from_llama(question: str, results: str = "No results available") -> str:
    prompt = PROMPT_TEMPLATE.format(schema=DB_SCHEMA, question=question, results=results)


    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.0
            }
        )
      

        # Extract the SQL query from the response
        if "choices" in response.json():
            content = response.json()["choices"][0]["message"]["content"]
            match = re.search(r"```sql\n(.*?)```", content, re.DOTALL)
            if match:
                sql_query = match.group(1).strip()
                return sql_query
            else:
                logging.error("No SQL query found in the LLM response")
                return "Error: Unable to extract SQL query. Please try again."
        else:
            logging.error("'choices' key not found in LLM API response")
            return "Error: Unable to generate SQL query. Please try again."

    except Exception as e:
        logging.error("Exception occurred while calling LLM API: %s", str(e))
        return "Error: An issue occurred while processing your request."