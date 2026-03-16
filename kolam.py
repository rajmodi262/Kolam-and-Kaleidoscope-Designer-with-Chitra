# REQUIRED LIBRARIES:
# pip install streamlit opencv-python scikit-image scipy networkx streamlit-mic-recorder SpeechRecognition gtts playsound==1.2.2 svgwrite matplotlib streamlit-drawable-canvas Pillow

import streamlit as st
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage.morphology import skeletonize
from io import BytesIO
from streamlit_drawable_canvas import st_canvas
from scipy.interpolate import splprep, splev
from skimage.measure import label
import streamlit.components.v1 as components
import re
import speech_recognition as sr
from streamlit_mic_recorder import mic_recorder
import threading
import time
import math
import os
from gtts import gTTS
from playsound import playsound
from PIL import Image, ImageDraw
import base64
import io

# Vector graphics support
try:
    import svgwrite
    SVG_AVAILABLE = True
except ImportError:
    SVG_AVAILABLE = False

# A friendly attempt to import networkx if available
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

# ---- App Configuration ----
st.set_page_config(layout="wide", page_title="Accessible Kolam Designer with Chitra")

# ---- Chitra Voice Assistant Configuration ----
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = True
if 'chitra_activated' not in st.session_state:
    st.session_state.chitra_activated = False

def speak_text(text):
    """Chitra's voice using Google TTS for consistent female voice"""
    if st.session_state.get('voice_enabled', True):
        st.info(f"Chitra: {text}")
        try:
            # Create the text-to-speech object with a female English voice
            tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
            
            # Save the speech to a temporary mp3 file
            audio_file = f"chitra_response_{int(time.time())}.mp3"
            tts.save(audio_file)
            
            # Play the audio file in a separate thread to avoid blocking
            def play_audio():
                try:
                    playsound(audio_file)
                    # Clean up the temporary file
                    if os.path.exists(audio_file):
                        os.remove(audio_file)
                except:
                    pass
            
            thread = threading.Thread(target=play_audio)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            st.warning(f"Chitra's voice is temporarily unavailable. Internet connection may be required. Error: {e}")

# ---- Predefined Kolam Library ----
PREMADE_PATTERNS = {
    "Simple Kolam": r"C:\Users\prati\Downloads\simple kolam.jpg",
    "Lotus Kolam": r"C:\Users\prati\Downloads\lotus kolam.jpg",
    "Star Kolam": r"C:\Users\prati\Downloads\star kolam.jpg"
}

# ---- Enhanced Voice Command Mappings ----
VOICE_COMMANDS = {
    # Navigation and Mode Commands
    "predefined": "predefined kolam",
    "upload": "upload image",
    "draw": "draw freehand", 
    "freehand": "draw freehand",
    "kaleidoscope": "kaleidoscope draw",
    "conversational drawing": "conversational drawing",
    "draw for me": "conversational drawing",
    "generative design": "generative design", # New Command
    "create a new design": "generative design", # New Command
    
    # Kolam Selection
    "simple": "simple kolam",
    "lotus": "lotus kolam", 
    "star": "star kolam",
    
    # Transformations
    "bigger": "scale 1.5",
    "smaller": "scale 0.7",
    "large": "scale 2.0",
    "tiny": "scale 0.5",
    "normal size": "scale 1.0",
    
    # Rotations
    "turn right": "rotate 90",
    "turn left": "rotate -90", 
    "flip": "rotate 180",
    "upside down": "rotate 180",
    
    # Colors
    "black background": "background #000000",
    "white background": "background #FFFFFF",
    "red background": "background #FF0000",
    "blue background": "background #0000FF",
    "green background": "background #00FF00",
    "yellow background": "background #FFFF00",
    "purple background": "background #800080",
    
    # Dot properties
    "small dots": "dot size 3",
    "big dots": "dot size 15", 
    "medium dots": "dot size 8",
    "huge dots": "dot size 25",
    
    # Mirroring
    "mirror horizontal": "horizontal mirror on",
    "mirror vertical": "vertical mirror on",
    "no mirror": "mirror off",
    
    # Grid
    "show grid": "grid on",
    "hide grid": "grid off",
    
    # Analysis and Actions
    "analyze": "analyze kolam",
    "analyse": "analyze kolam",
    "analyze kolam": "analyze kolam",
    "analyze this kolam": "analyze kolam",
    "analyze column": "analyze kolam",
    "analyze this column": "analyze kolam",
    "generate now": "generate now", # New Command
    "save": "download kolam",
    "clear": "clear canvas",
    "undo": "undo",
    "undo last drawing": "undo",
    "reset drawing": "clear drawing",
    "help": "help",
    "reset": "reset all"
}

