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

        # Voice clone via GMI Cloud
        # Endpoint: POST /api/v1/ie/requestqueue/apikey/requests
        # Model: minimax-audio-voice-clone-speech-2.6-hd

        # Step 1: Upload audio to temporary file host to get a public URL
        import uuid
        voice_id = "hum-" + str(uuid.uuid4())[:8]

        logger.info(f"Uploading audio to temporary host: name={name}, audio_size={len(audio_bytes)}")
        try:
            # Use 0x0.st for temporary file hosting
            upload_resp = requests.post(
                "https://0x0.st",
                files={"file": ("voice.mp3", audio_bytes, "audio/mpeg")},
                timeout=30
            )
            logger.info(f"Upload response: {upload_resp.status_code} {upload_resp.text[:200]}")

            if upload_resp.status_code != 200:
                return cors_response(json.dumps({"error": f"Upload failed with status {upload_resp.status_code}: {upload_resp.text[:100]}"}), 500)

            # 0x0.st returns the URL directly as plain text
            audio_url = upload_resp.text.strip()
            if not audio_url.startswith("http"):
                return cors_response(json.dumps({"error": f"Invalid URL returned: {audio_url}"}), 500)

            logger.info(f"Audio uploaded: {audio_url}")
        except Exception as e:
            logger.error(f"Upload error: {e}")
            return cors_response(json.dumps({"error": f"Failed to upload audio: {str(e)}"}), 500)

        # Step 2: Call voice clone API with the public URL
        clone_url = "https://console.gmicloud.ai/api/v1/ie/requestqueue/apikey/requests"
        clone_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        clone_body = {
            "model": "minimax-audio-voice-clone-speech-2.6-hd",
            "payload": {
                "text": "Hello, this is a test of the cloned voice.",
                "source_audio": audio_url,
                "voice_id": voice_id
            }
        }

        logger.info(f"Voice clone request: voice_id={voice_id}, audio_url={audio_url}")
        try:
            clone_resp = requests.post(clone_url, headers=clone_headers, json=clone_body, timeout=120)
            logger.info(f"Clone response: {clone_resp.status_code} {clone_resp.text[:500]}")

            if clone_resp.status_code != 200:
                return cors_response(clone_resp.text, clone_resp.status_code)

            clone_result = clone_resp.json()
        except requests.exceptions.JSONDecodeError:
            logger.error(f"Failed to parse clone response as JSON: {clone_resp.text}")
            return cors_response(json.dumps({"error": "Invalid response from voice clone API"}), 500)
        except Exception as e:
            logger.error(f"Clone request error: {e}")
            return cors_response(json.dumps({"error": f"Voice clone request failed: {str(e)}"}), 500)

        # Check if request was successful
        status = clone_result.get("status", "")
        if status == "failed":
            error_msg = clone_result.get("error", "Voice clone failed")
            return cors_response(json.dumps({"error": error_msg}), 400)

        # For async API, we need to poll for the result
        request_id = clone_result.get("request_id")
        if request_id:
            # Poll for completion
            import time
            poll_url = f"{clone_url}/{request_id}"
            for _ in range(30):  # Poll for up to 30 seconds
                time.sleep(2)
                poll_resp = requests.get(poll_url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
                if poll_resp.status_code == 200:
                    poll_result = poll_resp.json()
                    poll_status = poll_result.get("status", "")
                    if poll_status == "success":
                        # Extract voice_id from outcome
                        voice_id = poll_result.get("outcome", {}).get("voice_id", "")
                        if not voice_id:
                            voice_id = "cloned-" + str(hash(name))[:8]
                        result = {
                            "voice_id": voice_id,
                            "name": name,
                            "status": "success"
                        }
                        return cors_response(json.dumps(result), 200)
                    elif poll_status == "failed":
                        error_msg = poll_result.get("error", "Voice clone failed")
                        return cors_response(json.dumps({"error": error_msg}), 400)

        # If we get here, return the initial response
        result = {
            "voice_id": clone_result.get("outcome", {}).get("voice_id", "cloned-voice"),
            "name": name,
            "status": "success"
        }

        return cors_response(json.dumps(result), 200)

    except Exception as e:
        logger.error(f"Voice clone error: {e}\n{traceback.format_exc()}")
        return cors_response(json.dumps({"error": str(e)}), 500)
