#!/usr/bin/python3
"""
This module contains the city route
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def places(city_id):
    """get places objects"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = storage.all("Place")
    places_list = []
    for place in places.values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def place(place_id):
    """get place object"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """delete place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """create place object"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if "user_id" not in data:
        abort(400, "Missing name")
    if "name" not in data:
        abort(400, "Missing name")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    resp = jsonify(new_place.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """update a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
