#!/usr/bin/python3
"""
This module contains the city route
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State
from models.state import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def citites(state_id):
    """
    state_id: string - the state id
    Return:
    a json representation of the city
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all("City")
    cities_list = []
    for city in cities.values():
        if city.state_id == state_id:
            cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city(city_id):
    """
    Return:
    a json representation of the city
    """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """delete city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """create city object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data.update({"state_id": state_id})
    new_city = City(**data)
    new_city.save()
    resp = jsonify(new_city.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """update a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
