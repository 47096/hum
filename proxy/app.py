from flask import Flask, request, Response
import requests
import json
import logging
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type, X-Provider",
    "Content-Type": "application/json",
}

def cors_response(data, status=200):
    return Response(data, status=status, headers=CORS_HEADERS)

def get_api_url(provider, path=""):
    if provider == "minimax":
        return "https://api.minimax.chat/v1/music_generation"
    return f"https://console.gmicloud.ai/api/v1/ie/requestqueue/apikey/requests{path}"

def get_llm_url():
    return "https://api.minimax.chat/v1/text/chatcompletion_v2"

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}\n{traceback.format_exc()}")
    return cors_response(json.dumps({"error": str(e)}), 500)

@app.route("/llm", methods=["POST", "OPTIONS"])
def llm_proxy():
    try:
        if request.method == "OPTIONS":
            return ("", 204, CORS_HEADERS)

        api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not api_key:
            return cors_response(json.dumps({"error": "Missing API key"}), 401)

        body = request.get_json(silent=True)
        if not body:
            return cors_response(json.dumps({"error": "Missing body"}), 400)

        url = get_llm_url()
        api_headers = {
            "Authorization": api_key,
            "Content-Type": "application/json",
        }

        logger.info(f"LLM POST {url} api_key_len={len(api_key)}")
        resp = requests.post(url, json=body, headers=api_headers, timeout=60)
        logger.info(f"LLM Response: {resp.status_code} {resp.text[:200]}")
        return cors_response(resp.text, resp.status_code)

    except Exception as e:
        logger.error(f"LLM error: {e}\n{traceback.format_exc()}")
        return cors_response(json.dumps({"error": str(e)}), 500)

@app.route("/", methods=["POST", "GET", "OPTIONS"])
@app.route("/<path:request_id>", methods=["GET", "OPTIONS"])
def proxy(request_id=""):
    try:
        if request.method == "OPTIONS":
            return ("", 204, CORS_HEADERS)

        provider = request.headers.get("X-Provider", "gmi")
        api_key = request.headers.get("Authorization", "").replace("Bearer ", "")

        logger.info(f"Request: {request.method} provider={provider} key_len={len(api_key)}")

        if not api_key:
            return cors_response(json.dumps({"error": "Missing API key"}), 401)

        api_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        if request.method == "GET":
            url = get_api_url(provider, f"/{request_id}" if request_id else "")
            logger.info(f"GET {url}")
            resp = requests.get(url, headers=api_headers, timeout=30)
            logger.info(f"Response: {resp.status_code}")
            return cors_response(resp.text, resp.status_code)

        # POST
        url = get_api_url(provider)
        body = request.get_json(silent=True)
        if not body:
            return cors_response(json.dumps({"error": "Missing body"}), 400)

        logger.info(f"POST {url} body_keys={list(body.keys())}")
        resp = requests.post(url, json=body, headers=api_headers, timeout=600)
        logger.info(f"Response: {resp.status_code} len={len(resp.text)}")
        return cors_response(resp.text, resp.status_code)

    except Exception as e:
        logger.error(f"Request error: {e}\n{traceback.format_exc()}")
        return cors_response(json.dumps({"error": str(e)}), 500)
