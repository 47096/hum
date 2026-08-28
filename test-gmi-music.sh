#!/bin/bash
# Test GMI MiniMax Music 3.0 — set GMI_API_KEY in env first
#   export GMI_API_KEY="***"
#   ./test-gmi-music.sh

if [ -z "$GMI_API_KEY" ]; then
  echo "Set GMI_API_KEY first: export GMI_API_KEY=***"
  exit 1
fi

curl -X POST "https://console.gmicloud.ai/api/v1/ie/requestqueue/apikey/requests" \
  -H "Authorization: Bearer $GMI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "minimax-music-3.0",
    "payload": {
      "lyrics": "[verse]\nDaniel Daniel clap your hands\nClap them loud and clap them soft\n[chorus]\nDaniel is five and oh so bright\nLa la la la la la la",
      "prompt": "Cheerful children song, ukulele, clapping, bright",
      "sample_rate": 44100,
      "bitrate": 128000,
      "format": "mp3"
    }
  }'
