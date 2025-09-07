import yt_dlp

def download_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',  # saves as "Video Title.mp3"
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',  # kbps
        }],
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
