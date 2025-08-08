
from flask import Blueprint, request, jsonify
from joeyai.backend.services.projects import list_projects, create_project, rename_project, delete_project

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/projects', methods=['GET'])
def get_projects():
	limit = int(request.args.get('limit', 100))
	return jsonify(list_projects(limit))

@projects_bp.route('/projects', methods=['POST'])
def post_project():
	data = request.get_json(force=True)
	title = data.get('title') if data else None
	return jsonify(create_project(title))

@projects_bp.route('/projects/<int:id>', methods=['PATCH'])
def patch_project(id):
	data = request.get_json(force=True)
	title = data.get('title')
	return jsonify(rename_project(id, title))

@projects_bp.route('/projects/<int:id>', methods=['DELETE'])
def delete_project_route(id):
	return jsonify(delete_project(id))
