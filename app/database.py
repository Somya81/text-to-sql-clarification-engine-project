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

def load_csv_to_mysql(df,table_name="uploaded_data"):
    connection=mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    cursor=connection.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    columns=list(df.columns)
    columns_definitions=",".join(
        [f"`{column}` TEXT" for column in columns]
    )
    create_table_query=f"""
    CREATE TABLE {table_name}(
    {columns_definitions})
    """
    cursor.execute(create_table_query)
    # Data insert
    placeholders = ", ".join(["%s"] * len(columns))

    insert_query = f"""
    INSERT INTO {table_name}
    ({", ".join([f"`{column}`" for column in columns])})
    VALUES ({placeholders})
    """

    data = [
        tuple(row)
        for row in df.itertuples(index=False, name=None)
    ]

    cursor.executemany(insert_query, data)
    connection.commit()

    cursor.close()
    connection.close()

def get_table_schema(table_name="uploaded_data"):

    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor()

    cursor.execute(f"DESCRIBE {table_name}")

    schema = cursor.fetchall()

    cursor.close()
    connection.close()

    columns = [row[0] for row in schema]

    return columns