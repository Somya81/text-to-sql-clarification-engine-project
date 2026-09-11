from llm import generate_sql
from database import execute_query

question = input("Ask Your Sawal - ")

sql = generate_sql(question)

print("\nGenerated SQL:")
print(sql)

results = execute_query(sql)

print("\nResult:")
for row in results:
    print(row)