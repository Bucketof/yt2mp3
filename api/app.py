from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "Paste a YouTube URL first!", 400
        
        # Simple download - we'll improve this later
        os.system(f"yt-dlp -x --audio-format mp3 {url}")
        filename = os.listdir()[0]  # Get the first file
        return send_file(filename, as_attachment=True)
    
    return '''
    <h1>YouTube to MP3</h1>
    <form method="post">
        <input type="text" name="url" placeholder="Paste YouTube URL">
        <button type="submit">Convert</button>
    </form>
    '''
