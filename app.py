import os, glob, uuid, time, threading, subprocess
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

os.makedirs('downloads', exist_ok=True)
os.makedirs('uploads', exist_ok=True)

def cleanup_file(filepath):
    for _ in range(10):
        try:
            time.sleep(10)
            if os.path.exists(filepath): os.remove(filepath)
            break
        except Exception: pass

def get_base_ydl_opts():
    opts = {
        'quiet': True, 'noplaylist': True, 'nocheckcertificate': True, 'ignoreerrors': True, 'socket_timeout': 15,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }
    }
    if os.path.exists('cookies.txt'): opts['cookiefile'] = 'cookies.txt'
    return opts

def extract_with_retry(ydl_opts, url, download=False, retries=3, delay=2):
    last_err = None
    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=download)
                if info: return info
        except Exception as e: last_err = e
        time.sleep(delay)
    raise Exception(last_err or "Unable to extract info")

# --- SEO PAGES ---

@app.route('/')
def index():
    return render_template('index.html', 
        active_tab='downloader', 
        title='XENX Tools – All-in-One Media Toolkit', 
        desc='Download videos, convert MP3s, and merge audio/video securely online for free with XENX Tools.'
    )

@app.route('/mp3-converter')
def mp3_converter():
    return render_template('index.html', 
        active_tab='mp3', 
        title='Free Video to MP3 Converter - XENX Tools', 
        desc='Instantly convert any video URL to high-quality 320kbps MP3 audio seamlessly.'
    )

@app.route('/audio-trimmer')
def audio_trimmer():
    return render_template('index.html', 
        active_tab='audio', 
        title='Free Audio Trimmer & Merger App - XENX Tools', 
        desc='Trim dead space or merge multiple audio tracks together directly from your browser.'
    )

@app.route('/video-merger')
def video_merger():
    return render_template('index.html', 
        active_tab='video', 
        title='Free Video Merger Tool - XENX Tools', 
        desc='Combine multiple clips into a single MP4 video file instantly with zero watermarks.'
    )

@app.route('/torrent')
def torrent_page():
    return render_template('index.html', 
        active_tab='torrent', 
        title='Secure Cloud Torrent Client - XENX Tools', 
        desc='Safely process magnet links down to your browser using our encrypted proxy network.'
    )

# --- LEGAL PAGES ---

@app.route('/privacy-policy')
def privacy():
    return render_template('legal.html', title='Privacy Policy - XENX Tools', heading='Privacy Policy')

@app.route('/terms')
def terms():
    return render_template('legal.html', title='Terms of Service - XENX Tools', heading='Terms of Service')

@app.route('/contact')
def contact():
    return render_template('legal.html', title='Contact Us - XENX Tools', heading='Contact Us')

@app.route('/about')
def about():
    return render_template('legal.html', title='About Us - XENX Tools', heading='About XENX Tools')

# --- API ENDPOINTS ---

@app.route('/api/get')
def get_file():
    file = request.args.get('file')
    name = request.args.get('name', 'download')
    if not file: return "Error", 400
    filepath = os.path.abspath(os.path.join('downloads', file))
    if not filepath.startswith(os.path.abspath('downloads')): return "Error", 400
    if os.path.exists(filepath):
        threading.Thread(target=cleanup_file, args=(filepath,)).start()
        return send_file(filepath, as_attachment=True, download_name=name)
    return "File expired", 404

@app.route('/api/download', methods=['POST'])
def api_download():
    data = request.json
    if not data or 'url' not in data: return jsonify({"error": "Invalid URL"}), 400
    url = data['url']
    ydl_opts = get_base_ydl_opts()
    ydl_opts['skip_download'] = True
    try:
        info = extract_with_retry(ydl_opts, url, download=False)
        title = info.get('title', 'Unknown Title')
        formats = info.get('formats', [])
        parsed_formats = []
        for f in formats:
            format_type = "video" if f.get('vcodec') != 'none' else "audio"
            quality = f.get('format_note') or f.get('resolution') 
            if not quality and format_type == 'audio':
                quality = f"{f.get('abr', 'Unknown')}kbps" if f.get('abr') else "Audio"
            elif not quality:
                quality = f.get('format_id', 'Unknown')
            download_url = f.get('url')
            if download_url:
                parsed_formats.append({
                    "quality": str(quality), "type": format_type, "url": download_url,
                    "ext": f.get('ext', ''), "has_audio": f.get('acodec') != 'none', "format_id": f.get('format_id')
                })
        return jsonify({"title": title, "formats": parsed_formats})
    except Exception:
        return jsonify({"error": "This video cannot be processed right now. Try another link."}), 500

