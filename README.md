# AI Music — GMI Cloud

Generate songs from lyrics using MiniMax Music 3.0 via GMI Cloud or MiniMax APIs.

## How it works

```
Browser → Cloudflare Worker (CORS proxy) → GMI Cloud / MiniMax API → MP3
```

## Setup

### 1. Get an API key

**GMI Cloud (free during campaign, ends Sep 6, 2026):**
- Sign up at [console.gmicloud.ai](https://console.gmicloud.ai)
- Go to **API Keys** and create one

**MiniMax (paid):**
- Sign up at [platform.minimax.io](https://platform.minimax.io)
- Go to **API Keys** and create one

### 2. Deploy the CORS proxy (Cloudflare Worker)

```bash
cd worker
npx wrangler login      # one-time: authenticate with Cloudflare
npx wrangler deploy     # deploys the worker
```

Note the output URL (e.g. `https://gmi-music-proxy.<your-subdomain>.workers.dev`).

### 3. Host the frontend on GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages → Source → Deploy from branch**
3. Select `main` branch, `/ (root)` folder
4. Your site will be live at `https://<username>.github.io/<repo>/`

### 4. Configure in browser

1. Open the GitHub Pages URL
2. Select your provider (GMI Cloud or MiniMax)
3. Paste your API key
4. Expand **Proxy settings** and paste your Worker URL
5. Done — generate songs from any device

## Features

- **10 genres** with subgenre presets: Pop, R&B, Hip-hop, Rock, Electronic, Jazz, Country, Latin, K-pop, Metal
- **Lyrics templates**: Birthday, Love ballad, Hype track, Lullaby, Diss track, Story song
- **Song structure reference**: [Verse], [Chorus], [Bridge], [Hook], etc.
- **Style remix**: Generate 2-3 versions of the same lyrics in different genres
- **Advanced settings**: Sample rate, bitrate, format (MP3/WAV/PCM)
- **Song history**: Saved locally, replay or delete past generations
- **Copy/paste settings**: Share your config as JSON via clipboard

## Local development

For local use, you can skip the Worker and run the Python proxy:

```bash
python3 gmi_proxy.py
# Open http://localhost:8765
```

The app auto-detects: no proxy URL set → falls back to `localhost:8765`.

## Files

| File | Purpose |
|------|---------|
| `index.html` | Frontend app (single file, no build step) |
| `gmi_proxy.py` | Local Python CORS proxy (optional) |
| `worker/` | Cloudflare Worker CORS proxy |
| `test-gmi-music.sh` | CLI test script |
| `mockups.html` | Design concept mockups |
