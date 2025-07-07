from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return "Please enter a YouTube URL", 400
        
        # Simple system call that works on Vercel
        os.system(f"python -m yt_dlp -x --audio-format mp3 {url}")
        
        # Find the downloaded file
        for file in os.listdir():
            if file.endswith('.mp3'):
                return send_file(file, as_attachment=True)
        
        return "Conversion failed", 500
    
    return '''
    <form method="post">
        <input type="text" name="url" placeholder="Paste YouTube URL">
        <button type="submit">Convert</button>
    </form>
    '''
