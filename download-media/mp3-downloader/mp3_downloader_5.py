# Open the last folder location

import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog

CONFIG_FILE = "config.txt"

def choose_folder():
    """Open folder picker window."""
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Save Location")
    return folder_selected

def save_last_folder(path):
    """Save last folder to config file."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(path)

def load_last_folder():
    """Load last saved folder if exists."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def download_mp3(url, ffmpeg_path, save_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path,
        'quiet': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def get_urls():
    print("Paste one or more YouTube/SoundCloud links (press ENTER on empty line to finish):")
    urls = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        urls.extend(line.split())
    return urls

if __name__ == "__main__":
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg')

    # Load last folder or choose if not available
    save_path = load_last_folder()
    if not save_path or not os.path.exists(save_path):
        save_path = choose_folder()
        if save_path:
            save_last_folder(save_path)

    if not save_path:
        print("❌ No folder selected. Exiting.")
        exit()

    urls = get_urls()
    if not urls:
        print("No URLs entered.")
    else:
        print(f"\nDownloading {len(urls)} file(s) as MP3 to: {save_path}\n")
        for i, url in enumerate(urls, 1):
            print(f"📥 [{i}/{len(urls)}] Downloading: {url}")
            try:
                download_mp3(url, ffmpeg_path, save_path)
                print("✅ Download complete.\n")
            except Exception as e:
                print(f"❌ Error downloading {url}: {e}\n")
