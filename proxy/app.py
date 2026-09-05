from flask import Flask, request, Response
import requests
import json
import logging
import traceback
from mutagen.id3 import ID3, USLT
from mutagen.mp3 import MP3
import io

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
    return "https://api.gmi-serving.com/v1/chat/completions"

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
            "Authorization": f"Bearer {api_key}",
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

@app.route("/download", methods=["GET", "OPTIONS"])
def download_proxy():
    try:
        if request.method == "OPTIONS":
            return ("", 204, CORS_HEADERS)

        url = request.args.get("url")
        lyrics = request.args.get("lyrics", "")
        if not url:
            return cors_response(json.dumps({"error": "Missing url parameter"}), 400)

        logger.info(f"Download proxy: {url}")
        resp = requests.get(url, timeout=60)

        if resp.status_code != 200:
            return Response(resp.content, status=resp.status_code, headers={
                "Access-Control-Allow-Origin": "*",
                "Content-Type": "application/json",
            })

        audio_data = resp.content

        # Embed lyrics if provided
        if lyrics and url.lower().endswith(".mp3"):
            try:
                audio_file = io.BytesIO(audio_data)
                audio_file.name = "track.mp3"

                # Try to add ID3 tags
                try:
                    tags = ID3(audio_file)
                except:
                    tags = ID3()

                # Add lyrics as USLT frame (Unsynchronized Lyrics)
                tags.add(USLT(
                    encoding=3,  # UTF-8
                    lang="eng",
                    desc="",
                    text=lyrics
                ))

                # Write tags back to audio data
                audio_file_out = io.BytesIO()
                tags.save(audio_file)
                audio_file.seek(0)

                # Re-read with mutagen to apply tags
                mp3 = MP3(audio_file)
                mp3.tags = tags
                mp3.save(audio_file)

                audio_file.seek(0)
                audio_data = audio_file.read()
                logger.info(f"Embedded lyrics ({len(lyrics)} chars)")
            except Exception as e:
                logger.warning(f"Failed to embed lyrics: {e}")
                # Continue without lyrics — don't fail the download

        # Return the audio with CORS headers
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "audio/mpeg",
            "Content-Length": str(len(audio_data)),
        }

        return Response(audio_data, status=200, headers=headers)

    except Exception as e:
        logger.error(f"Download error: {e}\n{traceback.format_exc()}")
        return cors_response(json.dumps({"error": str(e)}), 500)

@app.route("/voice-clone", methods=["POST", "OPTIONS"])
def voice_clone():
    try:
        if request.method == "OPTIONS":
            return ("", 204, CORS_HEADERS)

        api_key = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not api_key:
            return cors_response(json.dumps({"error": "Missing API key"}), 401)

        body = request.get_json(silent=True)
        if not body:
            return cors_response(json.dumps({"error": "Missing body"}), 400)

        audio_base64 = body.get("audio")
        name = body.get("name", "My Voice")

        if not audio_base64:
            return cors_response(json.dumps({"error": "Missing audio data"}), 400)

        # Remove data URL prefix if present
        if "," in audio_base64:
            audio_base64 = audio_base64.split(",", 1)[1]

        # Decode base64 audio
        import base64
        audio_bytes = base64.b64decode(audio_base64)

        # Step 1: Upload audio file via GMI Cloud
        upload_url = "https://console.gmicloud.ai/api/v1/ie/requestqueue/apikey/requests/voice/upload"
        upload_headers = {
            "Authorization": f"Bearer {api_key}",
        }
        upload_files = {
            "file": ("voice.mp3", audio_bytes, "audio/mpeg"),
        }
        upload_data = {
            "purpose": "voice_clone",
        }

        logger.info(f"Voice clone upload: name={name}, audio_size={len(audio_bytes)}")
        upload_resp = requests.post(upload_url, headers=upload_headers, files=upload_files, data=upload_data, timeout=60)
        logger.info(f"Upload response: {upload_resp.status_code} {upload_resp.text[:200]}")

        if upload_resp.status_code != 200:
            return cors_response(upload_resp.text, upload_resp.status_code)

        upload_result = upload_resp.json()
        file_id = upload_result.get("file_id") or upload_result.get("file", {}).get("file_id")

        if not file_id:
            return cors_response(json.dumps({"error": "Failed to upload audio file", "response": upload_result}), 500)

        # Step 2: Clone voice via GMI Cloud
        clone_url = "https://console.gmicloud.ai/api/v1/ie/requestqueue/apikey/requests/voice/clone"
        clone_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        # Generate a unique voice_id
        import uuid
        voice_id = "hum-" + str(uuid.uuid4())[:8]

        clone_body = {
            "file_id": file_id,
            "voice_id": voice_id,
        }

        logger.info(f"Voice clone request: file_id={file_id}, voice_id={voice_id}")
        clone_resp = requests.post(clone_url, headers=clone_headers, json=clone_body, timeout=60)
        logger.info(f"Clone response: {clone_resp.status_code} {clone_resp.text[:200]}")

        if clone_resp.status_code != 200:
            return cors_response(clone_resp.text, clone_resp.status_code)

        clone_result = clone_resp.json()

        # Return voice_id to the frontend
        result = {
            "voice_id": voice_id,
            "name": name,
            "status": "success"
        }

        return cors_response(json.dumps(result), 200)

    except Exception as e:
        logger.error(f"Voice clone error: {e}\n{traceback.format_exc()}")
        return cors_response(json.dumps({"error": str(e)}), 500)
