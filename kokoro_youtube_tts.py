"""
Kokoro YouTube Voiceover Tool
=============================
A self-contained local tool for turning a script into an English voiceover
using the free, open-source Kokoro-82M TTS model (runs on CPU, no API key,
no internet needed after first setup).

FIRST-TIME SETUP
-----------------
1. Install Python 3.10, 3.11, or 3.12 if you don't have it (python.org).
2. (macOS/Linux only) Install espeak-ng, which Kokoro uses for pronunciation:
     macOS:   brew install espeak-ng
     Ubuntu:  sudo apt-get install espeak-ng
   Windows users: the installer below (piper-phonemize) usually covers this;
   if you hit pronunciation errors, install espeak-ng from
   https://github.com/espeak-ng/espeak-ng/releases

3. Run this script:
     python kokoro_youtube_tts.py

   The first run will automatically:
     - install the required Python packages (kokoro-onnx, soundfile, gradio)
     - download the Kokoro model files (~300MB, one-time)
     - open a browser tab with the tool, ready to use

Every run after that is instant and fully offline.
"""

import importlib
import os
import subprocess
import sys
import traceback
import urllib.request

# When packaged into a standalone .exe (via PyInstaller), bundled files
# extract to a temp folder referenced by sys._MEIPASS. When running as a
# normal .py script, just use the current folder.
BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
IS_FROZEN = getattr(sys, "frozen", False)

REQUIRED = ["kokoro_onnx", "soundfile", "gradio", "numpy"]
PIP_NAMES = {"kokoro_onnx": "kokoro-onnx"}

MODEL_FILE = os.path.join(BASE_DIR, "kokoro-v1.0.onnx")
VOICES_FILE = os.path.join(BASE_DIR, "voices-v1.0.bin")
ICON_FILE = os.path.join(BASE_DIR, "icon.ico")
BASE_URL = "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.1/"

# All 28 English voices Kokoro ships with. All are already inside the
# voices-v1.0.bin file you downloaded on first run — nothing more to fetch.
ENGLISH_VOICES = [
    # American English female
    "af_alloy", "af_aoede", "af_bella", "af_heart", "af_jessica", "af_kore",
    "af_nicole", "af_nova", "af_river", "af_sarah", "af_sky",
    # American English male
    "am_adam", "am_echo", "am_eric", "am_fenrir", "am_liam", "am_michael",
    "am_onyx", "am_puck", "am_santa",
    # British English female
    "bf_alice", "bf_emma", "bf_isabella", "bf_lily",
    # British English male
    "bm_daniel", "bm_fable", "bm_george", "bm_lewis",
]


def ensure_packages():
    if IS_FROZEN:
        return  # already bundled inside the .exe, nothing to install
    for mod in REQUIRED:
        try:
            importlib.import_module(mod)
        except ImportError:
            pkg = PIP_NAMES.get(mod, mod)
            print(f"Installing missing package: {pkg} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", pkg])


def ensure_model_files():
    for fname in (MODEL_FILE, VOICES_FILE):
        if os.path.exists(fname):
            print(f"{fname} already present — skipping download.")
        else:
            url = BASE_URL + fname
            print(f"Downloading {fname} (one-time, this may take a minute)...")
            urllib.request.urlretrieve(url, fname)
            print(f"Done: {fname}")


def main():
    ensure_packages()
    ensure_model_files()

    global np, sf, gr, Kokoro, kokoro
    import numpy as np
    import soundfile as sf
    import gradio as gr
    from kokoro_onnx import Kokoro

    print("Loading Kokoro model...")
    kokoro = Kokoro(MODEL_FILE, VOICES_FILE)
    print("Model loaded. Launching UI...")

    def split_into_chunks(text, max_len=450):
        """Split long scripts on sentence boundaries so each chunk stays a safe size."""
        import re
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        chunks, current = [], ""
        for s in sentences:
            if len(current) + len(s) + 1 <= max_len:
                current = (current + " " + s).strip()
            else:
                if current:
                    chunks.append(current)
                current = s
        if current:
            chunks.append(current)
        return chunks or [text]

    def generate_voiceover(script_text, voice, speed, progress=gr.Progress()):
        if not script_text.strip():
            raise gr.Error("Paste your script into the text box first.")

        chunks = split_into_chunks(script_text)
        all_audio = []
        sample_rate = 24000
        silence_gap = np.zeros(int(0.15 * sample_rate), dtype=np.float32)  # brief pause between chunks

        for i, chunk in enumerate(chunks):
            progress((i + 1) / len(chunks), desc=f"Generating part {i + 1}/{len(chunks)}")
            samples, sample_rate = kokoro.create(chunk, voice=voice, speed=speed, lang="en-us")
            all_audio.append(samples)
            all_audio.append(silence_gap)

        full_audio = np.concatenate(all_audio)
        out_path = "voiceover_output.wav"
        sf.write(out_path, full_audio, sample_rate)
        return out_path

    PREVIEW_TEXT = "Hi there, this is a quick preview of what this voice sounds like."

    def preview_voice(voice, speed):
        samples, sample_rate = kokoro.create(PREVIEW_TEXT, voice=voice, speed=speed, lang="en-us")
        out_path = "voice_preview.wav"
        sf.write(out_path, samples, sample_rate)
        return out_path

    with gr.Blocks(title="Kokoro YouTube Voiceover Tool") as demo:
        gr.Markdown("## 🎙️ Kokoro YouTube Voiceover Tool\nFree, local, offline English TTS.")
        with gr.Row():
            with gr.Column(scale=2):
                script_box = gr.Textbox(
                    label="Your script",
                    placeholder="Paste your full video script here...",
                    lines=16,
                )
            with gr.Column(scale=1):
                voice_dd = gr.Dropdown(ENGLISH_VOICES, value="af_heart", label="Voice")
                speed_slider = gr.Slider(0.7, 1.4, value=1.0, step=0.05, label="Speed")
                preview_btn = gr.Button("🔊 Preview Voice")
                preview_audio = gr.Audio(label="Preview", type="filepath")
                generate_btn = gr.Button("Generate Voiceover", variant="primary")
                audio_out = gr.Audio(label="Result", type="filepath")

        preview_btn.click(
            fn=preview_voice,
            inputs=[voice_dd, speed_slider],
            outputs=preview_audio,
        )

        generate_btn.click(
            fn=generate_voiceover,
            inputs=[script_box, voice_dd, speed_slider],
            outputs=audio_out,
        )

    print("Starting local server — a browser tab should open automatically.")
    print("If it doesn't, look for a 'Running on local URL:' line below and open that link.")
    demo.launch(inbrowser=True, favicon_path=ICON_FILE if os.path.exists(ICON_FILE) else None)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("\n" + "=" * 60)
        print("Something went wrong. Full error details below:")
        print("=" * 60)
        traceback.print_exc()
        print("=" * 60)
    finally:
        input("\nPress Enter to close this window...")
