from flask import Blueprint, request, jsonify
from backend.services.llm_engine import LLMEngine

llm_api = Blueprint('llm_api', __name__)
llm_engine = LLMEngine()

@llm_api.route('/llm/status', methods=['GET'])
def get_llm_status():
    model_name = request.args.get('model', llm_engine.default_model)
    ready = llm_engine.is_llm_ready(model_name)
    return jsonify({
        "ollama_running": llm_engine.llm_enabled,
        "model_checked": model_name,
        "model_available": ready
    }), 200

@llm_api.route('/llm/generate', methods=['POST'])
def generate_llm_response():
    if not llm_engine.llm_enabled:
        return jsonify({"error": "LLM functionality is disabled (Ollama not running). Load an LLM model and try again."}), 503

    data = request.get_json()
    prompt = data.get('prompt')
    model = data.get('model', llm_engine.default_model)

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    response_text = llm_engine.generate_response(prompt, model)
    
    # Check if the response_text indicates an error from LLMEngine
    if "LLM functionality is disabled" in response_text or "not available in Ollama" in response_text or "Error generating response" in response_text:
        return jsonify({"error": response_text}), 503
    
    return jsonify({"response": response_text, "model_used": model}), 200
