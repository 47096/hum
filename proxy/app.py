from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route("/", methods=["POST", "GET", "OPTIONS"])
def proxy():
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Authorization, Content-Type, X-Provider",
    }

    if request.method == "OPTIONS":
        return ("", 204, headers)

    if request.method == "GET":
        return Response('{"status":"ok"}', status=200, headers={**headers, "Content-Type": "application/json"})

    provider = request.headers.get("X-Provider", "gmi")
    api_key = request.headers.get("Authorization", "").replace("Bearer ", "")

    if not api_key:
        return Response('{"error":"Missing API key"}', status=401, headers={**headers, "Content-Type": "application/json"})

    if provider == "minimax":
        url = "https://api.minimax.chat/v1/music_generation"
    else:
        url = "https://api.gmicloud.ai/api/v1/requests"

    api_headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = request.get_json(silent=True)
    if not body:
        return Response('{"error":"Missing body"}', status=400, headers={**headers, "Content-Type": "application/json"})

    try:
        resp = requests.post(url, json=body, headers=api_headers, timeout=600)
        return Response(resp.text, status=resp.status_code, headers={**headers, "Content-Type": "application/json"})
    except Exception as e:
        return Response(f'{{"error":"{e}"}}', status=500, headers={**headers, "Content-Type": "application/json"})
