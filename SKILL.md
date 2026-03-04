---
name: creating-video-websites
description: Turn a video into a premium scroll-driven animated website with GSAP, canvas frame rendering, and layered animation choreography. Use when the user wants to convert a video into an animated web experience.
---

# Video to Premium Scroll-Driven Website

Turn a video file into a scroll-driven animated website with **animation variety and choreography** — multiple animation types working together, not one repeated effect.

## When to use this skill
- Generating a website from a video file.
- Creating a scroll-driven GSAP experience.
- Implementing a premium canvas-rendered video site.

## Input

The user provides: a video file path (MP4, MOV, etc.) and optionally:
- A theme/brand name
- Desired text sections and where they appear
- Color scheme preferences
- Any specific design direction

If the user doesn't specify these, ask briefly or use sensible creative defaults.

## Premium Checklist (Non-Negotiable)

- [ ] **Lenis smooth scroll** — native scroll feels "web page," Lenis feels "experience"
- [ ] **4+ animation types** — never repeat the same entrance animation consecutively
- [ ] **Staggered reveals** — label → heading → body → CTA, never all at once
- [ ] **No glassmorphism cards** — text on clean backgrounds, hierarchy via font size/weight/color
- [ ] **Direction variety** — sections enter from different directions (left, right, up, scale, clip)
- [ ] **Dark overlay for stats** — 0.88-0.92 opacity, counters animate up, only time center text is OK
- [ ] **Horizontal text marquee** — at least one oversized text element sliding on scroll (12vw+)
- [ ] **Counter animations** — all numbers count up from 0, never appear statically
- [ ] **Massive typography** — hero 12rem+, section headings 4rem+, marquee 10vw+
- [ ] **CTA persists** — `data-persist="true"` keeps final section visible, never disappears
- [ ] **Hero prominence + generous scroll** — hero gets 20%+ scroll range, 800vh+ total for 6 sections
- [ ] **Side-aligned text ONLY** — all text in outer 40% zones (`align-left`/`align-right`), never center. Exception: stats with full dark overlay
- [ ] **Circle-wipe hero reveal** — hero is standalone 100vh section, canvas reveals via `clip-path: circle()` as hero scrolls away
- [ ] **Frame speed 1.8-2.2** — product animation completes by ~55% scroll. Below 1.8 feels sluggish

## Workflow

### Step 1: Analyze the Video & Extract Frames

To extract frames from the user's video, use the Python script bundled with this skill instead of relying on external FFmpeg installations.

1. Ensure `opencv-python` is installed in the user's environment before proceeding. If not, use terminal to install it: `pip install opencv-python`.
2. Determine target fps and resolution.
    - **Target frame count**: 150-300 frames for good scroll experience
        - Short video (<10s): extract at original fps, cap at ~300
        - Medium (10-30s): extract at 10-15fps
        - Long (30s+): extract at 5-10fps
    - **Output resolution**: Match aspect ratio, cap width at 1920px (handled automatically by the script).

3. Run the frame extraction script:
```bash
python ~/.gemini/antigravity/skills/creating-video-websites/scripts/extract_frames.py "<VIDEO_PATH>" <CALCULATED_FPS> [--remove-bg]
```
*(Note for Windows users: The path will be `C:\Users\<user>\.gemini\antigravity\skills\creating-video-websites\scripts\extract_frames.py`)*

**Important:** If the video has a solid background, a "fake" transparency grid (like a stock video), or needs to integrate seamlessly over the dark website background, use the `--remove-bg` flag. This will use AI (`rembg`) to extract the main subject and create true transparent WebP frames. If `rembg` is missing, install it via `pip install "rembg[cpu]"`.

After extraction, the script will output WebP files into a `frames/` folder in the current directory.

### Step 2: Scaffold

```text
project-root/
  index.html
  css/style.css
  js/app.js
  frames/frame_0001.webp ...
```

No bundler. Vanilla HTML/CSS/JS + CDN libraries.

### Step 3: Build index.html

Required structure (in this order):

