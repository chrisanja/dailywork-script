# The folder picker shows up. But it doesnt save the last folder location

import yt_dlp
import os
import tkinter as tk
from tkinter import filedialog

def choose_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    folder_selected = filedialog.askdirectory(title="Select Save Location")
    return folder_selected

def download_mp3(url, ffmpeg_path, save_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),  # Save to chosen folder
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # kbps
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

    # Choose save location
    save_path = choose_folder()
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
