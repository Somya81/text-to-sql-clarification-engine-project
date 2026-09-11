import os
from dotenv import load_dotenv
from google import genai
load_dotenv()

client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_sql(question):
    prompt=f"""
You are a SQL assistant. 
Database:
customers(
    customer_id,
    name,
    city,
    email
)
Convert the user's question into a MySQL SELECT query. 
User question:
{question}
Return only the SQL query.
"""
    response=client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    sql=response.text.strip()
    sql=sql.replace("```sql", "")
    sql = sql.replace("```", "")    
    return sql.strip()
question = "Show customers who are from Mumbai"

sql = generate_sql(question)

print(sql)