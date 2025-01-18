from flask import Blueprint, request, jsonify
from app.services.syntactic_search import syntactic_search
import json

syntactic_search_bp = Blueprint('syntactic_search', __name__)

# Load the service registry
with open('data/servio_data.json', 'r') as f:
    service_registry = json.load(f)

@syntactic_search_bp.route('/', methods=['POST'])
def search():
    data = request.json
    query = data.get('query', '')
    field = data.get('field', 'func_name')
    top_n = data.get('top_n', 5)

    results = syntactic_search(query, service_registry, field, top_n)
    return jsonify(results)
