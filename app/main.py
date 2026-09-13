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

    results = execute_query(sql)

    print("\nResult:")
    for row in results:
        print(row)