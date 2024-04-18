#!/usr/bin/python3
"""
This module contains the reviews route
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def reviews(place_id):
    """get reviews objects"""

    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = storage.all("Review")
    reviews_list = []
    for review in reviews.values():
        if review.place_id == place_id:
            reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def review_id(review_id):
    """get review object"""

    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("reviews/<review_id>",
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """delete review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def create_reviews(place_id):
    """create review object"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()
    resp = jsonify(new_review.to_dict())
    resp.status_code = 201

    return resp


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """update a review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at",
                       "user_id", "Place_id"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
