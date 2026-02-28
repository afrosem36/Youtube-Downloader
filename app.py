import os
import yt_dlp
from flask import Flask, render_template, request, send_file, jsonify

# Configures Flask to find index.html in the root folder instead of /templates
app = Flask(__name__, template_folder='.')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, 'downloads')

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_info', methods=['POST'])
def get_info():
    url = request.json.get('url')
    try:
        # On Render, ffmpeg is installed via render-build.sh and is available globally
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # Filter unique video-only or combined resolutions
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
        return jsonify({'error': str(e)}), 400

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    res = request.form.get('resolution')
    
    ydl_opts = {
        'format': f'bestvideo[height<={res}]+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
        return send_file(filepath, as_attachment=True)
    except Exception as e:
        return f"Download Error: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
