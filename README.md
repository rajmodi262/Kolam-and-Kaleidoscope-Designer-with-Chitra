# 🎨 Accessible Kolam & Kaleidoscope Designer with Chitra

A voice-enabled, AI-assisted web application for creating, transforming, analyzing, and generating traditional South Indian **Kolam** patterns and **Kaleidoscope** designs. The app is built around **Chitra**, a personal voice assistant that makes the entire art-creation experience accessible to everyone — including visually impaired users.

---

## 🏆 Smart India Hackathon (SIH) 2025

> **Problem Statement ID:** SIH25107
> **Team Name:** BrainChain
> **Team ID:** 83250
> **Mentor:** Dr. Jayshree Ghorpade-Aher
> **Event:** Smart India Hackathon 2025 — University Internal Round, MIT World Peace University

### 🎖️ Achievement

Our team successfully cleared the college-level SIH rounds and secured a **Top 10% rank** at the university level, finishing with an **overall rank of 63** among strong competing teams.

### 💡 Problem Statement

This project recreates traditional Indian Kolam art using computational logic, applying geometric symmetry and iterative algorithms to generate complex patterns. The solution reduces manual effort by **80–90%** while ensuring consistency, scalability, and core computer science–driven creative design.

### 🐢 SIH Core Implementation — Python Turtle Graphics

The original SIH submission was built using **Python Turtle Graphics**, with algorithms designed to programmatically generate four types of Kolam patterns:

| Pattern Type | Description |
|---|---|
| **Star Kolams** | Geometric star forms using angle-based rotation |
| **Lotus Patterns** | Petal structures generated through iterative curve logic |
| **Spiral Designs** | Expanding/contracting spirals using incremental radius steps |
| **Symmetric Kolams** | Multi-axis symmetric patterns using reflective geometry |

Each design is generated using these core CS principles:

- **Loops & Conditionals** — Repeat and branch logic to build complex forms from simple rules
- **Symmetry & Angle-based Geometry** — Trigonometric rotation to achieve n-fold symmetry
- **Modular, Reusable Functions** — Clean separation of each pattern into callable functions
- **Clean Visual Logic** — Translating mathematical patterns directly into drawing instructions

### 🧠 Skills Developed

- Algorithmic thinking and geometric reasoning
- Python programming and Turtle graphics
- Creativity-driven problem solving
- Teamwork and hackathon-level project delivery

### 🔗 Links

