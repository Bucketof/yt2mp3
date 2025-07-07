from flask import Flask, request, send_file
from pytube import YouTube
import yt_dlp
from tqdm import tqdm
urls = []
# Valid domains
VALID_DOMAINS = [
    "youtube.com", 
    "youtu.be",
    "music.youtube.com",
    "m.youtube.com"
]
def take_urls():
    while True:
        url = input("Enter the YouTube video URL(s) (or 'done' to finish): ")
        if url.lower() == 'done':
            break
        if not any(domain in url for domain in VALID_DOMAINS):
            print("😤 Please enter a valid YouTube URL.")
            continue
        else:
            urls.append(url)
            print(f"✅ Added URL: {url}")
        if urls == []:
            print("😟 No URLs provided. Exiting.")
            continue
# Ask for the url of the YouTube video
def coverter():
    global ydl_opts
    ydl_opts = {
    "outtmpl": "%(title)s.%(ext)s",  # Saves files with the video title
    "format": "bestaudio/best",  # Best audio quality available
    "postprocessors": [{
        "key": "FFmpegExtractAudio",  # Extract audio
        "preferredcodec": "mp3",      # Convert to MP3
        "preferredquality": "192",    # Bitrate
    }],

    "quiet": True,  # Suppress verbose output
    "progress_hooks": [lambda d: tqdm.write(f"↳ {d.get('_percent_str','')} {d.get('_eta_str','')}")],
}
def download():
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(urls)

            print("Download completed successfully. 😆")
            # Give path to the downloaded files
            for url in urls:
                info = ydl.extract_info(url, download=False)
                print(f"Downloaded: {info['title']}.mp3")
    except yt_dlp.utils.DownloadError as e:
        print(f"An error occurred while downloading: {e}")
        exit()
def main():
    take_urls()
    if urls:
        coverter()
        download()
    else:
        print("No URLs provided. Exiting. 😟")
if __name__ == "__main__":
    main()
