from flask import Blueprint, request, jsonify
from ..services.conversation_service import add_message
from ..services.ollama_service import get_reply

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations/<int:id>/message', methods=['POST'])
def post_message(id):
    data = request.get_json(force=True) if request.is_json else {}
    content = data.get('content')
    model = data.get('model')
    temperature = data.get('temperature')
    max_tokens = data.get('max_tokens')
    system = data.get('system')
    # Step a: add user message
    add_message(id, 'user', content)
    # Step b: get assistant reply
    try:
        reply = get_reply(content, model=model, temperature=temperature, max_tokens=max_tokens, system=system)
    except Exception:
        reply = "Model offline"
    # Step c: add assistant message
    add_message(id, 'assistant', reply)
    # Step d: return reply
    return jsonify({"reply": reply})
