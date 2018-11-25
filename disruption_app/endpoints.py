#!/usr/bin/env python3
"""
endpoints.py - API endpoints
"""

from flask import Blueprint, render_template, request, jsonify
import json
import models
import tinder_api
from config import DevelopmentConfig as Config
import extract
import clean
endpoints = Blueprint("endpoints", __name__)


@endpoints.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')
    Config.FB_USERNAME = email
    Config.FB_PASSWORD = password
    Config.save()


@endpoints.route('/recommendations', methods=['GET'])
def get_recs():
    tinder = tinder_api.Client(username=Config.FB_USERNAME, password=Config.FB_PASSWORD)
    recommendations = tinder.get_recs().get('data').get('results')
    for i in range(len(recommendations)):
        clean_recs = clean.Clean(recommendations[i]['user'])
        extract.Extract(clean_recs)
    return jsonify(recommendations)
