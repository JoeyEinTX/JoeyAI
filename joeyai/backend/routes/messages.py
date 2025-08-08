
from flask import Blueprint, request, jsonify
from joeyai.backend.services.messages import list_messages, add_message

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/projects/<int:id>/messages', methods=['GET'])
def get_messages(id):
	limit = int(request.args.get('limit', 200))
	order = request.args.get('order', 'asc')
	return jsonify(list_messages(id, limit, order))

@messages_bp.route('/projects/<int:id>/message', methods=['POST'])
def post_message(id):
	from ..config import Config
	from joeyai.backend.services.ollama import generate
	from joeyai.backend.services.messages import list_messages, add_message
	data = request.get_json(force=True)
	role = data.get('role')
	content = data.get('content')
	# Store user message
	user_msg = add_message(id, role, content)
	# Compose prompt from last ~20 messages
	history = list_messages(id, limit=20, order='asc')
	prompt = "\n".join([f"{m['role']}: {m['content']}" for m in history])
	# Call Ollama
	reply_text = generate(Config.DEFAULT_MODEL, prompt)
	# Store assistant message
	add_message(id, 'assistant', reply_text)
	return jsonify({"reply": reply_text})
