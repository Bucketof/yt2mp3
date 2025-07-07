from flask import Flask, request, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "Please enter a YouTube URL", 400

        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
                # 👇 Add these lines for faster downloads
                'external_downloader': 'aria2c',
                'external_downloader_args': ['-x', '16', '-k', '1M'],
                # 👆 Uses 16 connections and 1MB chunks
                'quiet': True,
                'no_warnings': True,
                # Timeout protection
                'socket_timeout': 5,
                'retries': 3
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                    
                    if os.path.exists(filename):
                        return send_file(filename, as_attachment=True)
                    return "File not created", 500
                    
            except Exception as e:
                return f"Error: {str(e)}", 500

    return '''
    <form method="post">
        <input type="text" name="url" placeholder="Paste YouTube URL" required>
        <button type="submit">Convert</button>
    </form>
    '''
