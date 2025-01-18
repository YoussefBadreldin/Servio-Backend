from flask import Blueprint, request, jsonify
from app.services.semantic_search import semantic_search
import json

semantic_search_bp = Blueprint('semantic_search', __name__)

# Load the service registry
with open('data/servio_data.json', 'r') as f:
    service_registry = json.load(f)

@semantic_search_bp.route('/', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    aspects = data.get('aspects', ['func_name', 'docstring'])
    top_n = data.get('top_n', 5)

    results = semantic_search(query, service_registry, aspects, top_n)
    return jsonify(results)
