from flask import Flask, request, Response
import requests

app = Flask(__name__)

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type, X-Provider",
}

def get_api_url(provider, path=""):
    if provider == "minimax":
        return "https://api.minimax.chat/v1/music_generation"
    return f"https://console.gmicloud.ai/api/v1/ie/requestqueue/apikey/requests{path}"

@app.route("/", methods=["POST", "GET", "OPTIONS"])
@app.route("/<path:request_id>", methods=["GET", "OPTIONS"])
def proxy(request_id=""):
    if request.method == "OPTIONS":
        return ("", 204, CORS_HEADERS)

    provider = request.headers.get("X-Provider", "gmi")
    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")

    if not api_key:
        return Response('{"error":"Missing API key"}', status=401, headers={**CORS_HEADERS, "Content-Type": "application/json"})

    api_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    if request.method == "GET":
        url = get_api_url(provider, f"/{request_id}" if request_id else "")
        try:
            resp = requests.get(url, headers=api_headers, timeout=30)
            return Response(resp.text, status=resp.status_code, headers={**CORS_HEADERS, "Content-Type": "application/json"})
        except Exception as e:
            return Response(f'{{"error":"{e}"}}', status=500, headers={**CORS_HEADERS, "Content-Type": "application/json"})

    # POST
    url = get_api_url(provider)
    body = request.get_json(silent=True)
    if not body:
        return Response('{"error":"Missing body"}', status=400, headers={**CORS_HEADERS, "Content-Type": "application/json"})

    try:
        resp = requests.post(url, json=body, headers=api_headers, timeout=600)
        return Response(resp.text, status=resp.status_code, headers={**CORS_HEADERS, "Content-Type": "application/json"})
    except Exception as e:
        return Response(f'{{"error":"{e}"}}', status=500, headers={**CORS_HEADERS, "Content-Type": "application/json"})
