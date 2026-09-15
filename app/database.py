import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def execute_query(sql):

    sql=sql.strip().rstrip(";").strip()
    upper_sql=sql.upper()
    if upper_sql.startswith("SELECT"):
        pass
    elif upper_sql.startswith("WITH") and "SELECT" in upper_sql:
        pass
    else:
        raise ValueError(
            "Only SELECT and WITH... SELECT queries are allowed."
        )

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()
    cursor.execute(sql)

    results = cursor.fetchall()
    columns=[column[0] for column in cursor.description]

    cursor.close()
    connection.close()

    return columns,results