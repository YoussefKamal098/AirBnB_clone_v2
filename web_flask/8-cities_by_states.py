#!/usr/bin/python3
"""
This script sets up a Flask web application that retrieves and
displays states and their associated cities from a database. It defines a
route (/cities_by_states) that queries the database for all states and renders
them using an HTML template (8-cities_by_states.html). Additionally,
it includes a teardown function to close the database connection after
each request. The application runs on host 0.0.0.0 and port 5000
with debugging enabled.
"""

from flask import Flask, render_template

from models import storage
from models.state import State

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def cities_by_states():
    """
    Route to list all states.

    Fetches all states from the storage and passes them to
    the template for rendering.

    Returns:
        Rendered HTML template displaying the list of states.
    """
    states = storage.all(State).values()
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def close_db(exc):
    """
    Remove the current SQLAlchemy session.

    This function is called automatically when the
    application context is torn down. It ensures that the
    SQLAlchemy session is properly closed.

    Args:
        exc (Exception): The exception that caused the teardown, if any.
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