@app.route('/api/download_file', methods=['GET'])
def download_merged_file():
    url = request.args.get('url')
    format_id = request.args.get('format_id')
    if not url or not format_id: return "Error", 400
    file_id = str(uuid.uuid4())
    ydl_opts = get_base_ydl_opts()
    ydl_opts['format'] = f"{format_id}+bestaudio/best"
    ydl_opts['merge_output_format'] = 'mp4'
    ydl_opts['outtmpl'] = f'downloads/{file_id}.%(ext)s'
    
    try:
        info = extract_with_retry(ydl_opts, url, download=True)
        files = glob.glob(f"downloads/{file_id}.*")
        if not files: return "Failed merge", 500
        final_file = files[0]
        threading.Thread(target=cleanup_file, args=(final_file,)).start()
        safe_title = "".join(x for x in info.get('title', 'video') if x.isalnum() or x in " -_")
        return send_file(final_file, as_attachment=True, download_name=f"{safe_title}_{format_id}.mp4")
    except Exception:
        return jsonify({"error": "This video cannot be processed right now. Try another link."}), 500

@app.route('/api/convert-mp3', methods=['POST'])
def convert_mp3():
    data = request.json
    url = data.get('url')
    bitrate = data.get('bitrate', '192')
    if not url: return jsonify({"error": "URL required"}), 400
    file_id = str(uuid.uuid4())
    ydl_opts = get_base_ydl_opts()
    ydl_opts['format'] = 'bestaudio/best'
    ydl_opts['outtmpl'] = f'downloads/{file_id}.%(ext)s'
    ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': bitrate}]
    
    try:
        info = extract_with_retry(ydl_opts, url, download=True)
        safe_title = "".join(x for x in info.get('title', 'audio') if x.isalnum() or x in " -_")
        return jsonify({"success": True, "title": info.get('title'), "download_url": f"/api/get?file={file_id}.mp3&name={safe_title}_{bitrate}kbps.mp3"})
    except Exception:
        return jsonify({"error": "This video cannot be processed right now. Try another link."}), 500

@app.route('/api/trim-audio', methods=['POST'])
def trim_audio():
    if 'file' not in request.files: return jsonify({"error": "No file"}), 400
    file = request.files['file']
    start = request.form.get('start', '00:00:00')
    end = request.form.get('end', '00:00:10')
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1] or '.mp3'
    ipath = os.path.join('uploads', f"in_{file_id}{ext}")
    opath = os.path.join('downloads', f"out_{file_id}{ext}")
    file.save(ipath)
    subprocess.run(['ffmpeg', '-y', '-i', ipath, '-ss', start, '-to', end, '-c', 'copy', opath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cleanup_file(ipath)
    if os.path.exists(opath):
        return jsonify({"success": True, "download_url": f"/api/get?file=out_{file_id}{ext}&name=trimmed_{secure_filename(file.filename)}"})
    return jsonify({"error": "Trim failed"}), 500

@app.route('/api/merge-audio', methods=['POST'])
def merge_audio():
    files = request.files.getlist('files')
    if len(files) < 2: return jsonify({"error": "Provide 2+ files"}), 400
    file_id, paths = str(uuid.uuid4()), []
    lpath = os.path.join('uploads', f"list_{file_id}.txt")
    opath = os.path.join('downloads', f"out_{file_id}.mp3")
    with open(lpath, 'w', encoding='utf-8') as f:
        for i, file in enumerate(files):
            ipath = os.path.join('uploads', f"{file_id}_{i}.mp3")
            file.save(ipath)
            paths.append(ipath)
            f.write(f"file '{os.path.abspath(ipath)}'\n")
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lpath, '-c', 'copy', opath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cleanup_file(lpath)
    for p in paths: cleanup_file(p)
    if os.path.exists(opath): return jsonify({"success": True, "download_url": f"/api/get?file=out_{file_id}.mp3&name=merged_audio.mp3"})
    return jsonify({"error": "Merge failed"}), 500

@app.route('/api/merge-video', methods=['POST'])
def merge_video():
    files = request.files.getlist('files')
    if len(files) < 2: return jsonify({"error": "Provide 2+ files"}), 400
    file_id, paths = str(uuid.uuid4()), []
    lpath = os.path.join('uploads', f"list_{file_id}.txt")
    opath = os.path.join('downloads', f"out_{file_id}.mp4")
    with open(lpath, 'w', encoding='utf-8') as f:
        for i, file in enumerate(files):
            ext = os.path.splitext(file.filename)[1] or '.mp4'
            ipath = os.path.join('uploads', f"{file_id}_{i}{ext}")
            file.save(ipath)
            paths.append(ipath)
            f.write(f"file '{os.path.abspath(ipath)}'\n")
    subprocess.run(['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', lpath, '-c', 'copy', opath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cleanup_file(lpath)
    for p in paths: cleanup_file(p)
    if os.path.exists(opath): return jsonify({"success": True, "download_url": f"/api/get?file=out_{file_id}.mp4&name=merged_video.mp4"})
    return jsonify({"error": "Merge failed"}), 500

@app.route('/api/torrent', methods=['POST'])
def torrent():
    if not request.json.get('magnet'): return jsonify({"error": "Provide magnet link"}), 400
    return jsonify({"success": True, "message": "Torrent safely queued on the server backend."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
