# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Hobbyists and experimenters curious about AI music generation. They want to quickly create music ideas, demos, or background tracks without deep technical knowledge or professional music production skills.

## Product Purpose

A simplicity-first tool that lets users generate AI music in under 60 seconds. Users paste their API key, pick a genre, optionally add lyrics, and hit generate. The product succeeds when someone who's never used AI music generation can create their first song without reading documentation.

## Positioning

The simplest way to generate AI music. No account creation, no setup wizard, no learning curve — just paste a key and make music. Other tools require accounts, subscriptions, or complex interfaces. AI Music requires only an API key and a browser.

## Operating Context

Users open the app in a browser, paste their GMI Cloud or MiniMax API key (obtained separately), select a genre and style, optionally add lyrics with song structure tags, and click Generate. The app sends the request to the API, polls for completion, and plays the result. Songs are saved to browser localStorage for later playback.

## Capabilities and Constraints

- Single HTML file, no build step, runs anywhere
- Requires user to provide their own API key (GMI Cloud or MiniMax)
- Supports both instrumental and lyrical generation
- 10 music genres with 5 subgenres each
- 5 built-in lyrics templates
- Advanced settings: sample rate, bitrate, format, BPM, key, mode
- Style remix mode for generating multiple variations
- Song history stored in localStorage (browser only)
- Dark/light theme toggle
- Keyboard shortcut: Cmd/Ctrl+Enter to generate
- Share links via URL encoding

## Brand Commitments

- Name: AI Music
- Voice: Technical but approachable, terminal-inspired aesthetic
- Identity: Cyberpunk/hacker aesthetic with green-on-black color scheme
- No account required, no data collection beyond API keys stored locally

## Evidence on Hand

- Working app deployed at https://47096.github.io/ai-music/
- Proxy server deployed at https://ai-music-proxy.onrender.com/
- 5 lyrics templates: Morning coffee, Gym pump-up, Study focus, Sunset drive, Party starter

## Product Principles

1. **Simplicity above all** — Every feature must pass the "can a first-time user figure this out without instructions?" test
2. **No accounts, no tracking** — Users bring their own API key, we store nothing server-side
3. **Instant gratification** — From opening the app to hearing music should take under 60 seconds
4. **Progressive disclosure** — Basic flow is obvious; advanced settings exist but don't clutter the default experience

## Accessibility & Inclusion

- Keyboard navigation support (Cmd/Ctrl+Enter to generate)
- ARIA roles on interactive elements (toggles, buttons)
- Touch targets minimum 44px for mobile
- Focus indicators on interactive elements
