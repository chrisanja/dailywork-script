import yt_dlp
import re
import os
import sys

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def progress_hook(d):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)
        speed = d.get('_speed_str', 'N/A')
        eta = d.get('_eta_str', 'N/A')
        if total:
            percent = downloaded / total * 100
            print(
                f"\rDownloading... {percent:.2f}% "
                f"({downloaded / (1024*1024):.2f}MB / {total / (1024*1024):.2f}MB) "
                f"at {speed} | ETA: {eta}     ", end='', flush=True
            )
    elif d['status'] == 'finished':
        print("\n✅ Download complete, now post-processing...")


def main():
    print("Paste video URLs (one per line). Press Ctrl+D (Linux/macOS) or Ctrl+Z then Enter (Windows) when done:")
    urls_input = sys.stdin.read()
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]

    ydl_opts = {
        'progress_hooks': [progress_hook],
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 60,
    }

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in urls:
            try:
                print(f"\n📥 Downloading from: {url}")
                info = ydl.extract_info(url, download=True)
                print(f"✅ Downloaded: {sanitize_filename(info.get('title', 'video'))}.{info.get('ext')}")
            except Exception as e:
                print(f"❌ Error downloading {url}: {e}")

if __name__ == "__main__":
    main()

