from flask import Flask, render_template, request, redirect
from os import getenv
import requests

app = Flask(__name__)


# Testing the route
@app.route("/")
def default():
    return "Hello World! Testing application"


@app.route("/list")
def index():
    """Render the index page that by default displays a list of ToDo items"""

    # concatenating api url
    # Could create multiple API URLs in the env for specific calls ie. getenv("GET_ALL_ITEMS_URL")
    get_all_url = getenv("API_URL") + "/api/items"

    # get request for data
    list_of_items = requests.get(url=get_all_url, timeout=30).json()

    return render_template("index.html", title="My ToDo List", data=list_of_items)


@app.route("/add_item", methods=["GET"])
def add_item_view():
    """Render the add item view"""
    return render_template("add_item.html", title="Add Item")


@app.route("/add_item", methods=["POST"])
def add_item():
    """Post the data to the API endpoint and redirect to the index view (back to the list)"""

    title = request.form["title"]
    description = request.form["description"]

    # concatenate api endpoint with f-string
    create_url = f"/api/create/{title}/{description}"
    add_item_url = getenv("API_URL") + create_url

    # post data to api endpoint
    requests.post(url=add_item_url, timeout=30)
    return redirect("/list")


if __name__ == "__main__":
    app.run(debug=True)
