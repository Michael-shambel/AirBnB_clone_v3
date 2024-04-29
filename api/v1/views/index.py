#!/usr/bin/python3
"""
create flask api
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def get_status():
    """status of the API."""
    return jsonify({"status": "OK"})
