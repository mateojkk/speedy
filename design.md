# Design System Prompt — Clean Minimal Professional UI

Build this UI using the following design system. Follow it precisely — do not deviate with your own aesthetic choices.

### Fonts
- Import from Google Fonts: `Instrument Serif` (weights: 400, 400 italic) and `Outfit` (weights: 300, 400, 500, 600)
- Display/headings: `'Instrument Serif', serif` — use for page titles, card names, hero text
- Body/UI: `'Outfit', sans-serif` — use for everything else
- Never use Inter, Roboto, Arial, or system fonts

### Color Tokens
Define these as JS constants or CSS variables at the top of the file:

```js
const T = {
  accent:      "#1B4332",   // dark green — primary brand color
  accentHover: "#2D6A4F",   // slightly lighter green for hover/italic highlights
  accentBg:    "#EEF5F1",   // very light green for status badges, tags
  bg:          "#FAFAF9",   // off-white page background
  surface:     "#FFFFFF",   // card/component background
  text:        "#111111",   // primary text
  muted:       "#555555",   // body/secondary text
  subtle:      "#999999",   // labels, nav links, captions
  border:      "#E8E8E3",   // all borders and dividers
  tag:         "#F5F5F2",   // tech tag / chip background
};
```

### Spacing & Layout
- Page padding: `2.5rem` horizontal on desktop, `1.5rem` on mobile (max-width 640px)
- Section vertical padding: `4rem` to `4.5rem` top and bottom
- Dividers between sections: `1px solid ${T.border}`, full width minus the page padding (use `margin: 0 2.5rem`)
- Max content width: `960px` for hero, `900px` for about grids — left-aligned, not centered
- Grid gaps: `1.5rem` for card grids, `5rem` between two-column about layouts

### Typography Scale
- Hero title: `clamp(2.8rem, 6vw, 4.5rem)`, `font-family: Instrument Serif`, `line-height: 1.08`, `letter-spacing: -0.03em`
- Section label (eyebrow): `0.74rem`, `Outfit`, `font-weight: 500`, `letter-spacing: 0.1em`, `text-transform: uppercase`, color `T.subtle`
- Card name: `1.35–1.4rem`, `Instrument Serif`, `letter-spacing: -0.02em`
- Card tagline: `0.82rem`, `Outfit`, `font-weight: 500`, color `T.accentHover`
- Body text: `1rem` or `0.88rem`, `font-weight: 300`, `line-height: 1.65–1.85`, color `T.muted` or `#444`
- Tags/chips: `0.72rem`, `background: T.tag`, `color: #666`
- Nav links: `0.82rem`, `letter-spacing: 0.05em`, `text-transform: uppercase`, color `T.subtle`
- Footer: `0.78rem`, color `#aaa`, `letter-spacing: 0.03em`

### Borders & Radius
- All borders: `1px solid ${T.border}` (cards, sections, stack rows)
- Border radius: `2px` on buttons only — everything else is sharp (no border-radius on cards, tags, badges)
- Divider lines: `1px solid ${T.border}`
- Dashed borders for secondary CTAs: `1px dashed ${T.border}`

### Buttons
Two button styles only:

**Primary (dark fill):**
```css
padding: 0.72rem 1.6rem;
background: #111;
color: #fff;
border: none;
font-family: 'Outfit', sans-serif;
font-size: 0.85rem;
letter-spacing: 0.03em;
border-radius: 2px;
transition: background 0.2s;
/* hover: background #1B4332 */
```

**Outline (ghost):**
```css
padding: 0.72rem 1.6rem;
background: transparent;
color: #111;
border: 1px solid #ccc;
font-family: 'Outfit', sans-serif;
font-size: 0.85rem;
letter-spacing: 0.03em;
border-radius: 2px;
transition: border-color 0.2s, color 0.2s;
/* hover: border-color #1B4332, color #1B4332 */
```

### Cards
```css
border: 1px solid #E8E8E3;
padding: 1.75rem;
background: #FFFFFF;
/* hover: border-color #1B4332, transform: translateY(-3px) */
/* transition: border-color 0.2s, transform 0.2s */
```
No border-radius. No box shadow.

### Status Badges
```css
font-size: 0.68rem;
letter-spacing: 0.07em;
text-transform: uppercase;
padding: 0.22rem 0.6rem;
font-weight: 500;
/* no border-radius */
/* green status: background #EEF5F1, color #1B4332 */
/* amber status: background #F5F0E8, color #7A5C1E */
```

### Navigation
- Sticky top nav, `background: T.bg`, `border-bottom: 1px solid T.border`
- Left: brand name in Instrument Serif
- Right: 3 links in Outfit uppercase
- On scroll: add subtle `box-shadow: 0 1px 12px rgba(0,0,0,0.05)`

### Animations & Hover
- Card hover: `transform: translateY(-3px)` + border color to accent
- Link hover: color to `#1B4332`
- All transitions: `0.2s` ease, no easing function needed
- No entrance animations, no scroll animations, no parallax — keep it static and fast

### Italic Accent
In hero titles, wrap the emotional/key word in `<em>` with:
```css
font-style: italic;
color: #2D6A4F;
```

### Responsive Rules
At `max-width: 640px`:
- Reduce horizontal padding to `1.5rem`
- Two-column grids collapse to single column
- Nav link gap reduces to `1rem`
- Section padding reduces to `3rem`

### Do Not
- No gradients anywhere
- No box shadows on cards (only on focused inputs if any)
- No colored backgrounds on sections — everything sits on `#FAFAF9`
- No centered layouts — all content is left-aligned
- No heavy font weights (600+ only on nav brand, nowhere else)
- No rounded cards
- No dark mode toggle (design is light-mode only)
- No placeholder lorem ipsum — write real concise copy

### Tone of Copy
- Lowercase preferred for UI labels and nav
- Short, direct, no filler words
- Section eyebrows are single nouns or short noun phrases (e.g. "selected projects", "get in touch")
- Hero subtitles: one or two sentences, `font-weight: 300`

---

## Example section structure (for reference)

```
NAV (sticky)
HERO (eyebrow label + serif title with italic accent + muted subtitle + 2 CTAs)
DIVIDER
SECTION: cards grid (label + responsive grid of bordered cards)
DIVIDER
SECTION: two-column (label + about text left + stack/detail list right)
DIVIDER
SECTION: contact (label + short paragraph + text links with border-bottom)
FOOTER (two items, space-between)
```