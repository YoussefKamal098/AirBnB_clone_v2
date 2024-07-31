#!/usr/bin/python3
"""
This script creates a simple web application using the Flask framework.
The application listens on all network interfaces (`0.0.0.0`) on port `5000`
and returns a "Hello HBNB!" message when accessed via the root URL (`/`).
from flask import Flask
"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
