#!/usr/bin/python3
"""Application intialisation module"""

from flask import Flask
from os import getenv
from flask import Flask, jsonify, make_response
from src import storage
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger
from .docs.swagger_template import swagger_template
from .config import config
import logging


# create the app instance
app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['DEBUG'] = config.DEBUG
app.config['MAX_CONTENT_LENGTH'] = config.MAX_FILE_SIZE

# Setup Swagger
swagger = Swagger(app, template=swagger_template)

# Setup CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

@app.errorhandler(404)
def page_not_found(e):
    """json 404 page"""
    return make_response(jsonify({"error": "Resource (endpoint Not) found"}), 404)

@app.teardown_appcontext
def teardown(self) -> None:
    """Close the storage session"""
    storage.database.close()

@app.errorhandler(400)
def handle_bad_request(e):
    """json 400 page"""
    return (jsonify({'error': 'Bad request'}))

@app.route('/health')
def health_check():
    """Health check endpoint for frontend"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Object Counting API is running',
        'pipeline_available': True,
        'database': 'connected'
    })

# setup the API and the endpoints
api = Api(app)
from .api.views.inputs import *
from .api.views.object_types import *
from .api.views.outputs import *
from .api.views.monitoring import PerformanceMetrics, ObjectTypeStats, DatabaseStats, ResetStats, SystemHealth
from .api.views.batch_processing import BatchProcessing, BatchStatus

api.add_resource(InputList, '/api/count')
# Add count-all endpoint for auto-detection
app.add_url_rule('/api/count-all', 'count_all_objects', InputList().count_all_objects, methods=['POST'])
# api.add_resource(InputSingle, '/api/input/<id>')
api.add_resource(ObjectTypeList, '/api/object-types')
api.add_resource(ObjectTypeSingle, '/api/object/<id>')
api.add_resource(OutputList, '/api/results')
api.add_resource(OutputSingle, '/api/correct/<id>')

# Performance monitoring endpoints
api.add_resource(PerformanceMetrics, '/api/performance/metrics')
api.add_resource(ObjectTypeStats, '/api/performance/object-types')
api.add_resource(DatabaseStats, '/api/performance/database')
api.add_resource(ResetStats, '/api/performance/reset')
api.add_resource(SystemHealth, '/api/performance/health')

# Batch processing endpoints
api.add_resource(BatchProcessing, '/api/batch/process')
api.add_resource(BatchStatus, '/api/batch/status')

# run this file to run the app
if __name__ == "__main__":
    logging.info(f"Starting AI Object Counting Application in {config.ENV} mode")
    logging.info(f"Server will run on {config.HOST}:{config.PORT}")
    logging.info(f"Debug mode: {config.DEBUG}")
    logging.info(f"Database: {config.DATABASE_TYPE}")
    logging.info(f"Media directory: {config.MEDIA_DIRECTORY}")
    
    app.run(
        host=config.HOST, 
        port=config.PORT, 
        threaded=True, 
        debug=config.DEBUG
    )
