#!/usr/bin/python3
"""
Handles REST API actions for Review
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify([review.to_dict() for review in place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a specific Review object by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a specific Review object by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review object"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    if 'user_id' not in get_request.json():
        return abort(400, 'Missing user_id')
    if 'text' not in request.get_json():
        return abort(400, 'Missing text')
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    data = request.get_json()
    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a specific Review object by its ID"""
    review = storage.get(Review, review_id)
    if review is None:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