# ---- Kaleidoscope HTML Component ----
kaleidoscope_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Kaleidoscope Draw Pattern</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; } body { background: #000; color: #fff; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; height: 100vh; display: flex; flex-direction: column; } .header { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; background: rgba(20, 20, 20, 0.9); } .header h1 { font-size: 18px; font-weight: 500; } .btn { background: none; border: none; color: #fff; font-size: 16px; cursor: pointer; padding: 8px 15px; border-radius: 8px; } .btn.cancel { color: #FF453A; } .btn.done { background: #007AFF; color: #fff; } .canvas-area { flex: 1; display: flex; justify-content: center; align-items: center; position: relative; } #canvas { border: 2px dotted #333; border-radius: 15px; cursor: crosshair; background: #000; touch-action: none; } .controls { position: absolute; bottom: 30px; left: 50%; transform: translateX(-50%); background: rgba(30, 30, 30, 0.95); border-radius: 25px; padding: 25px; backdrop-filter: blur(20px); } .color-row { display: flex; justify-content: center; gap: 12px; margin-bottom: 25px; } .color { width: 45px; height: 45px; border-radius: 50%; cursor: pointer; border: 3px solid transparent; transition: all 0.2s ease; } .color.active { border-color: #fff; transform: scale(1.15); } .tool-row { display: flex; gap: 15px; align-items: center; justify-content: center; } .tool-btn { background: rgba(255, 255, 255, 0.1); border: none; color: #fff; padding: 12px 20px; border-radius: 12px; cursor: pointer; font-size: 14px; transition: all 0.2s ease; } .tool-btn:hover { background: rgba(255, 255, 255, 0.2); }
    </style>
</head>
<body>
    <div class="header"><button class="btn cancel" onclick="clearAll()">Cancel</button><h1>Draw pattern</h1><button class="btn done" onclick="saveImage()">Done</button></div>
    <div class="canvas-area">
        <canvas id="canvas" width="700" height="700"></canvas>
        <div class="controls">
            <div class="color-row"><div class="color" style="background: #FFFFFF" data-color="#FFFFFF"></div><div class="color" style="background: #FF2D92" data-color="#FF2D92"></div><div class="color" style="background: #FF8C00" data-color="#FF8C00"></div><div class="color" style="background: #FFFF00" data-color="#FFFF00"></div><div class="color active" style="background: #00FF88" data-color="#00FF88"></div><div class="color" style="background: #00BFFF" data-color="#00BFFF"></div><div class="color" style="background: #6A5ACD" data-color="#6A5ACD"></div><div class="color" style="background: #D3D3D3" data-color="#D3D3D3"></div><div class="color" style="background: #9932CC" data-color="#9932CC"></div><div class="color" style="background: conic-gradient(red, yellow, green, cyan, blue, magenta, red)" data-color="rainbow"></div></div>
            <div class="tool-row"><button class="tool-btn" onclick="clearAll()">Clear</button><button class="tool-btn" onclick="generateRandom()">Random</button></div>
        </div>
    </div>
    <script>
        class KaleidoscopeDraw{constructor(){this.canvas=document.getElementById('canvas');this.ctx=this.canvas.getContext('2d');this.drawing=!1;this.currentStroke=[];this.centerX=this.canvas.width/2;this.centerY=this.canvas.height/2;this.symmetryCount=8;this.currentColor='#00FF88';this.brushSize=4;this.glowSize=8;this.initCanvas();this.setupEvents();this.setupColorPicker()}
        initCanvas(){this.ctx.lineCap='round';this.ctx.lineJoin='round';this.ctx.globalCompositeOperation='screen'}
        setupEvents(){this.canvas.onmousedown=e=>this.startDraw(e);this.canvas.onmousemove=e=>this.draw(e);this.canvas.onmouseup=()=>this.endDraw();this.canvas.onmouseleave=()=>this.endDraw();this.canvas.ontouchstart=e=>{e.preventDefault();this.startDraw(e.touches[0])};this.canvas.ontouchmove=e=>{e.preventDefault();this.draw(e.touches[0])};this.canvas.ontouchend=e=>{e.preventDefault();this.endDraw()}}
        setupColorPicker(){document.querySelectorAll('.color').forEach(e=>{e.onclick=()=>{document.querySelectorAll('.color').forEach(e=>e.classList.remove('active'));e.classList.add('active');this.currentColor=e.dataset.color}})}
        getPosition(e){const t=this.canvas.getBoundingClientRect();return{x:(e.clientX-t.left)*(this.canvas.width/t.width),y:(e.clientY-t.top)*(this.canvas.height/t.height)}}
        startDraw(e){this.drawing=!0;const t=this.getPosition(e);this.currentStroke=[t];this.drawKaleidoscopePoint(t)}
        draw(e){if(!this.drawing)return;const t=this.getPosition(e),o=this.currentStroke[this.currentStroke.length-1];this.currentStroke.push(t);this.drawKaleidoscopeLine(o,t)}
        endDraw(){this.drawing=!1;this.currentStroke=[]}
        drawKaleidoscopePoint(e){const t=e.x-this.centerX,o=e.y-this.centerY;for(let s=0;s<this.symmetryCount;s++){const i=2*Math.PI*s/this.symmetryCount,r=t*Math.cos(i)-o*Math.sin(i),c=t*Math.sin(i)+o*Math.cos(i),h=this.centerX+r,a=this.centerY+c;this.drawGlowPoint(h,a);this.drawGlowPoint(h,this.centerY-c)}}
        drawKaleidoscopeLine(e,t){const o=e.x-this.centerX,s=e.y-this.centerY,i=t.x-this.centerX,r=t.y-this.centerY;for(let c=0;c<this.symmetryCount;c++){const h=2*Math.PI*c/this.symmetryCount,a=Math.cos(h),n=Math.sin(h),d=o*a-s*n,l=o*n+s*a,p=i*a-r*n,k=i*n+r*a,g=this.centerX+d,x=this.centerY+l,w=this.centerX+p,y=this.centerY+k;this.drawGlowLine(g,x,w,y);this.drawGlowLine(g,this.centerY-l,w,this.centerY-k)}}
        drawGlowPoint(e,t){const o=this.getColor(e,t);this.ctx.shadowColor=o;this.ctx.shadowBlur=this.glowSize;this.ctx.fillStyle=o;this.ctx.beginPath();this.ctx.arc(e,t,this.brushSize/2,0,2*Math.PI);this.ctx.fill();this.ctx.shadowBlur=0}
        drawGlowLine(e,t,o,s){const i=this.getColor(e,t);this.ctx.strokeStyle=i;this.ctx.lineWidth=this.brushSize;this.ctx.shadowColor=i;this.ctx.shadowBlur=this.glowSize;this.ctx.beginPath();this.ctx.moveTo(e,t);this.ctx.lineTo(o,s);this.ctx.stroke();this.ctx.shadowBlur=0}
        getColor(e,t){if('rainbow'===this.currentColor){const o=Math.atan2(t-this.centerY,e-this.centerX);return`hsl(${360*((o+Math.PI)/(2*Math.PI))}, 90%, 65%)`}return this.currentColor}
        clear(){this.ctx.clearRect(0,0,this.canvas.width,this.canvas.height)}}
        const kaleidoscope=new KaleidoscopeDraw;function clearAll(){kaleidoscope.clear()}function generateRandom(){kaleidoscope.random()}function saveImage(){const e=document.createElement('a');e.download='kaleidoscope-pattern.png';e.href=kaleidoscope.canvas.toDataURL();e.click()}
    </script>
</body>
</html>
"""

# ---- Enhanced Speech Recognition ----
def transcribe_audio(audio_data):
    """Enhanced audio transcription with better error handling"""
    if not audio_data: 
        return None
    
    r = sr.Recognizer()
    try:
        audio = sr.AudioData(audio_data["bytes"], audio_data["sample_rate"], audio_data["sample_width"])
        # Try Google Speech Recognition
        try:
            text = r.recognize_google(audio)
            return text.lower()
        except sr.RequestError:
            # Fallback to offline recognition if available
            try:
                text = r.recognize_sphinx(audio)
                return text.lower()
            except:
                return None
    except sr.UnknownValueError:
        return None
    except Exception as e:
        st.error(f"Audio processing error: {e}")
        return None

# ---- Session State Initialization ----
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Chitra, your voice-enabled Kolam assistant. Click 'Activate Chitra' to begin, then I can help you create beautiful patterns using voice commands!"}
    ]
if 'bg_color' not in st.session_state: st.session_state.bg_color = "#FFFFFF"
if 'dot_size' not in st.session_state: st.session_state.dot_size = 5
if 'opacity' not in st.session_state: st.session_state.opacity = 1.0
if 'scale' not in st.session_state: st.session_state.scale = 1.0
if 'rotation' not in st.session_state: st.session_state.rotation = 0
if 'current_mode' not in st.session_state: st.session_state.current_mode = "Predefined Kolam"
if 'current_pattern' not in st.session_state: st.session_state.current_pattern = "Simple Kolam"
if 'horizontal_mirror' not in st.session_state: st.session_state.horizontal_mirror = False
if 'vertical_mirror' not in st.session_state: st.session_state.vertical_mirror = False
if 'fill_shape' not in st.session_state: st.session_state.fill_shape = False
if 'show_grid' not in st.session_state: st.session_state.show_grid = False
if 'voice_feedback' not in st.session_state: st.session_state.voice_feedback = True
if 'dot_color_style' not in st.session_state: st.session_state.dot_color_style = "Solid Color"
if 'solid_dot_color' not in st.session_state: st.session_state.solid_dot_color = "#000000"
if 'drawn_objects' not in st.session_state: st.session_state.drawn_objects = []
if 'generated_points' not in st.session_state: st.session_state.generated_points = None
if 'gen_symmetry' not in st.session_state: st.session_state.gen_symmetry = 6
if 'gen_complexity' not in st.session_state: st.session_state.gen_complexity = 3
if 'gen_style' not in st.session_state: st.session_state.gen_style = 'loopy'
if 'gen_variation' not in st.session_state: st.session_state.gen_variation = 0.1
if 'base_points_for_generation' not in st.session_state: st.session_state.base_points_for_generation = None


# ---- Conversational Drawing Logic ----
def parse_and_execute_drawing_command(prompt):
    """Parses drawing commands and updates the state for conversational drawing."""
    width, height = 600, 600 # Standard canvas size for this mode
    
    # Actions
    if "undo" in prompt or "remove last" in prompt:
        if st.session_state.drawn_objects:
            st.session_state.drawn_objects.pop()
            return "Okay, I've removed the last shape you added."
        else:
            return "There's nothing to undo. The canvas is empty."
            
    if "clear drawing" in prompt or "reset drawing" in prompt or "start over" in prompt:
        st.session_state.drawn_objects = []
        return "The canvas is cleared. Let's start a new drawing!"

    # Drawing commands
    if "draw" in prompt or "add" in prompt or "create" in prompt:
        shape = None
        if "circle" in prompt: shape = "circle"
        elif "square" in prompt: shape = "square"
        elif "line" in prompt: shape = "line"
        
        if not shape:
            return "I can draw a circle, square, or line. What would you like?"

        # Default properties
        size_map = {"tiny": 20, "small": 50, "medium": 100, "large": 150, "big": 150, "huge": 200}
        size_val = size_map["medium"]
        for s, v in size_map.items():
            if s in prompt:
                size_val = v
                break
        
        margin = 50
        pos_map = {
            "center": (width//2, height//2),
            "top left": (margin + size_val//2, margin + size_val//2),
            "top right": (width - margin - size_val//2, margin + size_val//2),
            "bottom left": (margin + size_val//2, height - margin - size_val//2),
            "bottom right": (width - margin - size_val//2, height - margin - size_val//2),
            "top": (width//2, margin + size_val//2),
            "bottom": (width//2, height - margin - size_val//2),
            "left": (margin + size_val//2, height//2),
            "right": (width - margin - size_val//2, height//2)
        }
        position = pos_map["center"]
        for p_name, p_coords in pos_map.items():
            if p_name in prompt:
                position = p_coords
                break

        obj = {'type': shape, 'color': (0,0,0)}

        if shape == "circle":
            obj.update({'center': position, 'radius': size_val // 2})
            st.session_state.drawn_objects.append(obj)
            return f"Done. I've drawn a circle for you."
        
        if shape == "square":
            top_left = (position[0] - size_val//2, position[1] - size_val//2)
            bottom_right = (position[0] + size_val//2, position[1] + size_val//2)
            obj.update({'top_left': top_left, 'bottom_right': bottom_right})
            st.session_state.drawn_objects.append(obj)
            return f"Okay, I've added a square."

        if shape == "line":
            start_pos, end_pos = (margin, margin), (width - margin, height - margin) # Default diagonal
            if "from top to bottom" in prompt or "vertical" in prompt:
                start_pos, end_pos = (width//2, margin), (width//2, height-margin)
            if "from left to right" in prompt or "horizontal" in prompt:
                start_pos, end_pos = (margin, height//2), (width-margin, height//2)
            obj.update({'start': start_pos, 'end': end_pos})
            st.session_state.drawn_objects.append(obj)
            return f"I've drawn a line as you requested."

    return "I'm ready to draw for you. Please tell me what to draw, for example: 'draw a big circle in the center'."

# ---- Enhanced Chat Logic with Chitra's Personality ----
def handle_chat_prompt(prompt):
    """Enhanced chat handling with Chitra's personality and comprehensive voice commands"""
    prompt_lower = prompt.lower().strip()
    
    # Normalize command using mappings
    normalized_command = VOICE_COMMANDS.get(prompt_lower, prompt_lower)
    
    response = "I didn't quite understand that command. Please say 'help' and I'll tell you what I can do for you."
    
    # Handle conversational drawing if in that mode
    if st.session_state.current_mode == "Conversational Drawing":
        response = parse_and_execute_drawing_command(normalized_command)
        speak_text(response)
        return response

    # Extract numbers from prompt
    numbers = re.findall(r'-?\d+\.?\d*', normalized_command)
    value = float(numbers[0]) if numbers else None
    
    # Help command
    if "help" in normalized_command:
        response = """Hello! I'm Chitra, and here's what I can help you with:
        
**Navigation**: Say 'predefined', 'upload', 'draw', 'kaleidoscope', 'conversational drawing', or 'generative design'.
**Patterns**: Say 'simple', 'lotus', or 'star'.
**Size**: Say 'bigger', 'smaller', 'large', 'tiny', or 'normal size'.
**Rotation**: Say 'turn right', 'turn left', 'flip', or 'upside down'.
**Colors**: Say '[color] background' like 'red background' or 'blue background'.
**Dots**: Say 'small dots', 'big dots', 'medium dots', or 'huge dots'.
**Mirror**: Say 'mirror horizontal', 'mirror vertical', or 'no mirror'. 
**Grid**: Say 'show grid' or 'hide grid'.
**Actions**: Say 'analyze', 'generate now', 'save', 'clear', 'undo', or 'reset'.

When in 'Generative Design' mode, you can say 'set symmetry to 8' or 'use a spiky style'.
I'm here to make creating Kolam patterns easy and accessible. What would you like to create?"""
        speak_text("Here are all the commands I understand. I'm ready to help you create something beautiful!")
    
    # Mode switching
    elif any(mode in normalized_command for mode in ["predefined", "upload", "draw freehand", "kaleidoscope", "conversational drawing", "generative design"]):
        if "predefined" in normalized_command:
            st.session_state.current_mode = "Predefined Kolam"
            response = "Perfect! I've switched to predefined Kolam mode. Say 'simple', 'lotus', or 'star' to choose a beautiful pattern."
        elif "upload" in normalized_command:
            st.session_state.current_mode = "Upload Image"
            response = "Great choice! I've switched to upload mode. Please upload an image file and I'll help you work with it."
        elif "kaleidoscope" in normalized_command:
            st.session_state.current_mode = "Kaleidoscope Draw"
            response = "Wonderful! Kaleidoscope mode is now active. You can create symmetrical patterns that mirror beautifully."
        elif "draw" in normalized_command and "conversational" not in normalized_command:
            st.session_state.current_mode = "Draw Freehand"
            response = "Excellent! I've switched to freehand drawing mode. Use the canvas to draw your own unique pattern."
        elif "conversational drawing" in normalized_command:
            st.session_state.current_mode = "Conversational Drawing"
            st.session_state.drawn_objects = [] # Reset on mode switch
            response = "I'm ready to be your hands! Tell me what to draw. For example, say 'draw a circle'."
        elif "generative design" in normalized_command:
            st.session_state.current_mode = "Generative Design"
            response = "This is my favorite mode! I will create a new design based on your current kolam. You can change settings like symmetry and complexity, then say 'generate now'."
        speak_text(response)
    
    # Pattern selection
    elif any(pattern in normalized_command for pattern in ["simple", "lotus", "star"]):
        if "simple" in normalized_command:
            st.session_state.current_pattern = "Simple Kolam"
            response = "Beautiful choice! I've selected the Simple Kolam pattern for you."
        elif "lotus" in normalized_command:
            st.session_state.current_pattern = "Lotus Kolam"
            response = "Lovely! The Lotus Kolam is now selected. It's such an elegant pattern."
        elif "star" in normalized_command:
            st.session_state.current_pattern = "Star Kolam"
            response = "Wonderful! I've chosen the Star Kolam pattern. It has beautiful geometric symmetry."
        speak_text(response)
    
    # Scale commands
    elif "scale" in normalized_command and value is not None:
        st.session_state.scale = max(0.1, min(5.0, value))
        response = f"Perfect! I've set the scale to {st.session_state.scale}."
        speak_text(response)
    elif any(cmd in normalized_command for cmd in ["bigger", "smaller", "large", "tiny", "normal size"]):
        if "bigger" in normalized_command:
            st.session_state.scale = min(5.0, st.session_state.scale * 1.5)
            response = "Made it bigger! Your pattern should look larger now."
        elif "smaller" in normalized_command:
            st.session_state.scale = max(0.1, st.session_state.scale * 0.7)
            response = "Made it smaller! The pattern is now more compact."
        elif "large" in normalized_command:
            st.session_state.scale = 2.0
            response = "Set to large size! Your pattern will be quite prominent now."
        elif "tiny" in normalized_command:
            st.session_state.scale = 0.5
            response = "Made it tiny! Now you have a delicate, small pattern."
        elif "normal size" in normalized_command:
            st.session_state.scale = 1.0
            response = "Reset to normal size! Your pattern is back to its original scale."
        speak_text(response)
    
    # Rotation commands
    elif "rotate" in normalized_command and value is not None:
        st.session_state.rotation = int(value) % 360
        response = f"Done! I've rotated your pattern to {st.session_state.rotation} degrees."
        speak_text(response)
    elif any(cmd in normalized_command for cmd in ["turn right", "turn left", "flip", "upside down"]):
        if "turn right" in normalized_command:
            st.session_state.rotation = (st.session_state.rotation + 90) % 360
            response = "Turned right! Your pattern is now rotated 90 degrees clockwise."
        elif "turn left" in normalized_command:
            st.session_state.rotation = (st.session_state.rotation - 90) % 360
            response = "Turned left! Your pattern is now rotated 90 degrees counter-clockwise."
        elif "flip" in normalized_command or "upside down" in normalized_command:
            st.session_state.rotation = (st.session_state.rotation + 180) % 360
            response = "Flipped! Your pattern is now upside down from its original orientation."
        speak_text(response)
    
    # Background color commands  
    elif "background" in normalized_command:
        color_map = {
            "black": "#000000", "white": "#FFFFFF", "red": "#FF0000",
            "blue": "#0000FF", "green": "#00FF00", "yellow": "#FFFF00",
            "purple": "#800080", "orange": "#FFA500", "pink": "#FFC0CB"
        }
        for color_name, color_code in color_map.items():
            if color_name in normalized_command:
                st.session_state.bg_color = color_code
                response = f"Beautiful! I've changed the background to {color_name}. That will look lovely!"
                speak_text(response)
                break
    
    # Dot size commands
    elif "dot size" in normalized_command and value is not None:
        st.session_state.dot_size = max(1, min(50, int(value)))
        response = f"Perfect! I've set the dot size to {st.session_state.dot_size}."
        speak_text(response)
    elif any(cmd in normalized_command for cmd in ["small dots", "big dots", "medium dots", "huge dots"]):
        if "small dots" in normalized_command:
            st.session_state.dot_size = 3
            response = "Done! I've made the dots small and delicate."
        elif "medium dots" in normalized_command:
            st.session_state.dot_size = 8
            response = "Perfect! The dots are now medium-sized, nicely balanced."
        elif "big dots" in normalized_command:
            st.session_state.dot_size = 15
            response = "Great! I've made the dots bigger and more prominent."
        elif "huge dots" in normalized_command:
            st.session_state.dot_size = 25
            response = "Wonderful! The dots are now huge and will really stand out."
        speak_text(response)
    
    # Mirror commands
    elif "mirror" in normalized_command:
        if "horizontal" in normalized_command and "on" in normalized_command:
            st.session_state.horizontal_mirror = True
            response = "Enabled horizontal mirroring! Your pattern will reflect beautifully across the horizontal axis."
        elif "vertical" in normalized_command and "on" in normalized_command:
            st.session_state.vertical_mirror = True
            response = "Enabled vertical mirroring! Your pattern will reflect across the vertical axis."
        elif "off" in normalized_command or "no mirror" in normalized_command:
            st.session_state.horizontal_mirror = False
            st.session_state.vertical_mirror = False
            response = "Removed all mirroring. Your pattern is now displayed in its original form."
        speak_text(response)
    
    # Grid commands
    elif "grid" in normalized_command:
        if "on" in normalized_command or "show grid" in normalized_command:
            st.session_state.show_grid = True
            response = "Perfect! I've made the grid visible to help you see the pattern structure."
        elif "off" in normalized_command or "hide grid" in normalized_command:
            st.session_state.show_grid = False
            response = "Done! I've hidden the grid so you can see your pattern clearly."
        speak_text(response)
        
    # --- New Generative Commands ---
    elif "symmetry" in normalized_command and value is not None:
        st.session_state.gen_symmetry = max(2, min(16, int(value)))
        response = f"Generative symmetry set to {st.session_state.gen_symmetry}-fold."
        speak_text(response)
    elif "complexity" in normalized_command:
        if "increase" in normalized_command or "more" in normalized_command:
            st.session_state.gen_complexity = min(10, st.session_state.gen_complexity + 1)
        elif "decrease" in normalized_command or "less" in normalized_command:
            st.session_state.gen_complexity = max(1, st.session_state.gen_complexity - 1)
        response = f"Generative complexity is now {st.session_state.gen_complexity}."
        speak_text(response)
    elif "style" in normalized_command:
        if "loopy" in normalized_command: st.session_state.gen_style = 'loopy'
        elif "spiky" in normalized_command: st.session_state.gen_style = 'spiky'
        elif "floral" in normalized_command: st.session_state.gen_style = 'floral'
        response = f"Okay, I'll use a {st.session_state.gen_style} style for the next generation."
        speak_text(response)
    elif "generate now" in normalized_command:
        st.session_state['trigger_generation'] = True
        response = "On it! I'm creating a new design for you based on your settings. Here it comes!"
        speak_text(response)
    
    # Analysis command
    elif "analyze" in normalized_command:
        st.session_state['trigger_analysis'] = True
        response = "Certainly! Let me analyze your Kolam pattern for you. This will show you the mathematical beauty in your design."
        speak_text(response)
    
    # Reset command
    elif "reset" in normalized_command:
        st.session_state.scale = 1.0
        st.session_state.rotation = 0
        st.session_state.bg_color = "#FFFFFF"
        st.session_state.dot_size = 5
        st.session_state.opacity = 1.0
        st.session_state.horizontal_mirror = False
        st.session_state.vertical_mirror = False
        st.session_state.show_grid = False
        st.session_state.drawn_objects = []
        st.session_state.generated_points = None
        st.session_state.base_points_for_generation = None
        response = "All done! I've reset all your settings back to their defaults. Ready to start fresh!"
        speak_text(response)
    
    # Save/Download command
    elif "save" in normalized_command or "download" in normalized_command:
        response = "To save your beautiful creation, please use the download buttons below your pattern. You can save as PNG or SVG format!"
        speak_text(response)
    
    # Clear command
    elif "clear" in normalized_command:
        response = "Canvas is cleared! You have a fresh start to create something new and beautiful."
        speak_text(response)
    
    return response

# ---- NEW: Generative Design Function ----
def generate_new_kolam(base_points, symmetry_order=6, complexity=3, style='loopy', variation=0.1):
    """
    Generates a new Kolam design based on an existing set of points.
    """
    if base_points is None or len(base_points) < 2:
        return None

    center = np.mean(base_points, axis=0)
    # Normalize points by shifting them to be centered around the origin
    normalized_points = base_points - center

    all_generated_points = []

    # Get the distances of points from the center to use for scaling effects
    distances = np.linalg.norm(normalized_points, axis=1)
    max_dist = np.max(distances) if distances.size > 0 else 1.0

    for i in range(symmetry_order):
        angle = i * (2 * np.pi / symmetry_order)
        rot_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                               [np.sin(angle), np.cos(angle)]])
        
        # Rotate the entire base pattern for each symmetry sector
        rotated_base = normalized_points.dot(rot_matrix.T)
        
        sector_points = []
        for p, dist in zip(rotated_base, distances):
            # Add the base rotated point
            sector_points.append(p)

            # Apply style-based modifications
            if style == 'loopy':
                # Create a small loop/circle around each point
                radius = complexity * 2 * (dist / max_dist) # Scale loop size by distance from center
                num_loop_points = 8 + complexity
                loop_angles = np.linspace(0, 2 * np.pi, num_loop_points, endpoint=False)
                loop_x = p[0] + radius * np.cos(loop_angles)
                loop_y = p[1] + radius * np.sin(loop_angles)
                sector_points.extend(np.column_stack([loop_x, loop_y]))

            elif style == 'spiky':
                # Create a line of points from the point towards the center
                num_spike_points = complexity + 1
                spike = np.linspace(p, p * 0.5, num_spike_points)
                sector_points.extend(spike)

            elif style == 'floral':
                 # Create petal shapes originating from each point
                petal_length = complexity * 4 * (dist / max_dist)
                num_petal_points = 10 + complexity
                petal_shape = np.sin(np.linspace(0, np.pi, num_petal_points))**2
                
                # Angle of the point relative to origin
                point_angle = np.arctan2(p[1], p[0])
                
                # Create petal points along the direction from origin
                petal_radii = np.linspace(0, petal_length, num_petal_points)
                
                petal_x = p[0] + (petal_radii * np.cos(point_angle)) + (petal_shape * 5 * np.cos(point_angle + np.pi/2))
                petal_y = p[1] + (petal_radii * np.sin(point_angle)) + (petal_shape * 5 * np.sin(point_angle + np.pi/2))
                sector_points.extend(np.column_stack([petal_x, petal_y]))

        all_generated_points.append(np.array(sector_points))

    final_points = np.vstack(all_generated_points)
    
    # Add random variation for an organic feel
    if variation > 0:
        noise = (np.random.rand(*final_points.shape) - 0.5) * (max_dist * variation)
        final_points += noise

    # Translate points back to their original position
    return final_points + center

