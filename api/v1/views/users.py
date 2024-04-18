#!/usr/bin/python3
"""
This module contains the users route
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users():
    """list all users"""
    users = storage.all("User")
    users_list = []
    for user in users.values():
        users_list.append(user.to_dict())

    return jsonify(users_list)


@app_views.route("/users/<user_id>",
                 methods=["GET"], strict_slashes=False)
def user(user_id):
    """list user"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """delete user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """ create user"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")

    new_user = User(**data)
    new_user.save()
    resp = jsonify(new_user.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/users/<user_id>",
                 methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """update a user object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
