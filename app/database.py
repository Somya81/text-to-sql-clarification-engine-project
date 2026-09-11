import mysql.connector
connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shiv@ni22",
    database="text_to_sql_db"
)
import os
from dotenv import load_dotenv
load_dotenv()
def excute_query(sql):
    connection=mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
# if connection.is_connected():
#     print("MySQL connection successful!")

cursor=connection.cursor()
cursor.execute("SELECT * FROM customers")
results=cursor.fetchall()
for row in results:
    print(row)
cursor.close()
    cursor=connection.cursor()
    cursor.execute(sql)
    results=cursor.fetchall()
    cursor.close()
    connection.close()
    return results

connection.close()
query = "SELECT name, city FROM customers WHERE city = 'Mumbai'"
results = excute_query(query)
for row in results:
    print(row)