# ---- Utility Functions ---- (keeping all existing functions unchanged)
def render_drawn_objects_to_points(objects, width, height, thickness=5):
    """Renders shapes from a list onto an image and extracts points."""
    if not objects:
        return None
    
    # Create a blank image
    img = np.zeros((height, width), dtype=np.uint8)
    
    for obj in objects:
        if obj['type'] == 'circle':
            cv2.circle(img, obj['center'], obj['radius'], 255, thickness, lineType=cv2.LINE_AA)
        elif obj['type'] == 'square':
            cv2.rectangle(img, obj['top_left'], obj['bottom_right'], 255, thickness, lineType=cv2.LINE_AA)
        elif obj['type'] == 'line':
            cv2.line(img, obj['start'], obj['end'], 255, thickness, lineType=cv2.LINE_AA)
            
    # Now, convert this rendered image to points using skeletonization
    skeleton = skeletonize(img // 255).astype(np.uint8)
    y_coords, x_coords = np.where(skeleton)
    
    if y_coords.size > 0:
        return np.vstack((x_coords, y_coords)).T
    return None

def load_pattern_as_points(file_path):
    try:
        img = cv2.imread(file_path)
        if img is None: return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        skeleton = skeletonize(thresh // 255).astype(np.uint8)
        y_coords, x_coords = np.where(skeleton)
        return np.vstack((x_coords, y_coords)).T
    except Exception:
        st.error(f"Error loading image. Please ensure the file path is correct.")
        return None

def transform_points(points, scale=1.0, rotation=0):
    if points is None: return None
    center = np.mean(points, axis=0)
    shifted = (points - center) * scale
    theta = np.radians(rotation)
    rot_matrix = np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]])
    rotated = shifted.dot(rot_matrix.T)
    return rotated + center

