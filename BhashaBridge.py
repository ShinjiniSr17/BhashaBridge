import os
import pyaudio
import wave
import speech_recognition as sr
from gtts import gTTS
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, font

# Language dictionary
language_dict = {
    "Hindi": {"recognize": "hi-IN", "speak": "hi"},
    "Tamil": {"recognize": "ta-IN", "speak": "ta"},
    "Bengali": {"recognize": "bn-IN", "speak": "bn"},
    "Telugu": {"recognize": "te-IN", "speak": "te"},
    "Gujarati": {"recognize": "gu-IN", "speak": "gu"},
    "Marathi": {"recognize": "mr-IN", "speak": "mr"},
    "Kannada": {"recognize": "kn-IN", "speak": "kn"},
    "Malayalam": {"recognize": "ml-IN", "speak": "ml"},
    "Punjabi": {"recognize": "pa-IN", "speak": "pa"},
    "Urdu": {"recognize": "ur-IN", "speak": "ur"},
    "English": {"recognize": "en-IN", "speak": "en"}
}

def record_audio(duration=5):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = [stream.read(1024) for _ in range(0, int(16000 / 1024 * duration))]
    stream.stop_stream(); stream.close(); p.terminate()

    file_path = "recorded_audio.wav"
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))
    return file_path

def voice_to_text_using_wav(file_path, language="hi-IN"):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return "Sorry, couldn't understand the audio."
    except sr.RequestError:
        return "Speech recognition service is unavailable."

def text_to_voice_using_gtts(text, language="hi"):
    tts = gTTS(text=text, lang=language, slow=False)
    output_file = "output.mp3"
    tts.save(output_file)
    return output_file

def start_recording():
    try:
        duration = simpledialog.askinteger("Input", "Enter duration in seconds:", minvalue=1)
        if duration:
            instruction_label.config(text="Recording...", fg="#ff5e57")
            audio_file = record_audio(duration)
            lang_code = language_dict[language_combobox.get()]["recognize"]
            recognized_text = voice_to_text_using_wav(audio_file, language=lang_code)
            os.remove(audio_file)
            display_recognized_speech(recognized_text)
            instruction_label.config(text="Click Record to try again", fg="#888")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def convert_text_to_speech():
    try:
        text = text_entry.get()
        if text:
            lang_code = language_dict[language_combobox.get()]["speak"]
            audio_file = text_to_voice_using_gtts(text, language=lang_code)
            os.system(f"start {audio_file}")
            messagebox.showinfo("Success", "Speech generated successfully.")
        else:
            messagebox.showwarning("Input Needed", "Please enter text to convert.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def display_recognized_speech(text):
    recognized_text_label.config(text=f"{text}")

# --- Modern GUI Setup ---
root = tk.Tk()
root.title("BhashaBridge - Multilingual Voice ↔ Text")
root.geometry("900x600")
root.configure(bg="#f4f6f8")

# Fonts and styles
heading_font = font.Font(family="Segoe UI", size=24, weight="bold")
subheading_font = font.Font(family="Segoe UI", size=12)
label_font = font.Font(family="Segoe UI", size=10)
button_font = font.Font(family="Segoe UI", size=11, weight="bold")

# Wrapper Frame
main_frame = tk.Frame(root, bg="white", bd=0, highlightbackground="#ccc", highlightthickness=1)
main_frame.place(relx=0.5, rely=0.5, anchor="center", width=700, height=500)

# Header
tk.Label(main_frame, text="BhashaBridge", font=heading_font, bg="white", fg="#1e272e").pack(pady=(20, 5))
tk.Label(main_frame, text="Seamless Speech ↔ Text in Indian Languages", font=subheading_font, bg="white", fg="#485460").pack()

# Language selection
tk.Label(main_frame, text="Select Language", font=label_font, bg="white", fg="#2f3542").pack(pady=(20, 5))
language_combobox = ttk.Combobox(main_frame, values=list(language_dict.keys()), state="readonly", font=label_font, width=25)
language_combobox.set("Hindi")
language_combobox.pack()

# Instruction Label
instruction_label = tk.Label(main_frame, text="Click Record to begin speaking", font=label_font, bg="white", fg="#57606f")
instruction_label.pack(pady=(15, 5))

# Record Button
record_button = tk.Button(main_frame, text="🎤 Record Voice", command=start_recording, font=button_font,
                          bg="#0984e3", fg="white", activebackground="#74b9ff", padx=15, pady=5, bd=0)
record_button.pack(pady=(10, 15))

# Recognized Text Display
recognized_text_label = tk.Label(main_frame, text="Recognized Speech will appear here", wraplength=600, justify="center",
                                 font=("Segoe UI", 12), bg="#dff9fb", fg="#130f40", padx=10, pady=10, relief="flat")
recognized_text_label.pack(padx=20, pady=10, fill="x")

# Text-to-Speech Input
tk.Label(main_frame, text="Enter text for speech output", font=label_font, bg="white", fg="#2f3542").pack(pady=(15, 5))
text_entry = tk.Entry(main_frame, font=label_font, width=50, bd=1, relief="solid")
text_entry.pack(pady=(0, 10))

# Convert Button
convert_button = tk.Button(main_frame, text="🔊 Convert to Speech", command=convert_text_to_speech, font=button_font,
                           bg="#00b894", fg="white", activebackground="#55efc4", padx=15, pady=5, bd=0)
convert_button.pack(pady=(10, 5))

# Footer
tk.Label(root, text="Made with ♥ for Multilingual Communication", font=("Segoe UI", 9), bg="#f4f6f8", fg="#7f8c8d").pack(side="bottom", pady=10)

root.mainloop()
