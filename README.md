# MiniMax Music 3.0 — GMI Cloud

Generate songs from lyrics using MiniMax Music 3.0 via GMI Cloud's free API.

## How it works

```
Browser → Cloudflare Worker (CORS proxy) → GMI Cloud API → MP3
```

## Setup

### 1. Get a GMI Cloud API key
- Sign up at [console.gmicloud.ai](https://console.gmicloud.ai)
- Go to **API Keys** and create one
- Free during the campaign (ends Sep 6, 2026)

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
2. Paste your GMI Cloud API key
3. Expand **Proxy settings** and paste your Worker URL
4. Done — generate songs from any device

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
| `index.html` | Frontend app |
| `gmi_proxy.py` | Local Python CORS proxy (optional) |
| `worker/` | Cloudflare Worker CORS proxy |
| `test-gmi-music.sh` | CLI test script |
