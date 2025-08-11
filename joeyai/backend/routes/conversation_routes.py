from flask import Blueprint, request, jsonify
from ..services.conversation_service import (
    create_conversation, list_conversations, rename_conversation, get_messages, ensure_tables
)

conversations_bp = Blueprint('conversations', __name__)

@conversations_bp.before_app_request
def setup_tables():
    ensure_tables()

@conversations_bp.route('/conversations', methods=['POST'])
def post_conversation():
    data = request.get_json(force=True) if request.is_json else {}
    title = data.get('title')
    convo = create_conversation(title)
    return jsonify(convo)

@conversations_bp.route('/conversations', methods=['GET'])
def get_conversations():
    return jsonify(list_conversations())

@conversations_bp.route('/conversations/<int:id>/messages', methods=['GET'])
def get_conversation_messages(id):
    return jsonify(get_messages(id))

@conversations_bp.route('/conversations/<int:id>', methods=['PATCH'])
def patch_conversation(id):
    data = request.get_json(force=True) if request.is_json else {}
    title = data.get('title')
    convo = rename_conversation(id, title)
    return jsonify(convo)
