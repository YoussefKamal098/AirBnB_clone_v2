#!/usr/bin/python3
"""
Flask web application to display a list of states and
details of a specific state.
"""

from flask import Flask
from flask import render_template

from models.state import State
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/states")
def list_states():
    """
    Route to list all states.

    Fetches all states from the storage and passes them to
    the template for rendering.

    Returns:
        Rendered HTML template displaying the list of states.
    """
    states = storage.all(State)
    return render_template("9-states.html", states=states)


@app.route("/states/<string:id>")
def state_id(id):
    """
    Route to display details of a specific state.

    Fetches the state with the given ID from the storage and
    passes it to the template for rendering. If the state is
    not found, an empty template is rendered.

    Args:
        id (str): The ID of the state to be displayed.

    Returns:
        Rendered HTML template displaying the state
        details if found, otherwise an empty template.
    """
    state = storage.find("State", id)
    if not state:
        return render_template("9-states.html")

    return render_template("9-states.html", state=state)


@app.teardown_appcontext
def teardown(exc):
    """
    Remove the current SQLAlchemy session.

    This function is called automatically when the
    application context is torn down. It ensures that the
    SQLAlchemy session is properly closed.

    Args:
        exc (Exception): The exception that caused the teardown, if any.
    """
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
