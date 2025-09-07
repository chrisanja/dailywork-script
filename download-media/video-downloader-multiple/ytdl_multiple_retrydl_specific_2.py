import yt_dlp
import re
import os
import sys
import time

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

def attempt_download(url, ydl_opts, fallback=False):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = sanitize_filename(info.get('title', 'video'))
            ext = info.get('ext', 'mp4')
            print(f"✅ Downloaded: {title}.{ext}")
            return True
    except Exception as e:
        error_msg = str(e).lower()
        if any(keyword in error_msg for keyword in ["phantomjs", "timeout", "network", "connection", "proxy"]):
            print("⚠️ Connection problem detected. Retrying or falling back...")
            return "network"
        elif 'requested format not available' in error_msg and not fallback:
            return "format_unavailable"
        else:
            print(f"❌ Unknown error while downloading {url}.")
            return False

def main():
    print("Paste video URLs (one per line). Press Ctrl+D (Linux/macOS) or Ctrl+Z then Enter (Windows) when done:")
    try:
        urls_input = sys.stdin.read()
    except EOFError:
        urls_input = ""
    urls = [url.strip() for url in urls_input.splitlines() if url.strip()]

    if not urls:
        print("❗ No URLs provided.")
        return

    resolution = input("Enter desired resolution (e.g. 720, 1080) or leave blank for default: ").strip()

    if resolution.isdigit():
        format_str = f'bestvideo[height={resolution}]+bestaudio/best[height={resolution}]/best'
        print(f"📺 Trying to download at {resolution}p (fallback to default if unavailable)...")
    else:
        format_str = None
        print("🎥 Using yt-dlp default format selection...")

    base_opts = {
        'progress_hooks': [progress_hook],
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 60,
        'merge_output_format': 'mp4',
    }

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    for url in urls:
        print(f"\n📥 Downloading from: {url}")

        # Try custom format first
        opts = base_opts.copy()
        if format_str:
            opts['format'] = format_str

        result = attempt_download(url, opts)

        # If resolution not available, fallback to default format
        if result == "format_unavailable":
            print("🔁 Desired resolution not available. Retrying with default format...")
            opts['format'] = 'bestvideo+bestaudio/best'
            attempt_download(url, opts, fallback=True)
        elif result == "network":
            print("❌ Skipped due to network error.\n")

    input("\n🏁 All tasks done. Press Enter to exit...")

if __name__ == "__main__":
    main()
