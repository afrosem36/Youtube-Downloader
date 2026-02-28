import os
import yt_dlp
import time
from flask import Flask, render_template, request, send_file, jsonify

app = Flask(__name__)

# Use absolute paths for reliability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')
FFMPEG_PATH = os.path.join(BASE_DIR, 'ffmpeg.exe')

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        ydl_opts = {'ffmpeg_location': FFMPEG_PATH, 'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # Extract unique video resolutions
            resolutions = sorted(list(set(
                f['height'] for f in formats 
                if f.get('height') and f.get('vcodec') != 'none'
            )), reverse=True)
            
            return jsonify({
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'resolutions': resolutions,
                'url': url
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    res = request.form.get('resolution')
    
    # Logic to ensure best quality up to the chosen resolution
    ydl_opts = {
        'ffmpeg_location': FFMPEG_PATH,
        'format': f'bestvideo[height<={res}]+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
        
        # This sends it to the browser for download
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"System Error: {str(e)}", 500

if __name__ == '__main__':
    # '0.0.0.0' allows external access once hosted
    app.run(host='0.0.0.0', port=5000, debug=True)