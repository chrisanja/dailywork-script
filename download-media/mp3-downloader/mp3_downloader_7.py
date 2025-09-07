# Folder picker always open
# Default folder in the last saved location else in script's folder.
# Folder choice saved immediately after you select it (even before downloading)

import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog

CONFIG_FILE = "config.txt"

def choose_folder():
    """Open folder picker window starting at last saved folder if exists, else script location."""
    root = tk.Tk()
    root.withdraw()

    # Default start location
    initial_dir = os.path.dirname(os.path.abspath(__file__))

    # If config exists and folder still exists, use it
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            last_folder = f.read().strip()
            if os.path.exists(last_folder):
                initial_dir = last_folder

    folder_selected = filedialog.askdirectory(
        title="Select Save Location",
        initialdir=initial_dir
    )
    return folder_selected

def save_last_folder(path):
    """Save last folder to config file."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(path)

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

    # Always ask where to save (but start in last folder if available)
    save_path = choose_folder()
    if not save_path:
        print("❌ No folder selected. Exiting.")
        exit()

    # Save new folder choice
    save_last_folder(save_path)

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
