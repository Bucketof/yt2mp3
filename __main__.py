from flask import Flask, request, jsonify, send_file
from pytube import YouTube
import yt_dlp
from tqdm import tqdm
import os

app = Flask(__name__)

# Your existing code starts here (unchanged)
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
                return f"{info['title']}.mp3"  # Return the filename
    except yt_dlp.utils.DownloadError as e:
        print(f"An error occurred while downloading: {e}")
        return None
# Your existing code ends here

# New Flask routes
@app.route('/')
def home():
    return """
    <h1>YouTube MP3 Downloader</h1>
    <p>Send a POST request to /download with JSON containing YouTube URLs</p>
    <p>Example: {"urls": ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]}</p>
    """

@app.route('/download', methods=['POST'])
def web_download():
    # Get URLs from web request instead of console input
    data = request.get_json()
    if not data or 'urls' not in data:
        return jsonify({"error": "Please provide URLs in JSON format"}), 400
    
    # Replace the console input with web input
    global urls
    urls = []
    for url in data['urls']:
        if not any(domain in url for domain in VALID_DOMAINS):
            continue  # Skip invalid URLs
        urls.append(url)
    
    if not urls:
        return jsonify({"error": "No valid YouTube URLs provided"}), 400
    
    # Run your existing functions
    coverter()
    filename = download()
    
    if filename and os.path.exists(filename):
        return send_file(filename, as_attachment=True)
    else:
        return jsonify({"error": "Download failed"}), 500

# Keep your original main function
def main():
    take_urls()
    if urls:
        coverter()
        download()
    else:
        print("No URLs provided. Exiting. 😟")

if __name__ == "__main__":
    # Run in web mode if deployed, console mode if run directly
    if 'VERCEL' in os.environ:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    else:
        main()
