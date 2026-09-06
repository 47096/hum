# Hum — AI Music Generator

Generate songs and instrumentals using AI. Chat with the AI to create style prompts and lyrics, then generate music — all in one conversation.

**Live app:** [https://47096.github.io/hum/](https://47096.github.io/hum/)

**Built for:** [MiniMax Week](https://www.gmicloud.ai/minimax-week) — Synthesis Track

## How it works

```
Chat with AI → AI generates title/style/lyrics → Click Generate → Music plays
```

## Features

### Core
- **Chat-based creation** — describe your song in natural language, AI handles the rest
- **12 genre templates** — Pop, Hip-Hop, R&B, Latin, EDM, Afrobeats, Rock, K-Pop, Country, Lo-fi, Jazz, Soul
- **Image-to-song** — upload an image and AI generates style/lyrics based on the visual mood
- **Document-to-song** — upload a Word doc (.docx) or PowerPoint deck (.pptx) and AI creates a song inspired by the content
- **GitHub repo-to-song** — paste a GitHub URL and AI generates a song about the project
- **YouTube links** — paste a YouTube URL to create a song inspired by it
- **Song & Instrumental modes** — toggle between songs with lyrics and music-only tracks
- **Inline editing** — click to edit title, style, and lyrics directly in the chat
- **Regenerate** — don't like the first result? Click regenerate for a new variation
- **Embedded lyrics** — downloaded MP3s include lyrics for Apple Music

### How editing works
- Edit title, style, or lyrics by clicking on them in the chat
- Click **Generate** to create a song with your edits
- Use **Regenerate** to get a new variation with the same prompt
- Each generation creates a new recording — you can't edit an existing song's vocals

### Limitations
- MiniMax Music3.0 generates complete songs (music + vocals) — partial regeneration isn't supported
- Changing lyrics means generating a new song, not re-recording vocals
- The style prompt creates similar vibes but different executions each time

### UX Polish
- **Setup banner** — guided API key setup for first-time users
- **Sectioned lyrics** — lyrics display with verse/chorus labels for easy scanning
- **Generation timer** — see elapsed time while your song generates
- **Animated loading** — pulsing dots instead of static "Thinking..." text
- **Responsive design** — works on desktop, tablet, and mobile with swipe gestures
- **Keyboard accessible** — full keyboard navigation for all interactive elements
- **Player controls** — dimmed when no track loaded, active when music plays

### Technical
- **Single HTML file** — no build step, no dependencies, deploy anywhere
- **Session storage** — API keys stored securely in sessionStorage
- **Song history** — saved locally, replay or delete past generations
- **Download all** — export all tracks at once
- **Customizable** — sample rate, bitrate, format (MP3/WAV/PCM), BPM, key, mode

## Setup

### 1. Get an API key

**GMI Cloud:**
- Sign up at [console.gmicloud.ai](https://console.gmicloud.ai)
- Go to **API Keys** and create one

**MiniMax (alternative):**
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

## Tech Stack

- **Frontend:** Vanilla HTML/CSS/JS (single file, ~3000 lines)
- **Backend:** Python/Flask proxy for CORS handling
- **LLM:** MiniMax-M3 via GMI Cloud (chat, lyrics, title generation)
- **Music:** MiniMax Music3.0 via GMI Cloud (audio generation)
- **Hosting:** GitHub Pages (frontend) + Render (proxy)
- **Icons:** Lucide
- **Fonts:** Inter

## Competition

Built for [MiniMax Week](https://www.gmicloud.ai/minimax-week) — Synthesis Track.

**What makes it different:**
- Chat-based workflow (not a form)
- Image and YouTube inputs for creative inspiration
- Inline editing and regeneration
- Polished UX with accessibility focus

## License

MIT