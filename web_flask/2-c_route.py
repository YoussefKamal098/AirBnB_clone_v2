#!/usr/bin/python3
"""
This script creates a simple web application using the Flask framework.
"""

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    return 'HBNB'


@app.route('/c/<text>')
def c_is_fun(text):
    return f'C {text}'.replace('_', ' ')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
