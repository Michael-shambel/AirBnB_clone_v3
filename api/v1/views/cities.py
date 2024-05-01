#!/usr/bin/python3
"""
handles REST API actions for State
"""
from api.v1.views import app_views
from flask import jsonify
from flask import Flask
from flask import request
from flask import abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_states_cities(state_id):
    """handles states route"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        return abort(404)
    return jsonify([city.to_dict() for city in my_state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object."""
    my_city = storage.get(City, city_id)
    if my_city is None:
        return abort(404)
    return (my_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object:"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        return abort(404)
    storage.delete(my_city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        return abort(400, 'Missing name')
    data = request.get_json()
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
