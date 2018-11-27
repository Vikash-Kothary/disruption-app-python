#!/usr/bin/env python3
"""
app.py - Creates the flask web server
"""

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config


def create_app():
    """ 
    """
    app = Flask(__name__, static_folder='static', static_url_path='')
    app.config.from_object(config.DevelopmentConfig)
    return app


def create_db(app):
    """
    """
    def _init_db():
        with app.app_context():
            db.drop_all()
            db.create_all()

    def _save_util(user=None):
        if user:
            db.session.add(user)
        db.session.commit()

    def _clear_data():
        session = db.session
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

    db = SQLAlchemy()
    db.init_app(app)
    db.create_tables = _init_db
    db.save = _save_util
    db.clear_all = _clear_data
    return db


app = create_app()
db = create_db(app)


@app.route("/success")
def success():
    """Check if the Flask web server is working"""
    return "App is working"
