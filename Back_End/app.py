from flask import Flask
from db import get_all_items, add_item

app = Flask(__name__)


# Test for the route
@app.route("/")
def default():
    return "Hello World! Test api"


@app.route("/api/items", methods=["GET"])
def get_items() -> list:
    """Get all ToDo items in list format"""
    try:
        # Get data from database
        list_of_items = get_all_items()
        if not list_of_items:
            return "No data to retrieve, please create records", 404

        # map data to how we want it for the front end
        # doing mapping on the api layer as to not have functionality on front-end app
        mapped_data = [
            dict(zip(["title", "description"], row)) for row in list_of_items
        ]

        return mapped_data
    except:
        raise FailedGetAllItemsException, 400


@app.route("/api/create/<title>/<description>", methods=["POST"])
def create_items(title, description):
    """Create a ToDo item"""
    # Create variable how we want the data to be inserted
    new_item = {"title": title, "description": description}
    # Add to Database
    try:
        add_item(new_item)
        return "success", 200
    except:
        raise FailedCreateItemException, 400


# Thought about adding more CRUD functionality
# @app.route("/api/update/item_id/iscompleted", methods=["POST"])
# def update_item(item_id, iscompleted):
#     # Update record in database
#     try:
#         update_item(iscompleted, item_id)
#         return "success", 200
#     except:
#         return "Custom Error"


class FailedGetAllItemsException(Exception):
    """An exception raised when failing to get all items"""


class FailedCreateItemException(Exception):
    """An exception raised when failing to create a todo item"""


if __name__ == "__main__":
    app.run(debug=True)
