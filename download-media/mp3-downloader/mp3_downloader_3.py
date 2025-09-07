import yt_dlp
import os

def download_mp3(url, ffmpeg_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',  # saves as "Video Title.mp3"
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # kbps
        }],
        'ffmpeg_location': ffmpeg_path,  # Use FFmpeg from local folder
        'quiet': False,  # Show progress
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def get_urls():
    print("Paste one or more YouTube links (press ENTER on empty line to finish):")
    urls = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        # Allow space-separated or newline-separated input
        urls.extend(line.split())
    return urls

if __name__ == "__main__":
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg')
    
    urls = get_urls()
    if not urls:
        print("No URLs entered.")
    else:
        print(f"\nDownloading {len(urls)} video(s) as MP3...\n")
        for i, url in enumerate(urls, 1):
            print(f"📥 [{i}/{len(urls)}] Downloading: {url}")
            try:
                download_mp3(url, ffmpeg_path)
                print("✅ Download complete.\n")
            except Exception as e:
                print(f"❌ Error downloading {url}: {e}\n")