def draw_kolam_static(points, dot_color="black", bg_color="white", dot_size=3, opacity=1.0, fill=False, grid=False, marker='o', figsize=(8,8), cmap=None):
    """Enhanced function with properly working grid display"""
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_aspect("equal")
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    
    if points is not None and points.size > 0:
        # Set axis limits based on points
        margin = 50
        x_min, x_max = np.min(points[:, 0]) - margin, np.max(points[:, 0]) + margin
        y_min, y_max = np.min(points[:, 1]) - margin, np.max(points[:, 1]) + margin
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        
        # Show grid if requested - PROPERLY CONFIGURED
        if grid:
            # Calculate grid spacing based on the data range
            x_range = x_max - x_min
            y_range = y_max - y_min
            
            # Set grid spacing to create nice square grid
            grid_spacing = max(20, min(x_range/20, y_range/20))
            
            # Create custom tick locations for grid
            x_ticks = np.arange(x_min, x_max + grid_spacing, grid_spacing)
            y_ticks = np.arange(y_min, y_max + grid_spacing, grid_spacing)
            
            ax.set_xticks(x_ticks)
            ax.set_yticks(y_ticks)
            
            # Enable grid with proper styling
            ax.grid(True, linestyle='-', alpha=0.3, color='#CCCCCC', linewidth=0.8)
            ax.set_axisbelow(True)  # Put grid behind the points
            
            # Keep axis off but show grid
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        else:
            ax.axis("off")
        
        # Plot the Kolam points
        ax.scatter(points[:, 0], points[:, 1], s=dot_size, alpha=opacity, 
                   marker=marker, c=dot_color, cmap=cmap, edgecolors='none')
        
        # Fill shape if requested
        if fill and len(points) > 2:
            fill_color = plt.get_cmap(cmap)(0.5) if cmap and not isinstance(dot_color, str) else dot_color
            try:
                # Create a convex hull for filling
                from scipy.spatial import ConvexHull
                hull = ConvexHull(points)
                hull_points = points[hull.vertices]
                ax.fill(hull_points[:, 0], hull_points[:, 1], color=fill_color, alpha=0.2)
            except:
                # Fallback: simple polygon fill
                ax.fill(points[:, 0], points[:, 1], color=fill_color, alpha=0.2)
    else:
        # Default view when no points
        ax.set_xlim(0, 400)
        ax.set_ylim(0, 400)
        
        if grid:
            # Create a nice default grid
            grid_spacing = 20
            x_ticks = np.arange(0, 401, grid_spacing)
            y_ticks = np.arange(0, 401, grid_spacing)
            
            ax.set_xticks(x_ticks)
            ax.set_yticks(y_ticks)
            ax.grid(True, linestyle='-', alpha=0.3, color='#CCCCCC', linewidth=0.8)
            ax.set_axisbelow(True)
            ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)
        else:
            ax.axis("off")
    
    if not grid:
        ax.axis("off")
    
    plt.tight_layout()
    return fig

