"""
sql.py
Created by Colin Gasiewicz on 03/06/2024
Authors: Colin Gasiewicz, Ryan Quirk
This script compliments input.py
it contains sql functions to interface with the database
such as inserting and searching the data
"""
import os
import mysql.connector
from dotenv import load_dotenv
# Load environment variables from the .env file
load_dotenv()


def connect():
    """
    Connect to the database using credentials from the environment variables
    :return: connection object
    """
    # Load environment variables from the .env file
    load_dotenv()
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME')
        )
        if conn.is_connected():
            return conn
    except mysql.connector.Error as e:
        print(e)
        return None


def checkemail(email, con):
    """
    Query the database with the passed connection (param: con).
    The query is created with the email hash that is passed (param: email).
    Returns a boolean according to the result of the query, i.e. the email
    found in the database returns True.
    """
    cursor = con.cursor()

    # Limit the query to 1 result to save time.
    query = 'SELECT username FROM users WHERE username = %s LIMIT 1'
    cursor.execute(query, (email,))

    if cursor.fetchone(): return True
    else: return False


def checkpassword(pwd, con):
    """
    Query the database with the passed connection (param: con).
    The query is created with the password hash that is passed (param: pwd).
    Returns a boolean according to the result of the query, i.e. the password
    NOT found in the database returns False.
    """
    cursor = con.cursor()

    # Limit the query to 1 result to save time.
    query = 'SELECT password FROM users WHERE password = %s LIMIT 1'
    cursor.execute(query, (pwd,))

    if cursor.fetchone():
        return True
    else:
        return False