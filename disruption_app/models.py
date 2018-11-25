#!/usr/bin/env python3
"""
models.py - Package level variables
"""

import os
import json


def get_mock_data():
    basedir = os.path.abspath(os.path.dirname(__file__))
    mock_data_path = os.path.join(basedir, 'static/example.json')
    with open(mock_data_path, encoding='utf-8') as read_file:
        mock_data = json.loads(read_file.read())
    return mock_data