def create_svg(points, dot_color="black", bg_color="white", dot_size=3, width=800, height=600):
    """Create SVG vector graphics of Kolam pattern"""
    if not SVG_AVAILABLE or points is None or len(points) == 0:
        return None
    
    # Calculate bounds and center the pattern
    x_min, x_max = np.min(points[:, 0]), np.max(points[:, 0])
    y_min, y_max = np.min(points[:, 1]), np.max(points[:, 1])
    
    # Scale to fit SVG canvas with margin
    margin = 50
    scale_x = (width - 2 * margin) / (x_max - x_min) if x_max != x_min else 1
    scale_y = (height - 2 * margin) / (y_max - y_min) if y_max != y_min else 1
    scale = min(scale_x, scale_y)
    
    # Create SVG drawing
    dwg = svgwrite.Drawing(size=(width, height))
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill=bg_color))
    
    # Transform and draw points
    for point in points:
        x = margin + (point[0] - x_min) * scale
        y = margin + (point[1] - y_min) * scale
        dwg.add(dwg.circle(center=(x, y), r=dot_size/2, fill=dot_color))
    
    return dwg.tostring()

def smooth_path(points, smooth_factor=200):
    if len(points) < 4: return points
    try:
        tck, u = splprep([points[:, 0], points[:, 1]], s=5.0)
        x_new, y_new = splev(np.linspace(0, 1, smooth_factor), tck)
        return np.vstack((x_new, y_new)).T
    except Exception: return points

def paths_to_mask(paths, canvas_width, canvas_height, stroke_width=3):
    mask = np.zeros((canvas_height, canvas_width), dtype=np.uint8)
    for p in paths:
        pts = np.array(p, dtype=np.int32)
        if pts.shape[0] > 1:
             cv2.polylines(mask, [pts.reshape((-1,1,2))], False, 255, thickness=stroke_width, lineType=cv2.LINE_AA)
    return mask

def apply_glow_effect(mask, glow_color_hex="#00FFFF", blur_strengths=(9, 21, 41), intensity=0.9):
    if mask is None or mask.size == 0: return np.zeros((100,100,3), dtype=np.uint8)
    hex_col = glow_color_hex.lstrip('#'); r, g, b = tuple(int(hex_col[i:i+2], 16) for i in (0, 2, 4))
    color_bgr = (b, g, r); m = (mask.astype(np.float32) / 255.0); h, w = mask.shape
    colored = np.zeros((h, w, 3), dtype=np.float32)
    for i in range(3): colored[..., i] = m * (color_bgr[i] / 255.0)
    glow = np.zeros_like(colored)
    for k in blur_strengths:
        ksize = k if k % 2 == 1 else k + 1
        glow = cv2.add(glow, cv2.GaussianBlur(colored, (ksize, ksize), sigmaX=0))
    if np.max(glow) > 0: glow = glow / np.max(glow)
    stroke_bgr = np.zeros((h, w, 3), dtype=np.float32)
    for i in range(3): stroke_bgr[..., i] = m * (color_bgr[i] / 255.0)
    final = np.clip(glow * intensity + stroke_bgr, 0, 1.0)
    return (final * 255).astype(np.uint8)

def calculate_symmetry_properties(points):
    """Calculate symmetry and geometric properties of Kolam"""
    if points is None or len(points) == 0:
        return {}
    
    center = np.mean(points, axis=0)
    properties = {}
    
    # Calculate radial distances
    distances = np.sqrt(np.sum((points - center)**2, axis=1))
    properties['avg_radius'] = np.mean(distances)
    properties['radius_std'] = np.std(distances)
    
    # Calculate angles from center
    angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])
    angles = np.degrees(angles) % 360
    
    # Detect potential symmetry orders
    symmetry_scores = {}
    for order in [2, 3, 4, 5, 6, 8, 12]:
        sector_size = 360 / order
        sectors = np.floor(angles / sector_size).astype(int)
        sector_counts = np.bincount(sectors, minlength=order)
        symmetry_scores[order] = 1 - np.std(sector_counts) / (np.mean(sector_counts) + 1)
    
    best_symmetry = max(symmetry_scores.items(), key=lambda x: x[1])
    properties['likely_symmetry_order'] = best_symmetry[0]
    properties['symmetry_confidence'] = best_symmetry[1]
    
    # Calculate bounding box properties
    x_range = np.max(points[:, 0]) - np.min(points[:, 0])
    y_range = np.max(points[:, 1]) - np.min(points[:, 1])
    properties['aspect_ratio'] = x_range / y_range if y_range > 0 else 1
    properties['bounding_area'] = x_range * y_range
    
    return properties

def analyze_mask_enhanced(mask):
    """Enhanced Kolam analysis with educational information"""
    results = {}
    
    # Basic connectivity analysis
    labeled = label(mask > 0)
    results["Connected Components"] = int(labeled.max())
    
    # Skeleton analysis for mathematical properties
    skel = skeletonize(mask > 0).astype(np.uint8) * 255
    skeleton_pixels = np.sum(skel > 0)
    results["Skeleton Length (pixels)"] = int(skeleton_pixels)
    
    # Topological analysis using NetworkX if available
    if NETWORKX_AVAILABLE:
        try:
            G = nx.Graph()
            pixels = np.argwhere(skel > 0)
            pixel_set = set(map(tuple, pixels))
            
            # Build graph from skeleton
            for y, x in pixels:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dy == 0 and dx == 0: continue
                        if (y + dy, x + dx) in pixel_set:
                            G.add_edge((y, x), (y + dy, x + dx))
            
            degrees = [d for n, d in G.degree()]
            results["Endpoints"] = int(sum(1 for d in degrees if d == 1))
            results["T-junctions"] = int(sum(1 for d in degrees if d == 3))
            results["Crossings"] = int(sum(1 for d in degrees if d >= 4))
            
            # Calculate Euler characteristic (V - E + F)
            vertices = len(G.nodes())
            edges = len(G.edges())
            # For planar graphs: V - E + F = 2, so F = 2 - V + E
            euler_char = vertices - edges
            results["Euler Characteristic"] = euler_char
            
            # Calculate complexity measures
            if vertices > 0:
                results["Average Degree"] = round(2 * edges / vertices, 2)
            
            # Detect cycles
            try:
                cycles = list(nx.simple_cycles(G.to_directed()))
                results["Number of Cycles"] = len([c for c in cycles if len(c) >= 3])
            except:
                results["Number of Cycles"] = "Could not calculate"
                
        except Exception as e:
            results["Graph Analysis Error"] = str(e)
    else:
        results["Graph Analysis"] = "NetworkX not available"
    
    # Geometric analysis
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        perimeter = cv2.arcLength(largest_contour, True)
        
        results["Pattern Area"] = int(area)
        results["Pattern Perimeter"] = int(perimeter)
        
        if perimeter > 0:
            # Compactness measure (closer to 1 = more circular)
            compactness = 4 * math.pi * area / (perimeter ** 2)
            results["Compactness"] = round(compactness, 3)
    
    return results, skel

