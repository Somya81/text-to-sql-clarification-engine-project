import os
from dotenv import load_dotenv
from google import genai
from clarification import ClarificationResult

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_sql(question,schema=None):
    if schema:
        schema_text=", ".join(schema)
        database_info=f"""
Table: uploaded_data
Columns:
{schema_text}
"""
    else:
        database_info="""
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

orders.customer_id = customers.customer_id
orders.product_id = products.product_id

"""
    prompt = f"""
You are a SQL assistant.

Convert the user's natural language question
into one correct MySQL SELECT query.

Database:

{database_info}

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


def check_clarification(question,schema=None):
    if schema:
        schema_text=", ".join(schema)
        database_info=f"""
Table:uploaded_data
Columns:
{schema_text}
"""
    else:
        database_info="""
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

    orders.customer_id = customers.customer_id
    orders.product_id = products.product_id
    """
    prompt = f"""
You are a clarification assistant for a Text-to-SQL system.

Your job is to decide whether the user's question contains
enough information to generate ONE correct SQL query.




Ask for clarification ONLY when an important detail is missing.

Examples:

"Show customers"
-> clarification needed
Question:
"Do you want to see all customers or customers from a specific city?"

"Show all customers"
-> no clarification needed

"Show customers from Mumbai"
-> no clarification needed

"Show expensive products"
-> clarification needed
Question:
"What price should be considered expensive?"

"Show products above 10000"
-> no clarification needed

"Show recent orders"
-> clarification needed
Question:
"What date range should be considered recent?"

"Show orders from August 2026"
-> no clarification needed

"Which customer spent the most?"
-> no clarification needed

Return:

- needs_clarification = true when important information is missing.
- needs_clarification = false when the question is clear.
- If clarification is needed, provide one short question.
- If clarification is not needed, question must be null.

User question:

{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ClarificationResult,
        },
    )

    return ClarificationResult.model_validate_json(response.text)