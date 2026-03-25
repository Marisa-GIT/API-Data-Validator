import mysql.connector

def connect_db():

    conn = mysql.connector.connect(
        host="localhost",
        user="qa_user",
        password="api_validator_test",
        database="api_project"
    )
    return conn



