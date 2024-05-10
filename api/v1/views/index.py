#!/usr/bin/python3
"""
This module contains the status route
"""
from flask import jsonify
from . import app_views
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def get_status():
    """
    Return the status of the API
    """
    return jsonify({"status": "OK"})
