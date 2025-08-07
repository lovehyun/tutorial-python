from flask import Blueprint, request, jsonify
from services.chatbot_service6_history import handle_chat6
from services.chatbot_service7_langchain import handle_chat7
from services.chatbot_service8_langchain2_memchain import handle_chat8

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("", methods=["POST"])
@chatbot_bp.route("/", methods=["POST"])
def chat():
    data = request.get_json() or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "질문이 없습니다."}), 400

    try:
        # result = handle_chat6(question)
        # result = handle_chat7(question)
        result = handle_chat8(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
