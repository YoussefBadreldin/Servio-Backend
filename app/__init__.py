from flask import Flask
from flask_cors import CORS
from app.routes.semantic_search import semantic_search_bp
from app.routes.syntactic_search import syntactic_search_bp

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Register Blueprints
    app.register_blueprint(semantic_search_bp, url_prefix='/api/semantic')
    app.register_blueprint(syntactic_search_bp, url_prefix='/api/syntactic')

    return app