```html
<!-- 1. Loader: #loader > .loader-brand, #loader-bar, #loader-percent -->
<!-- 2. Fixed header: .site-header > nav with logo + links -->
<!-- 3. Hero: .hero-standalone (100vh, solid bg, word-split heading) -->
<!--    Contains: .section-label, .hero-heading (words in spans), .hero-tagline -->
<!--    Scroll indicator with arrow -->
<!-- 4. Canvas: .canvas-wrap > canvas#canvas (fixed, full viewport) -->
<!-- 5. Dark overlay: #dark-overlay (fixed, full viewport, pointer-events:none) -->
<!-- 6. Marquee(s): .marquee-wrap > .marquee-text (fixed, 12vw font) -->
<!-- 7. Scroll container: #scroll-container (800vh+) -->
<!--    Content sections with data-enter, data-leave, data-animation -->
<!--    Stats section with .stat-number[data-value][data-decimals] -->
<!--    CTA section with data-persist="true" -->
```

Content section example:
```html
<section class="scroll-section section-content align-left"
         data-enter="22" data-leave="38" data-animation="slide-left">
  <div class="section-inner">
    <span class="section-label">002 / Feature</span>
    <h2 class="section-heading">Feature Headline</h2>
    <p class="section-body">Description text here.</p>
  </div>
</section>
```

Stats section example:
```html
<section class="scroll-section section-stats"
         data-enter="54" data-leave="72" data-animation="stagger-up">
  <div class="stats-grid">
    <div class="stat">
      <span class="stat-number" data-value="24" data-decimals="0">0</span>
      <span class="stat-suffix">hrs</span>
      <span class="stat-label">Cold retention</span>
    </div>
  </div>
</section>
```

CDN scripts (end of body, this order):
```html
<script src="https://cdn.jsdelivr.net/npm/lenis@1/dist/lenis.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/ScrollTrigger.min.js"></script>
<script src="js/app.js"></script>
```

### Step 4: Build css/style.css

Use creative, distinctive styling. Key technical patterns:

```css
:root {
  --bg-light: #f5f3f0;
  --bg-dark: #111111;
  --text-on-light: #1a1a1a;
  --text-on-dark: #f0ede8;
  --font-display: 'Inter', sans-serif;
  --font-body: 'Roboto', sans-serif;
}

/* Side-aligned text zones — product occupies center */
.align-left { padding-left: 5vw; padding-right: 55vw; }
.align-right { padding-left: 55vw; padding-right: 5vw; }
.align-left .section-inner,
.align-right .section-inner { max-width: 40vw; }
```

- **Hero-first layout**: Hero is standalone 100vh with solid bg. Canvas starts hidden, reveals via circle-wipe as hero scrolls away.
- **Scroll sections**: `position: absolute` within scroll container, positioned at midpoint of enter/leave range, `transform: translateY(-50%)`.
- **Mobile (<768px)**: Collapse side alignment to centered text with dark backdrop overlays. Reduce scroll height to ~550vh.
- **Text contrast**: Never use `#999` for important text on light backgrounds. Use `#666` minimum for body, `var(--text-on-light)` for headings.

### Step 5: Build js/app.js

#### 5a. Lenis Smooth Scroll (MANDATORY)

```javascript
// Add Lenis Initialization Check
if(typeof Lenis === 'undefined'){
    console.error("Lenis is not loaded!")
}
const lenis = new Lenis({
  duration: 1.2,
  easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
  smoothWheel: true
});
lenis.on("scroll", ScrollTrigger.update);
gsap.ticker.add((time) => lenis.raf(time * 1000));
gsap.ticker.lagSmoothing(0);
```

#### 5b. Frame Preloader

Two-phase loading: load first 10 frames immediately (fast first paint), then load remaining frames in background. Show progress bar during load. Hide loader only after all frames are ready.

#### 5c. Canvas Renderer — Padded Cover Mode

