# antigravity-video-websites-skill

**Google Antigravity Skill: Premium Video-to-Website**

Transform any raw video file into an immersive, premium scroll-driven animated website instantly with Google Antigravity.

This skill equips your local Antigravity agent with the knowledge, rendering logic, and built-in AI tools to automatically scaffold a frontend application fueled by your video files—bridging the gap between raw footage and high-end interactive UI design.

## ✨ Features

By adding this skill, your Google Antigravity agent becomes an expert in:
- **🎥 WebP Frame Extraction**: Slices any `.mp4`, `.mov`, etc. video into optimized `.WebP` frames automatically via an embedded Python script.
- **✨ AI Background Removal (`rembg`)**: Identifies the subject of your video and erases solid backgrounds or "fake transparency grids", delivering clean, alpha-channel assets ready for dark-mode web composites. (Use the `--remove-bg` flag during prompt!).
- **🎯 Mandatory "Interview" Phase**: The agent will actively pause and ask the user for brand guidelines, hex colors, and content sources *before* touching a single line of code, ensuring a truly tailored result.
- **📜 Lenis Smooth Scroll**: Instantly scaffolds a native-feel, ultra-smooth scrolling experience.
- **🪄 GSAP Choreography**: Animates up to 6 different content sections using a variety of animations (`stagger-up`, `slide-left`, `scale-up`, `clip-reveal`, and more) driven by user scroll depth, ensuring no redundant motion.
- **✨ UI Polish (Pill Navs & Snap-Stops)**: Employs Apple-level interaction design like full-width Navbars that morph into frosted-glass "pills" on scroll, and magnetic "Snap-Stop" scroll triggers that rhythmically pause the user exactly when text appears.
- **🎨 Premium Visual Formatting**: Implements strict design system rules like 12rem massive typography, side-aligned layouts, horizontal scrolling marquees, and dynamic overlay fading based on scroll mapping.

## 🚀 How to Install in Google Antigravity

To register this skill globally so your agent can use it on any project:

### 1. Locate your Global Skills Directory:
* **Windows**: `C:\Users\<YourUser>\.gemini\antigravity\skills\`
* **Mac/Linux**: `~/.gemini/antigravity/skills/`

### 2. Copy the folder:
Download the contents of this repository and place them inside a folder named `creating-video-websites` directly inside the global `skills/` directory.

The final structure should look like this:
```txt
.gemini/antigravity/skills/creating-video-websites/
  ├── SKILL.md
  └── scripts/
       └── extract_frames.py
```

### 3. Dependencies
For the AI background extraction and OpenCV video slicing to run locally, tell your agent to verify these python packages are installed on your machine (or install them yourself):
```bash
pip install opencv-python numpy
pip install "rembg[cpu]"
```

## 💬 How to use it (Prompt Example)

Once the skill is in the folder, simply open a new Antigravity chat and say:

> *"Create a premium animated website for a boxing glove product named WILKO. Use the video file located at `C:\video.mp4`. Use the **creating-video-websites** skill and make sure to remove the video background."*

Antigravity will instantly process the video, slice the frames, scaffold the `index.html`, `style.css`, and `app.js` using GSAP/Lenis, and give you a functional scroll-driven site in underneath a minute.

## 🤝 Contributing
Feel free to open a PR or suggest improvements to the GSAP scroll-triggers, Lenis configurations, or the OpenCV slicing scripts.
