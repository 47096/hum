# Surface Brief: AI Music Redesign

## Job and Audience

**Who arrives:** Hobbyists and experimenters curious about AI music generation. They want to quickly create music ideas, demos, or background tracks without deep technical knowledge.

**Context:** Users open the app in a browser, paste an API key, pick a genre, and generate music. The experience should feel effortless and premium — like using a high-quality creative tool, not a hacker's playground.

**Visitor mode:** Operate — the visitor completes a task (generate music), not browses marketing content.

## Outcome and Proof

**Primary action:** Generate a song. Success = user clicks Generate and hears music within 60 seconds.

**Real evidence:**
- 10 music genres with 5 subgenres each
- 5 built-in lyrics templates
- Instrumental and lyrical generation modes
- Advanced settings (BPM, key, mode, sample rate, bitrate, format)
- Song history with playback

**Product-specific truth:** No account required, no data collection, API key stored only in browser. The simplest way to generate AI music.

## Selected Direction

**Visual world:** Minimal & Premium

**Thesis:** Strip away the cyberpunk terminal aesthetic. Replace with a calm, confident interface that communicates quality through restraint — generous whitespace, precise typography, and intentional color.

**Palette strategy:** Restrained — neutral base (off-white or very light gray) with one accent color for primary actions. Dark mode as alternate, not default.

**Typography:** One clean sans-serif for body (e.g., Inter, DM Sans, or similar), one slightly warmer or more characterful face for display elements (headings, logo). No monospace except for code/data fields.

**Structural thesis:** Single-column layout with clear visual hierarchy. The Generate button should be the most prominent element on the page. Genre selection, lyrics, and advanced settings should feel organized but not cluttered.

**Signature interaction:** The Generate button should feel satisfying to click — clear visual feedback, smooth transition to "Composing..." state, and a polished result display.

**First viewport:**
- Clean header with logo and minimal navigation
- Prominent genre/subgenre selection (horizontal chips, not wrapped)
- Lyrics input with templates as secondary action
- Large, centered Generate button
- Status indicator below button

## Scope and Boundaries

**Fidelity:** Production-ready single-page app. Not a mockup — real, working HTML/CSS/JS.

**Breadth:** Complete redesign of the existing app. Same features, new visual world.

**Interactivity:** Full functionality preserved. Theme toggle, instrumental mode, advanced settings, history.

**What remains untouched:**
- All existing features and functionality
- API integration (GMI Cloud + MiniMax)
- Proxy configuration
- localStorage-based history
- Keyboard shortcuts

**Anti-goals:**
- No cyberpunk/terminal aesthetic
- No monospace font for body text
- No dark default (light mode primary)
- No glow effects or neon accents
- No complex visual noise

## States and Ranges

**Content ranges:**
- Genre chips: 10 items
- Subgenre chips: 5 items per genre
- Lyrics: 0-3,500 characters
- History: 0-50 songs

**Material states:**
- First visit (no API key)
- API key set, ready to generate
- Generating (loading state)
- Song complete (player visible)
- Error state
- Empty history
- Instrumental mode active

## Interaction and Layout

**Hierarchy:**
1. Generate button (primary)
2. Genre/subgenre selection
3. Lyrics input
4. Advanced settings (collapsed by default)
5. History (below fold)

**Layout:** Single-column, max-width ~700px, centered. Generous vertical spacing between sections.

**Responsive:** Mobile-first. Genre chips should wrap gracefully. Generate button always visible above the fold.

**Affordances:**
- Chips clearly show selection state (filled vs outline)
- Toggle switches for binary options (instrumental, remix)
- Collapsible sections for advanced settings
- Clear primary action (Generate) vs secondary actions

**Feedback:**
- Button click → immediate visual response
- Generating → clear progress indication
- Success → smooth transition to player
- Error → clear, actionable error message

**Transitions:** Subtle, purposeful. No gratuitous animation. Focus on state changes (button → loading → result).

## Constraints and Open Decisions

**Platform:** Web (browser-based)

**Delivery:** Single HTML file, no build step

**Accessibility:**
- Keyboard navigation (Cmd/Ctrl+Enter to generate)
- ARIA roles on interactive elements
- Touch targets ≥44px
- Focus indicators

**Open decisions:**
- Exact color palette (to be determined in visual direction)
- Exact typography choices (to be determined)
- Whether to keep dark mode as alternate or remove it
