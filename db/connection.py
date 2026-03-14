import os
from dotenv import load_dotenv
import psycopg2

load_dotenv() # later move it to main or app.py

def get_connection():
    # try:
        connection = psycopg2.connect(
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            host = os.getenv('DB_HOST'),
            port= int(os.getenv('DB_PORT'))
        )
        return connection
    # except Exception as e:
        # print(f"An error occurred: {e}")