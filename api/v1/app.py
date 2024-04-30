#!/usr/bin/python3
"""
it is time to start your API!
"""
import os
from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import jsonify


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Handles teardown of the app."""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handler for 404 error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)