```javascript
const IMAGE_SCALE = 0.85; // 0.82-0.90 sweet spot
function drawFrame(index) {
  const img = frames[index];
  if (!img) return;
  const cw = canvas.width, ch = canvas.height;
  const iw = img.naturalWidth, ih = img.naturalHeight;
  const scale = Math.max(cw / iw, ch / ih) * IMAGE_SCALE;
  const dw = iw * scale, dh = ih * scale;
  const dx = (cw - dw) / 2, dy = (ch - dh) / 2;
  ctx.fillStyle = bgColor; // sampled from frame corners
  ctx.fillRect(0, 0, cw, ch);
  ctx.drawImage(img, dx, dy, dw, dh);
}
```

- Auto-sample background color from frame edge pixels with `sampleBgColor()` every ~20 frames
- Fill canvas with sampled color BEFORE drawing (fills the thin padded border seamlessly)
- Apply devicePixelRatio scaling for crisp rendering

#### 5d. Frame-to-Scroll Binding

```javascript
const FRAME_SPEED = 2.0; // 1.8-2.2, higher = product animation finishes earlier
ScrollTrigger.create({
  trigger: document.getElementById('scroll-container'),
  start: "top top",
  end: "bottom bottom",
  scrub: true,
  onUpdate: (self) => {
    const accelerated = Math.min(self.progress * FRAME_SPEED, 1);
    const index = Math.min(Math.floor(accelerated * FRAME_COUNT), FRAME_COUNT - 1);
    if (index !== currentFrame) {
      currentFrame = index;
      requestAnimationFrame(() => drawFrame(currentFrame));
    }
  }
});
```

#### 5e. Section Animation System

Each section reads `data-animation` and gets a different entrance. Sections with `data-persist="true"` stay visible once animated in. Position sections absolutely at the midpoint of their enter/leave range with `translateY(-50%)`.

```javascript
function setupSectionAnimation(section) {
  const type = section.dataset.animation;
  const persist = section.dataset.persist === "true";
  const enter = parseFloat(section.dataset.enter) / 100;
  const leave = parseFloat(section.dataset.leave) / 100;
  const children = section.querySelectorAll(
    ".section-label, .section-heading, .section-body, .section-note, .cta-button, .stat"
  );

  const tl = gsap.timeline({ paused: true });

  switch (type) {
    case "fade-up":
      tl.from(children, { y: 50, opacity: 0, stagger: 0.12, duration: 0.9, ease: "power3.out" });
      break;
    case "slide-left":
      tl.from(children, { x: -80, opacity: 0, stagger: 0.14, duration: 0.9, ease: "power3.out" });
      break;
    case "slide-right":
      tl.from(children, { x: 80, opacity: 0, stagger: 0.14, duration: 0.9, ease: "power3.out" });
      break;
    case "scale-up":
      tl.from(children, { scale: 0.85, opacity: 0, stagger: 0.12, duration: 1.0, ease: "power2.out" });
      break;
    case "rotate-in":
      tl.from(children, { y: 40, rotation: 3, opacity: 0, stagger: 0.1, duration: 0.9, ease: "power3.out" });
      break;
    case "stagger-up":
      tl.from(children, { y: 60, opacity: 0, stagger: 0.15, duration: 0.8, ease: "power3.out" });
      break;
    case "clip-reveal":
      tl.from(children, { clipPath: "inset(100% 0 0 0)", opacity: 0, stagger: 0.15, duration: 1.2, ease: "power4.inOut" });
      break;
  }

  // Play/reverse based on scroll position via ScrollTrigger onUpdate
  // If persist is true, never reverse when scrolling past the leave point
}
```

#### 5f. Horizontal Text Marquee

```javascript
document.querySelectorAll(".marquee-wrap").forEach(el => {
  const speed = parseFloat(el.dataset.scrollSpeed) || -25;
  gsap.to(el.querySelector(".marquee-text"), {
    xPercent: speed,
    ease: "none",
    scrollTrigger: { trigger: '#scroll-container', start: "top top", end: "bottom bottom", scrub: true }
  });
});
```

### Step 6: Test

1. Serve locally: `npx serve .` (or `python -m http.server 8000`)
2. Scroll through fully — verify each section has a DIFFERENT animation type
3. Confirm: smooth scroll, frame playback, staggered reveals, marquee slides, counters count up, dark overlay fades, CTA persists at end
