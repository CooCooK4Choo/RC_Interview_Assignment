from os import getenv
from typing import Optional
import psycopg2


# Create reusable connection to DB
def connect_to_db():
    try:

        conn = psycopg2.connect(
            database=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            host=getenv("DB_HOST"),
            port=getenv("DB_PORT"),
            password=getenv("DB_PASSWORD"),
        )
        return conn
    except:
        raise FailedToConnectToDBException


# Creating Specific database call
def get_all_items():
    """Get title and description from todo_items"""

    # Connect to DB
    conn = connect_to_db()

    try:
        # Using context manager to auto close cursor
        with conn.cursor() as db:
            db.execute(
                """ SELECT title, 
                       description 
                       FROM todo_list.todo_items
                       ORDER BY created_at DESC;"""
            )
            list_of_items = db.fetchall()

        return list_of_items
    except (Exception, psycopg2.DatabaseError) as error:
        raise error


def add_item(items_payload: dict):
    try:
        # Connect to DB
        conn = connect_to_db()
        # Using context manager to auto close cursor
        with conn.cursor() as db:
            insert_sql = f"INSERT INTO todo_list.todo_items(title, description) VALUES ('{items_payload['title']}', '{items_payload['description']}');"
            print(insert_sql)
            db.execute(insert_sql)
            # Commit context
            conn.commit()
        return True
    except (Exception, psycopg2.DatabaseError) as error:
        raise error


# Thought about adding more CRUD functionality
# def update_item(iscompleted: bool, item_id: int):
#     try:
#         conn = connect_to_db()
#         with conn.cursor() as db:
#             update_sql = """ UPDATE todo_list.todo_items
#                             SET isCompleted=%s, updated_at=now()
#                             WHERE id=%s;"""
#             db.execute(
#                 update_sql,
#                 (
#                     iscompleted,
#                     item_id,
#                 ),
#             )
#         return True
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)


class FailedToConnectToDBException(Exception):
    """An exception raise when failing to connect to the database"""
