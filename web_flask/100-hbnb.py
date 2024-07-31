#!/usr/bin/python3
"""
This script creates a simple web application using the Flask framework.
"""

from flask import Flask
from flask import render_template

from models.state import State
from models.amenity import Amenity
from models.place import Place
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb')
def hbnb():
    """Displays the main HBnB filters HTML page."""
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()
    states = storage.all(State).values()
    return render_template(
        "100-hbnb.html",
        amenities=amenities,
        places=places,
        states=states
    )


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
    app.run(host="0.0.0.0", port=5000, debug=True)
