#!/usr/bin/env python3
"""
endpoints.py - API endpoints
"""

from flask import Blueprint, render_template, request, jsonify
import json
import mock

endpoints = Blueprint("endpoints", __name__)


@api.route('/recommendations', methods=['GET'])
def get_recs():
    response = {}
    email = request.json.get('email')
    password = request.json.get('password')
    return jsonify(response)