def generate_educational_analysis(points, mask_results, symmetry_props):
    """Generate educational analysis of the Kolam pattern"""
    
    analysis = {
        "overview": "",
        "mathematical_concepts": [],
        "cultural_significance": "",
        "geometric_properties": [],
        "complexity_metrics": []
    }
    
    # Overview
    components = mask_results.get("Connected Components", 0)
    if components == 1:
        analysis["overview"] = "This Kolam consists of a single connected pattern, representing unity and continuity in traditional Tamil culture."
    elif components > 1:
        analysis["overview"] = f"This Kolam has {components} separate components, which may represent different elements or phases in life's journey."
    
    # Mathematical concepts
    analysis["mathematical_concepts"].append("**Topology**: The study of spatial properties preserved under continuous deformations.")
    
    endpoints = mask_results.get("Endpoints", 0)
    crossings = mask_results.get("Crossings", 0)
    
    if endpoints > 0:
        analysis["mathematical_concepts"].append(f"**Graph Theory**: This pattern has {endpoints} endpoints, indicating open paths in the design.")
    
    if crossings > 0:
        analysis["mathematical_concepts"].append(f"**Network Analysis**: The pattern contains {crossings} crossing points, showing intersection complexity.")
    
    euler_char = mask_results.get("Euler Characteristic")
    if euler_char is not None:
        analysis["mathematical_concepts"].append(f"**Euler Characteristic**: V - E = {euler_char}, a fundamental topological invariant.")
    
    # Symmetry analysis
    if symmetry_props and 'likely_symmetry_order' in symmetry_props:
        order = symmetry_props['likely_symmetry_order']
        confidence = symmetry_props['symmetry_confidence']
        if confidence > 0.7:
            analysis["mathematical_concepts"].append(f"**Rotational Symmetry**: Pattern shows {order}-fold rotational symmetry (confidence: {confidence:.2f}).")
    
    # Geometric properties
    compactness = mask_results.get("Compactness")
    if compactness is not None:
        if compactness > 0.8:
            analysis["geometric_properties"].append("**Shape**: High compactness indicates a nearly circular overall form.")
        elif compactness > 0.5:
            analysis["geometric_properties"].append("**Shape**: Moderate compactness indicates a balanced, organic form.")
        else:
            analysis["geometric_properties"].append("**Shape**: Low compactness indicates an elongated or complex boundary.")
    
    aspect_ratio = symmetry_props.get("aspect_ratio", 1) if symmetry_props else 1
    if aspect_ratio > 1.5:
        analysis["geometric_properties"].append("**Proportion**: The pattern is horizontally elongated.")
    elif aspect_ratio < 0.67:
        analysis["geometric_properties"].append("**Proportion**: The pattern is vertically elongated.")
    else:
        analysis["geometric_properties"].append("**Proportion**: The pattern has balanced proportions.")
    
    # Cultural significance
    analysis["cultural_significance"] = """
    **Cultural Context**: Kolam is a traditional South Indian art form, primarily practiced in Tamil Nadu. 
    These geometric patterns are drawn daily at dawn using rice flour, serving both aesthetic and spiritual purposes.
    
    **Symbolism**: Kolam patterns often represent:
    - The infinite nature of existence (continuous loops)
    - Protection and welcome (drawn at thresholds)
    - Mathematical precision and cosmic order
    - Prosperity and abundance (rice flour attracts ants and birds)
    """
    
    # Complexity metrics
    skeleton_length = mask_results.get("Skeleton Length (pixels)", 0)
    if skeleton_length > 5000:
        analysis["complexity_metrics"].append("**High Complexity**: Extensive pattern with rich detail.")
    elif skeleton_length > 2000:
        analysis["complexity_metrics"].append("**Moderate Complexity**: Well-developed pattern with good detail.")
    else:
        analysis["complexity_metrics"].append("**Simple Complexity**: Clean, minimalist pattern.")
    
    avg_degree = mask_results.get("Average Degree")
    if avg_degree is not None:
        if avg_degree > 3:
            analysis["complexity_metrics"].append(f"**High Connectivity**: Average node degree of {avg_degree} indicates rich interconnections.")
        else:
            analysis["complexity_metrics"].append(f"**Moderate Connectivity**: Average node degree of {avg_degree} indicates balanced structure.")
    
    return analysis

# ---- Main Streamlit App UI ----
st.title("🎨 Accessible Kolam & Kaleidoscope Designer with Chitra")
st.markdown("### Voice-Enabled Pattern Creation with Your Personal Assistant")

# Chitra activation section
if not st.session_state.chitra_activated:
    st.info("👋 Meet Chitra, your personal voice assistant for creating beautiful Kolam patterns!")
    if st.button("🚀 Activate Chitra"):
        st.session_state.chitra_activated = True
        st.rerun()
else:
    # CONSOLIDATED: Welcome message on first activation
    if 'chitra_welcomed' not in st.session_state:
        st.session_state.chitra_welcomed = True
        welcome_message = "Welcome! I'm Chitra, your voice assistant. I'm ready to help you create beautiful patterns. Try saying 'simple lotus pattern' or ask for 'help' to get started."
        speak_text(welcome_message)
        # Add this welcome to the chat history
        if len(st.session_state.messages) == 1:
            st.session_state.messages.append({"role": "assistant", "content": welcome_message})

st.info("🔊 **Accessibility Features**: This app includes comprehensive voice commands with Chitra. A new 'Conversational Drawing' mode allows visually impaired users to create art by telling Chitra what to draw.")

col1, col2 = st.columns([2,1])

with col2:
    st.markdown("### Control Panel")
    
    st.markdown("#### 🔊 Chitra Settings")
    voice_enabled = st.checkbox("Enable Chitra's Voice", value=st.session_state.get('voice_feedback', True), key='voice_feedback')
    
    st.markdown("---")
    
    mode_options = ["Predefined Kolam", "Upload Image", "Draw Freehand", "Kaleidoscope Draw", "Conversational Drawing", "Generative Design"]
    mode = st.radio("Kolam Source", 
                    mode_options,
                    index=mode_options.index(st.session_state.current_mode))
    
    if mode != st.session_state.current_mode:
        st.session_state.current_mode = mode
        st.session_state.generated_points = None # Clear generated points on mode switch