- 📁 **GitHub Repository:** [https://lnkd.in/dF__qkXs](https://lnkd.in/dF__qkXs)
- 🎥 **Project Demo Video:** [https://lnkd.in/dwqXN3cP](https://lnkd.in/dwqXN3cP)

> 👆 Click the **Project Demo** link above to watch the full working demonstration of the Kolam & Kaleidoscope Designer with Chitra.

---

## 📌 Table of Contents

1. [Smart India Hackathon (SIH) 2025](#-smart-india-hackathon-sih-2025)
2. [Project Overview](#project-overview)
3. [Key Features](#key-features)
4. [Tech Stack](#tech-stack)
5. [Project Structure](#project-structure)
6. [Application Modes](#application-modes)
7. [Chitra — Voice Assistant](#chitra--voice-assistant)
8. [Preprocessing & Computer Vision Pipeline](#preprocessing--computer-vision-pipeline)
9. [Generative Design Algorithm](#generative-design-algorithm)
10. [Kolam Analysis Engine](#kolam-analysis-engine)
11. [Kaleidoscope Drawing Tool](#kaleidoscope-drawing-tool)
12. [Visual Effects](#visual-effects)
13. [Download & Export Options](#download--export-options)
14. [Accessibility Features](#accessibility-features)
15. [Installation & Setup](#installation--setup)
16. [Usage Guide](#usage-guide)
17. [Sample Images Included](#sample-images-included)
18. [Known Limitations & Future Scope](#known-limitations--future-scope)

---

## 📖 Project Overview

**Kolam** is a traditional South Indian art form from Tamil Nadu where intricate geometric patterns are drawn with rice flour, primarily at home thresholds each morning. This project digitizes, preserves, and extends that art form with modern machine learning, computer vision, and speech technology.

The application is built as a **multi-mode Streamlit web app** that allows users to:
- Load, draw, upload, or conversationally create Kolam patterns
- Apply transformations like scale, rotation, and mirroring
- Generate entirely new patterns from an existing base using algorithmic methods
- Analyze the mathematical and topological properties of any pattern
- Interact with everything using voice commands via the **Chitra** assistant

---

## ✅ Key Features

- **6 distinct creation modes**: Predefined, Upload, Freehand, Kaleidoscope, Conversational, and Generative Design
- **Chitra Voice Assistant**: Full natural language interaction, voice command processing, and spoken audio feedback via Google TTS
- **Conversational Drawing**: Visually impaired users can say "draw a big circle in the center" and Chitra draws it
- **Generative Design**: Algorithmically generate new Kolam patterns using symmetry, complexity, and style parameters
- **Computer Vision pipeline**: Skeletonization, contour detection, and mask processing for pattern extraction
- **Mathematical Analysis**: Topological analysis (Euler characteristic, endpoints, crossings), graph theory via NetworkX, and symmetry detection
- **Kaleidoscope HTML tool**: A built-in 8-fold symmetry interactive HTML5 canvas for freehand kaleidoscope drawing
- **Glow Effect**: Real-time neon/glow effect preview on freehand drawings
- **SVG Export**: Scalable vector graphics export for high-quality printing
- **Grid Overlay**: Toggle a calibrated grid to assist with precise pattern placement

---

## 🛠️ Tech Stack

| Category | Library / Tool | Purpose |
|---|---|---|
| **Frontend / UI** | Streamlit | Multi-mode interactive web application |
| **Drawing Canvas** | streamlit-drawable-canvas | Interactive freehand drawing canvas in browser |
| **Voice Input** | streamlit-mic-recorder | Microphone recording in the Streamlit interface |
| **Speech Recognition** | SpeechRecognition (sr) | Converts spoken audio to text (Google + Sphinx fallback) |
| **Text-to-Speech** | gTTS (Google TTS) | Converts Chitra's responses to spoken audio |
| **Audio Playback** | playsound 1.2.2 | Plays generated audio responses from Chitra |
| **Computer Vision** | OpenCV (cv2) | Image loading, thresholding, skeletonization rendering, contour analysis |
| **Image Processing** | scikit-image (skimage) | Skeletonization, connected component labeling |
| **Data & Arrays** | NumPy | All array math, transformations, and point operations |
| **Curve Smoothing** | SciPy (splprep, splev) | B-spline interpolation for smooth path drawing |
| **Graph Theory** | NetworkX (optional) | Topological graph analysis of skeleton patterns |
| **Vector Graphics** | svgwrite (optional) | Generate scalable SVG output files |
| **Visualization** | Matplotlib | Static rendering of Kolam dot patterns |
| **Image Handling** | Pillow (PIL) | Image loading and drawing utilities |
| **HTML Components** | streamlit.components.v1 | Embedding the Kaleidoscope HTML5 canvas |
| **Base64 / IO** | base64, io (BytesIO) | In-memory image export and encoding |
| **Threading** | threading | Non-blocking audio playback in background threads |
| **File System** | os, time | Temp audio file management |
| **Regex** | re | Parsing numeric values from voice commands |
| **Language** | Python 3.x | Core programming language |

> ⚠️ `svgwrite` and `networkx` are **optional** — the app works without them, gracefully disabling those features.

---

## 📁 Project Structure

```
Kolam-and-Kaleidoscope-Designer-with-Chitra/
│
├── kolam.py                  # Main Streamlit application (all modes, Chitra, analysis)
├── simple kolam.jpg          # Sample predefined Kolam — Simple pattern
├── lotus kolam.jpg           # Sample predefined Kolam — Lotus pattern
├── star kolam.jpg            # Sample predefined Kolam — Star pattern
└── .gitattributes            # Git line-ending configuration
```

---

## 🖥️ Application Modes

The app has **6 modes**, selectable via a sidebar radio button:

```
Predefined Kolam
Upload Image
Draw Freehand
Kaleidoscope Draw
Conversational Drawing   ← Accessibility mode
Generative Design        ← AI-powered creation
```

---

### 1. 📚 Predefined Kolam

**Purpose:** Load one of three bundled Kolam images (Simple, Lotus, Star) for transformation and analysis.

**How it works:**
1. Reads the image from disk using OpenCV
2. Converts to grayscale and applies **Otsu's thresholding** to binarize the image
3. Runs **skeletonization** (scikit-image) to reduce strokes to a single-pixel-wide path
4. Extracts `(x, y)` coordinates from skeleton pixels as a point cloud
5. The point cloud is then transformed, visualized, and made available for analysis or generation

---

### 2. 📁 Upload Image

**Purpose:** Let users upload their own Kolam photograph or scan.

**Process:**
1. User uploads a PNG/JPG file through Streamlit's file uploader
2. Bytes are decoded with `np.frombuffer` and `cv2.imdecode`
3. Same pipeline as Predefined mode: grayscale → threshold → skeletonize → points
4. Chitra gives voice confirmation on success or failure

---

### 3. ✏️ Draw Freehand

**Purpose:** Let users draw Kolam strokes directly on an interactive canvas.

**Features:**
- `streamlit-drawable-canvas` provides a `freedraw` canvas
- **Reference Image Uploader**: Upload a Kolam image alongside the canvas as a visual tracing guide
- **Stroke Width** slider and **Smoothing** slider (uses SciPy B-spline interpolation via `splprep`/`splev`)
- **Glow Effect toggle**: When enabled, the mask of drawn paths is processed with multi-scale Gaussian blur and `screen` composite blending to create a neon/glow appearance
- Glow color and intensity are configurable
- Glow preview displayed below canvas with PNG download option
- Path data is parsed from Streamlit canvas JSON, converted to NumPy arrays, and smoothed before use

---

### 4. 🌀 Kaleidoscope Draw

**Purpose:** Draw freehand patterns with automatic 8-fold kaleidoscopic symmetry.

**Implementation:**
- An entire custom HTML5/JavaScript application is embedded using `streamlit.components.v1.components.html()`
- Built as a single self-contained HTML string with inline CSS and JavaScript
- Uses an HTML5 `<canvas>` element with a custom `KaleidoscopeDraw` JavaScript class
- **8-fold symmetry**: Each stroke is rotated 8 times and reflected, producing 16 total mirrored segments
- Supports 10 colors including a rainbow mode (computed with `hsl()`)
- Glow effect is achieved via `ctx.shadowBlur` and `globalCompositeOperation = 'screen'`
- "Done" button exports the canvas as a downloadable PNG
- Designed for touch screen support as well as mouse

---

### 5. 🗣️ Conversational Drawing

**Purpose:** Accessibility mode for visually impaired users to create art entirely through voice or text commands.

**How it works:**
1. User says or types commands like "draw a big circle in the center" or "add a line from left to right"
2. `parse_and_execute_drawing_command()` parses the natural language:
   - Detects **shape** keywords: `circle`, `square`, `line`
   - Detects **size** keywords: `tiny`, `small`, `medium`, `large`, `huge`
   - Detects **position** keywords: `center`, `top left`, `bottom right`, `left`, `right`, etc.
3. Shape objects are stored as dictionaries in `st.session_state.drawn_objects`
4. Each shape is **rendered to a temporary OpenCV image** and displayed
5. `render_drawn_objects_to_points()` converts rendered shapes to a skeleton point cloud for further processing
6. Supports `undo`, `clear drawing`, and `start over` commands

---

### 6. 🔮 Generative Design

**Purpose:** Algorithmically generate a new, unique Kolam design based on an existing pattern.

**User Controls:**
- **Symmetry Order** (2–16): Number of rotational segments in the generated pattern
- **Complexity** (1–10): Controls density and elaborateness of style effects
- **Generation Style**: `loopy`, `spiky`, or `floral` (each applies a different mathematical transform)
- **Variation/Randomness** (0–0.5): Adds Gaussian noise for an organic feel
- Triggerable via button or Chitra voice command: "generate now"

See the [Generative Design Algorithm](#generative-design-algorithm) section for full technical details.

---

## 🎤 Chitra — Voice Assistant

**Chitra** is the core accessibility feature of this project. She is a voice-interactive AI assistant built into the sidebar.

### Architecture

```
User speaks → mic_recorder → audio bytes
→ sr.Recognizer (Google Speech API → Sphinx fallback)
→ transcribed text
→ handle_chat_prompt()
→ VOICE_COMMANDS lookup / regex parsing
→ Session state update
→ gTTS (Google TTS, Indian English accent: tld='co.in')
→ playsound() in background thread
→ st.info() text display
```

### Activation
- Chitra must be explicitly activated using a "🚀 Activate Chitra" button
- On first activation, she plays a personalized welcome message

### Voice Command System

Chitra understands 50+ voice commands organized into these categories:

| Category | Example Commands |
|---|---|
| **Navigation** | "predefined", "upload", "draw", "kaleidoscope", "conversational drawing", "generative design" |
| **Pattern Selection** | "simple", "lotus", "star" |
| **Scale** | "bigger", "smaller", "large", "tiny", "normal size" |
| **Rotation** | "turn right", "turn left", "flip", "upside down" |
| **Background Colors** | "red background", "blue background", "black background" |
| **Dot Size** | "small dots", "medium dots", "big dots", "huge dots" |
| **Mirroring** | "mirror horizontal", "mirror vertical", "no mirror" |
| **Grid** | "show grid", "hide grid" |
| **Generative** | "set symmetry to 8", "increase complexity", "use a floral style", "generate now" |
| **Actions** | "analyze", "save", "clear", "undo", "reset", "help" |

### Text Chat
- In addition to voice, users can type messages directly to Chitra via a `st.chat_input` widget
- Full conversation history is maintained in `st.session_state.messages` and displayed in the sidebar

---

## 🔬 Preprocessing & Computer Vision Pipeline

For any mode that produces a displayable Kolam, the following pipeline runs:

```
Input (image / canvas / shapes)
         │
         ▼
  Grayscale Conversion (cv2.cvtColor)
         │
         ▼
  Otsu's Binarization (cv2.threshold)
         │
         ▼
  Skeletonization (skimage.morphology.skeletonize)
         │
         ▼
  Point Extraction → np.array of (x, y) coordinates
         │
         ▼
  Transformation (scale, rotation via rotation matrix)
         │
         ▼
  Mirroring (horizontal / vertical reflection about center)
         │
         ▼
  Matplotlib Scatter Rendering (draw_kolam_static)
```

**Smoothing** (Freehand mode only): SciPy B-spline interpolation (`splprep`/`splev`) is applied to smooth jagged canvas paths before point extraction.

---

## 🧬 Generative Design Algorithm

The `generate_new_kolam()` function takes an existing point cloud and creates a new pattern:

**Step-by-step:**

1. **Centering**: Shifts all points to be centered around the origin
2. **Distance Normalization**: Computes each point's distance from center for scale-aware effects
3. **Symmetry Loop**: Iterates `symmetry_order` times, rotating the base pattern by `2π/n` for each sector
4. **Style Application** — one of three modes:
   - **`loopy`**: Adds a small circle of points around each base point; loop radius scales with distance from center
   - **`spiky`**: Creates a line of interpolated points from each base point toward the center, creating a spike effect
   - **`floral`**: Generates petal-shaped curves using `sin²` functions along the direction vector from the origin, with perpendicular offset
5. **Noise Addition**: Gaussian noise (`np.random.rand`) scaled by `variation * max_dist` is added for organic randomness
6. **Re-centering**: Final points are translated back to the original center position

---

## 📊 Kolam Analysis Engine

Triggered by the "🔍 Analyze Kolam" button (or Chitra's "analyze" command), the analysis runs in three tabs:

### Tab 1 — Technical Analysis

- **Connected Components**: `skimage.measure.label` counts separate disconnected regions
- **Skeleton Metrics**: Pixel count of the mathematical skeleton
- **Graph Theory** (via NetworkX):
  - Builds a graph from skeleton pixels with adjacency edges
  - Counts **endpoints** (degree 1), **T-junctions** (degree 3), **crossings** (degree ≥ 4)
  - Computes **Euler Characteristic** (V − E), a fundamental topological invariant
  - Calculates **average node degree** as a connectivity measure
  - Detects graph **cycles**
- **Geometry**: Contour area, perimeter, and **compactness** = `4π × area / perimeter²`

### Tab 2 — Educational Insights

- Pattern overview (unity vs. multi-component)
- Identified mathematical concepts with explanations (Topology, Graph Theory, Euler Characteristic, Symmetry)
- Geometric properties: shape compactness, aspect ratio, proportion
- Cultural significance of Kolam in Tamil Nadu tradition

### Tab 3 — Visual Analysis

- **Pattern Structure**: Binary mask visualization showing the overall form
- **Skeleton Analysis**: Single-pixel-width skeleton showing the core mathematical structure

### Symmetry Detection

`calculate_symmetry_properties()` detects the most likely rotational symmetry order:
- Computes polar angles of all points relative to the centroid
- Divides the 360° space into sectors for each candidate order (2, 3, 4, 5, 6, 8, 12)
- Uses standard deviation of sector point counts as a uniformity score
- Reports the best-fit symmetry order and a confidence value (0–1)

---

## 🌈 Kaleidoscope Drawing Tool

The embedded HTML5 Kaleidoscope tool is a complete standalone drawing app:

**JavaScript class: `KaleidoscopeDraw`**

- **8-fold symmetry**: Each stroke is rendered at 8 rotation angles (`2π × i / 8`) plus reflections
- **Glow rendering**: Uses `ctx.shadowBlur` with `globalCompositeOperation = 'screen'` for a luminous effect
- **Color palette**: 9 solid colors + rainbow mode (hue computed from `Math.atan2` angle relative to center)
- **Touch support**: Handles both mouse events and touch events for mobile/tablet drawing
- **Save**: Canvas exported as PNG via `canvas.toDataURL()`

---

## ✨ Visual Effects

### Glow Effect (Freehand Mode)

`apply_glow_effect()` creates a neon/glow appearance on any drawn mask:

1. Converts the hex glow color to BGR values
2. Normalizes the mask to float [0, 1]
3. Creates a colored layer from the mask
4. Applies **three Gaussian blurs at increasing kernel sizes** (9, 21, 41 pixels) and sums them for a multi-layer glow
5. Normalizes the glow layer and adds it to the original sharp stroke
6. Clips the result and returns an 8-bit BGR image

### Color Gradient Mode

When the user selects "Color Gradient" in the control panel, Matplotlib's `scatter()` is called with `c = np.arange(len(points))` and a chosen colormap (viridis, plasma, inferno, magma, cividis, rainbow, jet), producing a multi-color gradient through the pattern.

---

## 💾 Download & Export Options

| Format | Description | Available In |
|---|---|---|
| **PNG (300 DPI)** | High-resolution rasterized Kolam | All modes with pattern |
| **SVG** | Scalable vector graphics (circles per point) | All modes (requires svgwrite) |
| **Glow PNG** | Neon-style glow effect render | Freehand mode |
| **Generated PNG** | Output of the Generative Design | Generative Design mode |
| **Kaleidoscope PNG** | Screenshot of Kaleidoscope canvas | Kaleidoscope mode |

---

## ♿ Accessibility Features

This project was built with accessibility as a primary goal:

- **Voice Commands**: 50+ commands covering all app functions
- **Audio Feedback**: Every Chitra response is also spoken aloud (Indian English female voice via gTTS)
- **Conversational Drawing**: Visually impaired users can create art entirely through speech
- **Keyboard Accessible**: All Streamlit controls support keyboard navigation
- **Text Chat Fallback**: Type to Chitra if microphone is unavailable
- **High Contrast Options**: Black/white background and custom dot colors
- **Grid Overlay**: Helps users with spatial difficulties align patterns

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip
- Internet connection (for Google Speech Recognition and gTTS)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/your-username/Kolam-and-Kaleidoscope-Designer-with-Chitra.git
cd Kolam-and-Kaleidoscope-Designer-with-Chitra
```

### Step 2 — Install Dependencies

```bash
pip install streamlit opencv-python scikit-image scipy networkx \
            streamlit-mic-recorder SpeechRecognition gtts playsound==1.2.2 \
            svgwrite matplotlib streamlit-drawable-canvas Pillow
```

> `networkx` and `svgwrite` are optional — the app gracefully disables their features if not installed.

### Step 3 — Update Image Paths

In `kolam.py`, update the `PREMADE_PATTERNS` dictionary to point to images in the same folder:

```python
PREMADE_PATTERNS = {
    "Simple Kolam": "simple kolam.jpg",
    "Lotus Kolam":  "lotus kolam.jpg",
    "Star Kolam":   "star kolam.jpg"
}
```

### Step 4 — Run the App

```bash
streamlit run kolam.py
```

Open your browser at `http://localhost:8501`.

---

## 📋 Usage Guide

1. **Open the app** at `http://localhost:8501`
2. Click **"🚀 Activate Chitra"** — she will greet you with a voice welcome
3. Pick a mode from the sidebar:
   - **Predefined** → choose Simple / Lotus / Star
   - **Upload** → upload your own Kolam image
   - **Freehand** → draw on the canvas; use Reference Image for tracing
   - **Kaleidoscope** → draw with 8-fold symmetry in the embedded tool
   - **Conversational** → tell Chitra to "draw a circle" or "add a square"
   - **Generative** → tweak parameters and click "Generate New Design"
4. Use the **sidebar controls** to change colors, dot size, scale, rotation, mirroring, and grid
5. Click **"🔍 Analyze Kolam"** for a full mathematical and cultural breakdown
6. Download your creation as PNG or SVG

---

## 🖼️ Sample Images Included

| File | Description |
|---|---|
| `simple kolam.jpg` | A basic, minimal Kolam for beginners |
| `lotus kolam.jpg` | A floral Lotus-inspired Kolam design |
| `star kolam.jpg` | A geometric star-pattern Kolam |

---

## ⚠️ Known Limitations & Future Scope

### Limitations

- Predefined pattern file paths are hardcoded with absolute Windows paths — must be updated manually
- `playsound==1.2.2` may have compatibility issues on some Linux/Mac systems
- Google Speech Recognition and gTTS require an active internet connection
- The Kaleidoscope HTML tool's output cannot currently be fed back into the analysis pipeline
- `use_column_width=True` is a deprecated Streamlit parameter (should be `use_container_width`)
- Conversational drawing supports only basic shapes (circle, square, line)

### Future Scope

- Add a color picker for conversational drawing ("draw a red circle")
- Enable Kaleidoscope output to be imported into the analysis and generative modes
- Add more Kolam patterns to the predefined library
- Support Tamil voice commands for native speakers
- Offline TTS fallback (pyttsx3) when internet is unavailable
- Web deployment on Streamlit Cloud or Hugging Face Spaces
- Mobile-optimized responsive layout
- More generative styles (geometric, mandala, spiral)
- Pattern sharing and community gallery feature

---

## 🏛️ About Kolam

Kolam is a traditional South Indian art form primarily practiced in Tamil Nadu. These geometric patterns are drawn daily at dawn with rice flour at home thresholds, serving both aesthetic and spiritual purposes. They embody deep mathematical principles including **Topology**, **Graph Theory**, **Symmetry**, and **Fractals**. This application helps preserve and study this beautiful mathematical art form while making it accessible to everyone through natural conversation and voice interaction.

---

## 👨‍💻 Authors

Developed as an academic project focused on accessible art creation and the intersection of traditional culture with modern AI and computer vision technology.

---

## 📜 License

This project is intended for educational and research purposes. Please check with the project authors before any commercial use.