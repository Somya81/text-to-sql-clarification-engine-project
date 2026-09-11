from llm import generate_sql
from database import excute_query

question=input("Ask Your Sawal - ")
sql=generate_sql(question)

print("\nGenerate SQL: ")
print(sql)

results=excute_query(sql)

print("\nResult: ")
for row in results:
    print(row)