# ---- Enhanced Sidebar with Chitra Voice Assistant ----
with st.sidebar:
    if st.session_state.chitra_activated:
        st.header("🎤 Chat with Chitra")
        st.markdown("**Try saying:**\n- 'Start conversational drawing'\n- 'Create a new design'\n- 'Analyze this kolam'\n- 'Show grid'")
        
        st.markdown("---")
        col_mic1, col_mic2 = st.columns(2)
        with col_mic1:
            audio_data = mic_recorder(start_prompt="🎤 Talk to Chitra", stop_prompt="🔴 Processing...", just_once=True, use_container_width=True, format="wav", key="chitra_mic")
        with col_mic2:
            if st.button("🆘 Ask for Help", help="Get help from Chitra"):
                st.session_state.messages.append({"role": "assistant", "content": handle_chat_prompt("help")})

        if audio_data and audio_data.get("bytes"):
            with st.spinner("🔄 Chitra is listening..."):
                spoken_prompt = transcribe_audio(audio_data)
                if spoken_prompt:
                    st.success(f"👂 Chitra heard: '{spoken_prompt}'")
                    st.session_state.messages.append({"role": "user", "content": spoken_prompt})
                    response = handle_chat_prompt(spoken_prompt)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                else:
                    error_msg = "I'm sorry, I couldn't quite hear that. Could you please try again or type your message?"
                    st.error(error_msg)
                    speak_text(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

        st.markdown("---")
        
        st.subheader("💬 Conversation with Chitra")
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
        
        if prompt := st.chat_input("Type a message to Chitra", key="chitra_text_input"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.write(prompt)
            response = handle_chat_prompt(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"): st.write(response)
    else:
        st.header("🎤 Chitra Voice Assistant")
        st.info("Activate Chitra above to start voice interaction!")

    st.markdown("---")
    
    st.header("Manual Controls")

    # Coloring options with improved UI
    with st.expander("🎨 Coloring Options", expanded=True):
        st.color_picker("Background Color", key="bg_color")
        st.markdown("---")
        
        dot_style = st.radio(
            "Dot Color Style",
            ["Solid Color", "Color Gradient"],
            key="dot_color_style"
        )

        if dot_style == "Solid Color":
            st.color_picker("Dot Color", key="solid_dot_color")
        else: # "Color Gradient"
            st.selectbox(
                "Color Gradient",
                options=['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'rainbow', 'jet'],
                key="color_gradient"
            )

    with st.expander("🎛 Shape & Style Settings", expanded=False):
        st.slider("Dot Size", 1, 50, key="dot_size")
        marker_options = {"Circle": "o", "Square": "s", "Diamond": "D", "Star": "*", "Point": "."}
        marker_choice = st.selectbox("Dot Style", list(marker_options.keys()))
        marker = marker_options[marker_choice]
        st.slider("Opacity", 0.1, 1.0, key="opacity")
        st.checkbox("Fill Kolam Shape", key="fill_shape")
        st.checkbox("Show Grid", key="show_grid")
        
        st.markdown("**Transformations**")
        st.slider("Scale", 0.5, 3.0, key="scale")
        st.slider("Rotation (degrees)", 0, 360, key="rotation")
        st.checkbox("Horizontal Mirror", key="horizontal_mirror")
        st.checkbox("Vertical Mirror", key="vertical_mirror")

# ---- Main Content Area ----
with col1:
    points = None
    canvas_width, canvas_height = 640, 480

    if st.session_state.current_mode == "Predefined Kolam":
        st.subheader("📚 Predefined Kolam Library")
        choice = st.selectbox("Choose a Kolam Pattern", list(PREMADE_PATTERNS.keys()),
                              index=list(PREMADE_PATTERNS.keys()).index(st.session_state.current_pattern) if st.session_state.current_pattern in PREMADE_PATTERNS else 0)
        if choice != st.session_state.current_pattern:
            st.session_state.current_pattern = choice
            if st.session_state.chitra_activated:
                speak_text(f"Selected {choice}")
        points = load_pattern_as_points(PREMADE_PATTERNS[choice])
        if points is None:
            st.error(f"⚠ Could not load {choice}. Please check the file path.")
            if st.session_state.chitra_activated:
                speak_text(f"I'm sorry, I couldn't load the {choice} pattern. Please check the file path.")

    elif st.session_state.current_mode == "Upload Image":
        st.subheader("📁 Upload Your Kolam Image")
        uploaded_file = st.file_uploader("Choose an image file", type=["png","jpg","jpeg"])
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            nparr = np.frombuffer(bytes_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            skeleton = skeletonize(thresh // 255).astype(np.uint8)
            y_coords, x_coords = np.where(skeleton)
            points = np.vstack((x_coords, y_coords)).T
            if points.size > 0:
                st.success("✅ Image uploaded and processed successfully!")
                if st.session_state.chitra_activated:
                    speak_text("Perfect! I've processed your uploaded image successfully.")
            else:
                st.error("❌ Could not process the uploaded image.")
                if st.session_state.chitra_activated:
                    speak_text("I'm sorry, I had trouble processing your uploaded image. Please try a different image.")

    elif st.session_state.current_mode == "Draw Freehand":
        st.subheader("✏️ Freehand Drawing Canvas")
        with st.expander("🎨 Drawing Options", expanded=True):
            c1, c2 = st.columns(2)
            stroke_width = c1.slider("Stroke Width", 1, 30, 3)
            smoothness = c2.slider("Smoothing", 50, 800, 300)
            
            enable_aod = st.checkbox("Enable Glow Effect", value=True)
            
            if enable_aod:
                glow_color = st.color_picker("Glow Color", "#00FFFF")
                glow_intensity = st.slider("Glow Intensity", 0.1, 2.0, 0.9)
        
        # Create columns for the canvas and the new reference image uploader
        canvas_col, ref_col = st.columns([2, 1])

        with ref_col:
            st.markdown("#### 🖼️ Reference Image")
            st.info("Upload a Kolam pattern to use as a visual guide while you draw.")
            reference_image = st.file_uploader("Upload reference image", type=["png", "jpg", "jpeg"])
            if reference_image is not None:
                st.image(reference_image, caption="Your Reference Pattern")
            else:
                st.markdown("Your reference image will appear here once uploaded.")

        with canvas_col:
            # Regular canvas without grid
            canvas_result = st_canvas(
                fill_color="rgba(0,0,0,0)", stroke_width=stroke_width, stroke_color="#000000",
                background_color="#FFFFFF", update_streamlit=True, 
                height=canvas_height, width=canvas_width, drawing_mode="freedraw", key="canvas"
            )
        
            # Process the canvas results
            if canvas_result.json_data and canvas_result.json_data.get("objects"):
                paths = []
                for obj in canvas_result.json_data["objects"]:
                    if obj['type'] == 'path' and 'path' in obj:
                        try:
                            path_data = obj["path"]
                            if len(path_data) > 0:
                                path_points = [[point[1], point[2]] for point in path_data if len(point) >= 3]
                                if len(path_points) > 1:
                                    paths.append(np.array(path_points, dtype=float))
                        except (IndexError, ValueError, TypeError):
                            continue
                
                if paths:
                    try:
                        all_pts = np.vstack(paths)
                        points = smooth_path(all_pts, smooth_factor=smoothness)
                        
                        if enable_aod:
                            st.subheader("✨ Glow Effect Preview")
                            mask = paths_to_mask(paths, canvas_width, canvas_height, stroke_width=stroke_width*2)
                            glow_img = apply_glow_effect(mask, glow_color_hex=glow_color, intensity=glow_intensity)
                            st.image(glow_img, caption="Kolam with Glow Effect", use_column_width=True)
                            _, png = cv2.imencode('.png', cv2.cvtColor(glow_img, cv2.COLOR_BGR2RGB))
                            st.download_button("💾 Download Glow PNG", data=png.tobytes(), file_name="kolam_glow.png", mime="image/png")
                            points = None
                    except ValueError:
                        st.warning("Drawing data is inconsistent. Please try drawing again.")
                        points = None
    
    elif st.session_state.current_mode == "Conversational Drawing":
        st.subheader("🗣️ Conversational Drawing with Chitra")
        st.info("Tell Chitra what to draw! Use commands like 'draw a circle', 'add a line', 'undo', or 'clear drawing'.")
        # Render the current drawing and convert it to points for processing
        conv_canvas_w, conv_canvas_h = 600, 600
        points = render_drawn_objects_to_points(st.session_state.drawn_objects, conv_canvas_w, conv_canvas_h)
        
        # Display the rendered drawing
        if st.session_state.drawn_objects:
            temp_img = np.zeros((conv_canvas_h, conv_canvas_w, 3), dtype=np.uint8)
            temp_img.fill(255) # White background
            for obj in st.session_state.drawn_objects:
                color_bgr = (0,0,0)
                if obj['type'] == 'circle':
                    cv2.circle(temp_img, obj['center'], obj['radius'], color_bgr, 5, cv2.LINE_AA)
                elif obj['type'] == 'square':
                    cv2.rectangle(temp_img, obj['top_left'], obj['bottom_right'], color_bgr, 5, cv2.LINE_AA)
                elif obj['type'] == 'line':
                    cv2.line(temp_img, obj['start'], obj['end'], color_bgr, 5, cv2.LINE_AA)
            st.image(temp_img, caption="Your drawing by Chitra", use_column_width=True)
        else:
            st.info("The canvas is currently empty. Tell Chitra what to draw!")


    elif st.session_state.current_mode == "Kaleidoscope Draw":
        st.subheader("🌀 Kaleidoscope Pattern Creator")
        st.info("🎨 Draw in the tool below. Your strokes will be mirrored symmetrically!")
        components.html(kaleidoscope_html, height=850, scrolling=False)
        st.markdown("---")
        st.markdown("💡 **Tips:**\n- Start from the center and draw outward.\n- Try different colors for vibrant patterns.\n- Save your creation and upload it using 'Upload Image' mode.")
        points = None
        
    if st.session_state.current_mode == "Generative Design":
        st.subheader("🔮 Generative Kolam Creator")
        st.info("This mode uses the current kolam as a base to generate a new, unique design. Adjust the parameters below and click 'Generate'!")

        # Generative Design Controls
        with st.expander("🛠️ Generation Parameters", expanded=True):
            st.slider("Symmetry Order", 2, 16, key='gen_symmetry')
            st.slider("Complexity", 1, 10, key='gen_complexity')
            st.selectbox("Generation Style", ['loopy', 'spiky', 'floral'], key='gen_style')
            st.slider("Variation/Randomness", 0.0, 0.5, key='gen_variation')
        
        if st.button("✨ Generate New Design") or st.session_state.get('trigger_generation', False):
            if 'trigger_generation' in st.session_state:
                del st.session_state['trigger_generation']

            if st.session_state.get('base_points_for_generation') is not None:
                with st.spinner("Chitra is imagining a new pattern..."):
                    generated = generate_new_kolam(
                        st.session_state.base_points_for_generation,
                        symmetry_order=st.session_state.gen_symmetry,
                        complexity=st.session_state.gen_complexity,
                        style=st.session_state.gen_style,
                        variation=st.session_state.gen_variation
                    )
                    st.session_state.generated_points = generated
            else:
                st.warning("Please select, upload, or draw a base Kolam first before generating.")
        
        # Display the generated design if it exists
        if st.session_state.generated_points is not None:
            st.markdown("---")
            st.subheader("🌱 Your Generated Creation")
            fig_gen = draw_kolam_static(
                st.session_state.generated_points,
                dot_color=st.session_state.solid_dot_color,
                bg_color=st.session_state.bg_color,
                dot_size=st.session_state.dot_size,
                grid=st.session_state.show_grid
            )
            st.pyplot(fig_gen)
            # Add download for the generated image
            buf_gen = BytesIO()
            fig_gen.savefig(buf_gen, format="png", bbox_inches='tight', pad_inches=0.1, facecolor=fig_gen.get_facecolor(), dpi=300)
            st.download_button("💾 Download Generated PNG", data=buf_gen.getvalue(), file_name="generated_kolam.png", mime="image/png")

    # This block handles the display of the ORIGINAL kolam
    if points is not None and len(points) > 0:
        st.markdown("---")
        st.subheader("🎨 Your Kolam Creation")
        
        transformed_points = transform_points(points, scale=st.session_state.scale, rotation=st.session_state.rotation)
        
        final_points_list = [transformed_points]
        center = np.mean(transformed_points, axis=0)
        if st.session_state.horizontal_mirror:
            mirrored_h = transformed_points.copy()
            mirrored_h[:, 1] = 2 * center[1] - mirrored_h[:, 1]
            final_points_list.append(mirrored_h)
        if st.session_state.vertical_mirror:
            mirrored_v = transformed_points.copy()
            mirrored_v[:, 0] = 2 * center[0] - mirrored_v[:, 0]
            final_points_list.append(mirrored_v)
        if st.session_state.horizontal_mirror and st.session_state.vertical_mirror:
            mirrored_hv = transformed_points.copy()
            mirrored_hv[:, 0] = 2 * center[0] - mirrored_hv[:, 0]
            mirrored_hv[:, 1] = 2 * center[1] - mirrored_hv[:, 1]
            final_points_list.append(mirrored_hv)

        combined_points = np.vstack(final_points_list)
        st.session_state.base_points_for_generation = combined_points # Update the base points with transformations
        
        # Handle both solid and gradient color styles
        cmap_value, color_value = None, None
        
        if st.session_state.dot_color_style == "Solid Color":
            color_value = st.session_state.solid_dot_color
        else:  # Color Gradient
            cmap_value = st.session_state.get('color_gradient', 'viridis')
            color_value = np.arange(len(combined_points))
            
        fig = draw_kolam_static(
            combined_points, 
            dot_color=color_value, 
            bg_color=st.session_state.bg_color, 
            dot_size=st.session_state.dot_size, 
            opacity=st.session_state.opacity, 
            fill=st.session_state.fill_shape, 
            grid=st.session_state.show_grid, # Grid will now show properly
            marker=marker, 
            figsize=(10, 8), 
            cmap=cmap_value
        )
        st.pyplot(fig)

        # Download options
        col_dl1, col_dl2, col_dl3 = st.columns(3)
        
        # PNG Download
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0.1, 
                    facecolor=fig.get_facecolor(), dpi=300)
        col_dl1.download_button("💾 Download PNG", data=buf.getvalue(), 
                                file_name="accessible_kolam.png", mime="image/png")
        
        # SVG Download
        if SVG_AVAILABLE:
            svg_content = create_svg(combined_points, 
                                     dot_color=st.session_state.solid_dot_color if st.session_state.dot_color_style == "Solid Color" else "black",
                                     bg_color=st.session_state.bg_color, 
                                     dot_size=st.session_state.dot_size)
            if svg_content:
                col_dl2.download_button("🎨 Download SVG", data=svg_content, 
                                        file_name="kolam_vector.svg", mime="image/svg+xml")
            else:
                col_dl2.info("SVG not available")
        else:
            col_dl2.info("Install svgwrite for SVG")
        
        # Analysis button
        if col_dl3.button("🔍 Analyze Kolam") or st.session_state.get('trigger_analysis', False):
            if 'trigger_analysis' in st.session_state: 
                del st.session_state['trigger_analysis']
            
            with st.spinner("🔬 Chitra is analyzing your Kolam pattern..."):
                st.markdown("---")
                st.header("📊 Enhanced Kolam Pattern Analysis")
                
                # Prepare data for analysis
                min_xy = combined_points.min(axis=0)
                pts_norm = combined_points - min_xy
                scale_to = 400.0 / max(pts_norm.max(), 1.0)
                pts_scaled = (pts_norm * scale_to).astype(int) + 10
                mask_an = np.zeros((420, 420), dtype=np.uint8)
                # Ensure we have a list of arrays for polylines
                if len(pts_scaled.shape) > 1 and pts_scaled.shape[0] > 1:
                     cv2.polylines(mask_an, [pts_scaled], isClosed=False, color=255, thickness=2, lineType=cv2.LINE_AA)
                mask_an = cv2.dilate(mask_an, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3)), iterations=1)
                
                # Perform analyses
                mask_results, skel = analyze_mask_enhanced(mask_an)
                symmetry_props = calculate_symmetry_properties(combined_points)
                educational_analysis = generate_educational_analysis(combined_points, mask_results, symmetry_props)
                
                # Display results
                tab1, tab2, tab3 = st.tabs(["📈 Technical Analysis", "🎓 Educational Insights", "🖼 Visual Analysis"])
                
                with tab1:
                    st.subheader("Technical Metrics")
                    col1_tech, col2_tech = st.columns(2)
                    
                    with col1_tech:
                        st.markdown("**Topological Properties:**")
                        for key in ["Connected Components", "Endpoints", "T-junctions", "Crossings", "Euler Characteristic"]:
                            if key in mask_results:
                                st.write(f"• {key}: {mask_results[key]}")
                    
                    with col2_tech:
                        st.markdown("**Geometric Properties:**")
                        for key in ["Pattern Area", "Pattern Perimeter", "Compactness", "Average Degree"]:
                            if key in mask_results:
                                st.write(f"• {key}: {mask_results[key]}")
                        
                        if symmetry_props:
                            st.write(f"• Symmetry Order: {symmetry_props.get('likely_symmetry_order', 'Unknown')}")
                            st.write(f"• Symmetry Confidence: {symmetry_props.get('symmetry_confidence', 0):.2f}")
                            st.write(f"• Aspect Ratio: {symmetry_props.get('aspect_ratio', 1):.2f}")
                
                with tab2:
                    st.subheader("Educational Insights")
                    
                    st.markdown("#### 🎯 Pattern Overview")
                    st.write(educational_analysis["overview"])
                    
                    st.markdown("#### 🧮 Mathematical Concepts")
                    for concept in educational_analysis["mathematical_concepts"]:
                        st.markdown(concept)
                    
                    st.markdown("#### 📐 Geometric Properties")
                    for prop in educational_analysis["geometric_properties"]:
                        st.markdown(f"• {prop}")
                    
                    st.markdown("#### 📊 Complexity Analysis")
                    for metric in educational_analysis["complexity_metrics"]:
                        st.markdown(f"• {metric}")
                    
                    st.markdown("#### 🏛 Cultural Significance")
                    st.markdown(educational_analysis["cultural_significance"])
                
                with tab3:
                    st.subheader("Visual Analysis")
                    
                    col_vis1, col_vis2 = st.columns(2)
                    with col_vis1:
                        st.image(mask_an, caption="Pattern Structure Analysis", use_column_width=True)
                        st.markdown("*Shows the overall structure and connectivity of your Kolam pattern.*")
                    
                    with col_vis2:
                        st.image(skel, caption="Skeleton Analysis", use_column_width=True)
                        st.markdown("*Displays the mathematical skeleton - the core structure reduced to single-pixel width lines.*")
                
                # Summary for Chitra's voice feedback
                if st.session_state.chitra_activated:
                    components_count = mask_results.get('Connected Components', 0)
                    endpoints_count = mask_results.get('Endpoints', 0)
                    summary = f"Analysis complete! Your beautiful Kolam has {components_count} connected components"
                    if endpoints_count > 0:
                        summary += f" with {endpoints_count} endpoints"
                    if symmetry_props and symmetry_props.get('symmetry_confidence', 0) > 0.7:
                        order = symmetry_props['likely_symmetry_order']
                        summary += f" and shows lovely {order}-fold symmetry"
                    summary += ". The mathematical beauty in your pattern is truly remarkable!"
                    
                    speak_text(summary)
                st.success("✅ Comprehensive analysis completed!")

    elif st.session_state.current_mode not in ["Kaleidoscope Draw", "Draw Freehand", "Conversational Drawing", "Generative Design"]:
        st.info("👆 Choose or upload a Kolam pattern to get started!")

# ---- Footer ----
st.markdown("---")
st.markdown("### 🌟 Enhanced Accessibility Features with Chitra")
st.markdown("""
- 🎤 **Chitra Voice Assistant**: Your personal AI companion with natural conversation
- 🔮 **Generative Design Mode**: A new mode where Chitra helps you create new patterns algorithmically based on your existing design.
- 🗣️ **Conversational Drawing**: A new mode for visually impaired users to create art through voice commands.
- 🔊 **Audio Feedback**: Chitra speaks to you with a clear, friendly voice  
- ⌨️ **Keyboard Accessible**: All controls work with keyboard navigation
- 🎨 **Vector Graphics**: Download scalable SVG files for high-quality prints
- 📊 **Educational Analysis**: Learn about the mathematics and culture behind Kolam patterns
- 🌐 **Grid Display**: Visual grid overlay to help with pattern alignment
""")

st.markdown("### 📚 About Kolam")
st.markdown("""
Kolam is a traditional art form from Tamil Nadu, India, where intricate geometric patterns are drawn with rice flour. 
These patterns are not just decorative but embody deep mathematical principles including:

- **Topology**: Study of spatial properties
- **Graph Theory**: Analysis of connections and networks  
- **Symmetry**: Rotational and reflective balance
- **Fractals**: Self-similar patterns at different scales

This application, enhanced with Chitra your voice assistant, helps preserve and study this beautiful mathematical art form while making it accessible to everyone through natural conversation and voice commands.
""")
