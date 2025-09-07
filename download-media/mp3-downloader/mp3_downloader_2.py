import yt_dlp
import os

def download_mp3(url):
    # Path to the 'ffmpeg' folder relative to this script
    ffmpeg_path = os.path.join(os.path.dirname(__file__), 'ffmpeg')

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',  # saves as "Video Title.mp3"
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # kbps
        }],
        'ffmpeg_location': ffmpeg_path,  # Tell yt_dlp to use our ffmpeg folder
        'quiet': False,  # show progress
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Enter the video URL to download as MP3: ").strip()
    if url:
        download_mp3(url)
    else:
        print("No URL entered.")
