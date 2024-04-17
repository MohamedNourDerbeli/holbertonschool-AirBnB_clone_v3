#!/usr/bin/python3
"""
This module contains the status route
"""
from flask import jsonify
from . import app_views
from models import storage


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Return the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """
    Return the number of objects by type
    """
    total_objects = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    return jsonify(total_objects)

@app_views.errorhandler(404)
def not_found(error):
    """
    Return a 404 error
    """
    return jsonify({"error": "Not found"}), 404
