# Hum — AI music generator

**Product — chat (or paste anything) into a song.**

Describe a vibe, upload a deck/photo, drop a GitHub link or YouTube URL — Hum writes style + lyrics and generates the track in one conversation.

https://github.com/user-attachments/assets/cce36cd9-dcc2-4a13-82eb-ca20e15ae68b

**[Live app →](https://47096.github.io/hum/)** · Built for [MiniMax Week](https://www.gmicloud.ai/minimax-week) — Synthesis Track

---

## Why this product

Music generation is usually a form and a prompt box. Hum is a **conversation**: editable title/style/lyrics in chat, multiple input types (text, image, doc, repo, video), then one click to a finished song with **lyrics embedded** in the MP3.

## How it works

```
Chat / upload → title + style + lyrics → Generate → play + download
```

## Features

| Area | What you get |
|------|----------------|
| **Create** | Chat prompts · 12 genre templates · song or instrumental |
| **Inputs** | Text · image · .docx/.pptx · GitHub repo URL · YouTube URL |
| **Edit** | Click-to-edit title / style / lyrics · regenerate variations |
| **Output** | Play in-browser · WAV/MP3 · lyrics in MP3 tags · download all |
| **UX** | Setup banner · verse/chorus layout · timers · responsive · keyboard |

**Limits (honest):** full-song generation only (no partial vocal re-record). Each Generate is a new take.

## Use cases

| Use | How |
|-----|-----|
| **Team anthem / all-hands** | Paste the quarterly deck |
| **Content & social** | Image or caption → short track |
| **Open-source / dev community** | Paste your GitHub repo |
| **Learning** | Notes → lo-fi study track |
| **Personal** | Travel photos, resumes, in-jokes → a song |

## Sample track

Showcase output from the app (also in-repo: [`demo/hum-of-creation.mp3`](demo/hum-of-creation.mp3)).

<audio controls src="https://github.com/47096/hum/raw/main/demo/hum-of-creation.mp3">
  Your browser does not support the audio element.
  <a href="demo/hum-of-creation.mp3">Download the sample MP3</a>
</audio>

## Run your own

1. **API key** — [GMI Cloud](https://console.gmicloud.ai) or [MiniMax](https://platform.minimax.io)  
2. **Proxy** — `proxy/` on [Render Blueprint](https://render.com) (or `python proxy/app.py` locally)  
3. **Frontend** — this repo’s `index.html` (GitHub Pages or any static host)  
4. **Configure** — provider + key + proxy URL in the app  

```bash
cd proxy && pip install -r requirements.txt && python app.py
# frontend: open index.html or serve the repo root
```

## Repo layout

| Path | Role |
|------|------|
| `index.html` | Single-file frontend |
| `proxy/app.py` | CORS proxy + lyrics embedding (Flask) |
| `render.yaml` | Render deploy config |
| `demo/hum-of-creation.mp3` | Sample generated track |

## Tech

Vanilla HTML/CSS/JS · Flask proxy · MiniMax-M3 (chat/lyrics) · MiniMax Music3.0 (audio) · GitHub Pages + Render · Lucide · Inter

**Privacy:** API keys stay in `sessionStorage`; generation goes through your proxy to the music provider you choose.

## Family

- [`mimo-reader`](https://github.com/47096/mimo-reader) — browser TTS product  
- [`hanna`](https://github.com/47096/hanna) — Chrome TTS extension  
- [`lux-tts`](https://github.com/47096/lux-tts) — Colab voice-clone demo  

## License

MIT · [datafying](https://datafying.co/)
