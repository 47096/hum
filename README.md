# AI Music — GMI Cloud

Generate songs from lyrics using MiniMax Music 3.0 via GMI Cloud or MiniMax APIs.

## How it works

```
Browser → Render proxy (CORS) → GMI Cloud / MiniMax API → MP3
```

## Setup

### 1. Get an API key

**GMI Cloud (free during campaign, ends Sep 6, 2026):**
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
5. Copy the URL (e.g. `https://ai-music-proxy.onrender.com`)

**Why Render instead of Cloudflare Workers?**
- No timeout limits (Cloudflare free plan has a 100s timeout)
- Handles long-running song generation (5+ minutes)
- Free tier: 750 hours/month, no credit card required

### 3. Host the frontend on GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages → Source → Deploy from branch**
3. Select `main` branch, `/ (root)` folder
4. Your site will be live at `https://<username>.github.io/<repo>/`

### 4. Configure in browser

1. Open the GitHub Pages URL
2. Select your provider (GMI Cloud or MiniMax)
3. Paste your API key
4. Expand **Proxy settings** and paste your Render proxy URL
5. Done — generate songs from any device

## Features

- **10 genres** with subgenre presets: Pop, R&B, Hip-hop, Rock, Electronic, Jazz, Country, Latin, K-pop, Metal
- **Lyrics templates**: Birthday, Love ballad, Hype track, Lullaby, Diss track, Story song
- **Song structure reference**: [Verse], [Chorus], [Bridge], [Hook], etc.
- **Style remix**: Generate 2-3 versions of the same lyrics in different genres
- **Advanced settings**: Sample rate, bitrate, format (MP3/WAV/PCM)
- **Song history**: Saved locally, replay or delete past generations
- **Copy/paste settings**: Share your config as JSON via clipboard
- **Long song support**: No timeout limits via Render proxy

## Local development

For local use, you can skip Render and run the Python proxy:

```bash
python3 gmi_proxy.py
# Open http://localhost:8765
```

The app auto-detects: no proxy URL set → falls back to `localhost:8765`.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Frontend app (single file, no build step) |
| `proxy/app.py` | Render CORS proxy (Python/Flask) |
| `proxy/requirements.txt` | Python dependencies |
| `render.yaml` | Render deployment config |
| `gmi_proxy.py` | Local Python CORS proxy (optional) |
| `test-gmi-music.sh` | CLI test script |
| `mockups.html` | Design concept mockups |
