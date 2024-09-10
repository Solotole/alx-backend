#!/usr/bin/env python3
"""Flask app development"""
from flask import Flask, render_template
from flask_babel import Babel
from typing import List


app = Flask(__name__)


class Config:
    """a basic configuring class"""
    LANGUAGES: List = ['en', 'fr']
    BABEL_DEFAULT_LOCALE: str = 'en'
    BABEL_DEFAULT_TIMEZONE: str = 'UTC'


app.config.from_object(Config)
babel = Babel(app)


@app.route('/')
def index():
    """index python file"""
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run()
