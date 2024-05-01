#!/usr/bin/python3
"""
Handles all RESTFul API actions for state objects
"""
from flask import Flask, jsonify, request, abort
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """Retrievs the list of all state objects"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a state object"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a State object"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create a state"""
    data = request.get_json()
    if not request.get_json():
        abort(400, 'Not a JSON')

    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a state object"""
    state_found = storage.get(State, state_id)
    data = request.get_json()
    if not request.get_json():
        abort(400, 'Not a JSON')
    if state_found is None:
        abort(404)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state_found, key, value)
    state_found.save()
    return jsonify(state_found.to_dict()), 200
