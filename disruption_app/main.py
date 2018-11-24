#!/usr/bin/env python3
"""
main.py - Run the complete application
"""

from app import app, db
from views import views
from models import *

db.create_tables()
app.register_blueprint(views)


def run():
    app.run(host='0.0.0.0', port=5000, debug=True)

if __name__ == '__main__':
    run()
