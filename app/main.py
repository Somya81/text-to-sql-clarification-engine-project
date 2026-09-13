from llm import generate_sql,check_clarification
from database import execute_query

question = input("Ask Your Sawal - ")
clarification=check_clarification(question)
if clarification.needs_clarification:
    print("\nCould you clarify")
    print(clarification.question)
else:
    sql = generate_sql(question)

    print("\nGenerated SQL:")
    print(sql)

    columns,results = execute_query(sql)

    print("\nResult:")
    print(" | ".join(columns))
    for row in results:
        print(" | ".join(str(value) for value in row))