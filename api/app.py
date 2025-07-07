from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "❌ Missing YouTube URL", 400
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'audio.%(ext)s',  # Simplified filename
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])  # Download the video
                return send_file('audio.mp3', as_attachment=True)
        except Exception as e:
            return f"🚨 Error: {str(e)}", 500

    return '''
    <h1>YouTube to MP3</h1>
    <form method="post">
        <input type="text" name="url" placeholder="Paste YouTube URL">
        <button type="submit">Convert</button>
    </form>
    '''
