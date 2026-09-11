import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def execute_query(sql):
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()
    cursor.execute(sql)

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return results