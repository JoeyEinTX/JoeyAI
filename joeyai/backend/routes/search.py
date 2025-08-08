
from flask import Blueprint, request, jsonify
from joeyai.backend.services.search import search_messages

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
	q = request.args.get('q', '')
	limit = int(request.args.get('limit', 100))
	return jsonify(search_messages(q, limit))
