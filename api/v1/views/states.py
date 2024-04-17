#!/usr/bin/python3
"""
This module contains the states route
"""
from flask import jsonify, abort
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
