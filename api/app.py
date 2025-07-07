from flask import Flask, request, send_file
from __main__ import download, coverter  # Import your existing functions
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def web_interface():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "Please enter a YouTube URL", 400
        
        # Use your existing download logic
        coverter()
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                filename = f"{info['title']}.mp3"
                ydl.download([url])
                
                if os.path.exists(filename):
                    return send_file(filename, as_attachment=True)
                return "Download failed", 500
        except Exception as e:
            return f"Error: {str(e)}", 500
    
    return '''
    <h1>YouTube to MP3</h1>
    <form method="post">
        <input type="text" name="url" placeholder="Paste YouTube URL">
        <button type="submit">Convert</button>
    </form>
    '''
