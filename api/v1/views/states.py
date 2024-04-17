#!/usr/bin/python3
"""
This module contains the states route
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states():
    """
    :return:
    Return:
    a json representation of all states
    """

    states = storage.all("State")
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())

    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state(state_id):
    """
    :param state_id:
    :return:
    state_id: string - the state id
    Return:
    a json representation of the state
    """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """
    :param state_id:
    :return:
    state_id: string - the state id
    Return:
    a json representation of the state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    :return:
    Return:
    a json representation of the state
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")

    new_state = State(**data)
    storage.save()
    resp = jsonify(new_state.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """update a state object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
