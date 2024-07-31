#!/usr/bin/python3
"""
This script creates a simple web application using the
Flask framework that lists all states.
"""

from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def list_states():
    """
    Route to list all states.

    Fetches all states from the storage and passes them to
    the template for rendering.

    Returns:
        Rendered HTML template displaying the list of states.
    """
    states = storage.all(State).values()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def close_db(exc):
    """
    Remove the current SQLAlchemy session.

    This function is called automatically when the
    application context is torn down. It ensures that the
    SQLAlchemy session is properly closed.

    Args:
        exc (Exception): The exception that caused the
        teardown, if any.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
