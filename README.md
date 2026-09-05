# Hum — AI Music Generator

Generate songs and instrumentals using AI. Chat with the AI to create style prompts and lyrics, then generate music.

**Live app:** [https://47096.github.io/hum/](https://47096.github.io/hum/)

## How it works

```
Browser → Render proxy (CORS) → GMI Cloud / MiniMax API → MP3
```

## Features

- **Chat-based creation** — describe your song in natural language
- **12 genre templates** — Pop, Hip-Hop, R&B, Latin, EDM, Afrobeats, Rock, K-Pop, Country, Lo-fi, Jazz, Soul
- **Image-to-song** — upload an image and AI generates style/lyrics based on the visual mood
- **YouTube links** — paste a YouTube URL to create a song inspired by it
- **Song & Instrumental modes** — toggle between songs with lyrics and music-only tracks
- **Click-to-edit** — edit title, style, and lyrics inline in the chat
- **AI-generated titles** — AI names each track automatically
- **Embedded lyrics** — downloaded MP3s include lyrics for Apple Music
- **Song history** — saved locally, replay or delete past generations
- **Download all** — export all tracks at once
- **Customizable** — sample rate, bitrate, format (MP3/WAV/PCM), BPM, key, mode

## Setup

### 1. Get an API key

**GMI Cloud (free during campaign):**
- Sign up at [console.gmicloud.ai](https://console.gmicloud.ai)
- Go to **API Keys** and create one

**MiniMax (paid):**
- Sign up at [platform.minimax.io](https://platform.minimax.io)
- Go to **API Keys** and create one

### 2. Deploy the CORS proxy (Render)

The proxy is in the `proxy/` folder and deploys automatically via Render Blueprint.

1. Go to [render.com](https://render.com) and sign up with GitHub
2. Click **"New"** → **"Blueprint"**
3. Connect this repo
4. Click **"Apply"** — Render will deploy the proxy automatically
5. Copy the URL (e.g. `https://hum-proxy.onrender.com`)

**Why Render?**
- No timeout limits (handles long-running generation)
- Free tier: 750 hours/month, no credit card required

### 3. Host the frontend on GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages → Source → Deploy from branch**
3. Select `main` branch, `/ (root)` folder
4. Your site will be live at `https://<username>.github.io/hum/`

### 4. Configure in browser

1. Open the GitHub Pages URL
2. Select your provider (GMI Cloud or MiniMax)
3. Paste your API key
4. Paste your Render proxy URL
5. Done — generate songs from any device

## Local development

For local use, run the Python proxy:

```bash
cd proxy
pip install -r requirements.txt
python app.py
# Open http://localhost:8765
```

## Files

| File | Purpose |
|------|---------|
| `index.html` | Frontend app (single file, no build step) |
| `proxy/app.py` | CORS proxy with lyrics embedding (Python/Flask) |
| `proxy/requirements.txt` | Python dependencies |
| `render.yaml` | Render deployment config |
