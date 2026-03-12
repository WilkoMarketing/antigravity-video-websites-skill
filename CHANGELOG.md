# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-03-11

### Added
- **"Step 0: The Interview" Task**: Added mandatory interview questions for the agent to gather design system variables (colors, fonts, brand vibe) before generating the UI.
- **Navbar Scroll-to-Pill Animation**: Introduced a GSAP behavior that transforms a full-width navbar into a centered, glassmorphism "pill" shape as the user scrolls.
- **Magnetic Snap-Stop Logic**: Integrated ScrollTrigger `snap` patterns to create rhythmic pauses when information cards enter the viewport ("boom, boom, boom" reading effect).

## [1.0.0] - 2026-03-04

### Added
- Initial release of the `creating-video-websites` skill.
- Native Python script (`extract_frames.py`) with OpenCV for slicing MP4/MOV videos into WebP frames.
- **AI Background Removal**: Integrated `rembg` (neural network) to strip out solid backgrounds or fake transparency grids via the `--remove-bg` flag.
- Smooth scrolling integration with Lenis.
- GSAP choreography and scroll-trigger animations for 6+ varying section transitions.
- Strict design rules (12rem massive typography, side-alignment, circle-clip hero reveal).
