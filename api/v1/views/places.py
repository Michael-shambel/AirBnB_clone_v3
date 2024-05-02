#!/usr/bin/python3
"""
Create a new view for Place objects that handles
all default RESTFul API actions:
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        return abort(400, 'missing user_id')
    if 'name' not in request.get_json():
        return abort(400, 'Missing name')
    user_id = request.get_json['user_id']
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    data = request.get_json()
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    if not request.json:
        return abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
