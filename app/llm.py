import os
from dotenv import load_dotenv
from google import genai
from clarification import ClarificationResult
load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_sql(question):
    prompt = f"""
You are a SQL assistant.
Decide whether the user's question is specific enough
to generate a correct SQL query.

If important information is missing, clarification is needed.
Example:
"Show customers" -> unclear
"Show customers from Mumbai" -> clear
"Show all customers" -> clear
Database:

customers(
    customer_id,
    name,
    city,
    email
)
products(
    product_id,
    product_name,
    category,
    price
)
orders(
    order_id,
    customer_id,
    product_id,
    quantity,
    order_date
)
Relationships:
orders.customer_id=customers.customer_id
orders.product_id=products.product_id
Rules:
- Generate only SELECT queries.
- You can use JOIN, GROUP BY, HAVING, ORDER BY, COUNT, SUM, AVG and LIMIT.
- Do not generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE or CREATE.
- Use the correct table and column names.
- Return only the SQL query.
User question:

{question}

Return only the SQL query.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    sql = response.text.strip()
    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")

    return sql.strip()

def check_clarification(question):
    prompt=f"""
Decide if user's question is clear enough to generate SQL.
User question:
{question}
"""
    response=client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type":"application/json",
            "response_schema":ClarificationResult,
        },
    )
    return ClarificationResult.model_validate_json(response.text)