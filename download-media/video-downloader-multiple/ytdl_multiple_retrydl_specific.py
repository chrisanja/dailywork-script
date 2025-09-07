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

    # Ask for desired resolution
    resolution = input("Enter desired resolution (e.g. 720, 1080) or leave blank for default: ").strip()
    
    # Build format string if valid resolution provided
    if resolution.isdigit():
        format_str = f'bestvideo[height={resolution}]+bestaudio/best[height={resolution}]/best'
        print(f"📺 Trying to download videos at {resolution}p (with fallback to default format if unavailable)...")
    else:
        format_str = None
        print("🎥 Using yt-dlp default format selection...")

    # Basic options
    ydl_opts = {
        'progress_hooks': [progress_hook],
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 60,
    }

    # Add format only if user provided a valid resolution
    if format_str:
        ydl_opts['format'] = format_str
        ydl_opts['merge_output_format'] = 'mp4'  # needed when merging streams

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
