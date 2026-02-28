import os
import re
import time
import secrets
import logging
import threading
from urllib.parse import urlparse

import yt_dlp
from flask import Flask, render_template, request, send_file, jsonify, after_this_request

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# ── App Setup ─────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder=".")

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
COOKIES_PATH    = os.path.join(BASE_DIR, "cookies.txt")

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ═════════════════════════════════════════════════════════════════════════════
# VALIDATORS
# ═════════════════════════════════════════════════════════════════════════════

ALLOWED_DOMAINS = {
    "youtube.com", "www.youtube.com",
    "youtu.be", "www.youtu.be",
    "m.youtube.com", "music.youtube.com"
}
MAX_RESOLUTION    = 2160
VALID_RESOLUTIONS = [144, 240, 360, 480, 720, 1080, 1440, 2160]


def validate_youtube_url(url: str):
    """Returns (is_valid, error_message)."""
    if not url or not isinstance(url, str):
        return False, "No URL provided."
    url = url.strip()
    try:
        parsed = urlparse(url)
    except Exception:
        return False, "Malformed URL."
    if parsed.scheme not in ("http", "https"):
        return False, "URL must use http or https."
    if parsed.netloc not in ALLOWED_DOMAINS:
        return False, f"Only YouTube URLs are allowed. Got: {parsed.netloc}"
    pattern = re.compile(
        r'(youtube\.com/watch\?.*v=[\w-]+|youtu\.be/[\w-]+|youtube\.com/shorts/[\w-]+)'
    )
    if not pattern.search(url):
        return False, "URL does not appear to be a valid YouTube video link."
    return True, ""


def validate_resolution(res):
    """Returns (is_valid, res_int, error_message)."""
    try:
        res_int = int(res)
    except (TypeError, ValueError):
        return False, 0, "Resolution must be a number."
    if res_int > MAX_RESOLUTION:
        return False, 0, f"Max resolution allowed is {MAX_RESOLUTION}p."
    if res_int not in VALID_RESOLUTIONS:
        return False, 0, f"Invalid resolution: {res_int}p."
    return True, res_int, ""


# ═════════════════════════════════════════════════════════════════════════════
# SECURITY
# ═════════════════════════════════════════════════════════════════════════════

_token_store: dict = {}
TOKEN_TTL_SECONDS  = 120


def generate_unlock_token() -> str:
    token = secrets.token_urlsafe(32)
    _token_store[token] = time.time() + TOKEN_TTL_SECONDS
    return token


def validate_unlock_token(token: str) -> bool:
    if not token or token not in _token_store:
        return False
    if time.time() > _token_store[token]:
        del _token_store[token]
        return False
    del _token_store[token]
    return True


def sanitize_filename(name: str) -> str:
    name = re.sub(r'[/\\?%*:|"<>\x00]', '_', name)
    name = name.strip('. ')
    return name[:200] or "video"


def is_safe_path(base_dir: str, filepath: str) -> bool:
    return os.path.realpath(filepath).startswith(os.path.realpath(base_dir))


# ═════════════════════════════════════════════════════════════════════════════
# DOWNLOADER SERVICE
# ═════════════════════════════════════════════════════════════════════════════

_info_cache: dict = {}
CACHE_TTL = 300  # 5 minutes


def _cached_get(url: str):
    entry = _info_cache.get(url)
    if entry and time.time() < entry["expires"]:
        logger.info(f"Cache hit: {url}")
        return entry["data"]
    return None


def _cache_set(url: str, data: dict):
    _info_cache[url] = {"data": data, "expires": time.time() + CACHE_TTL}


def _build_ydl_opts(extra: dict) -> dict:
    base = {"quiet": True, "no_warnings": True, "socket_timeout": 15}
    if os.path.exists(COOKIES_PATH):
        base["cookiefile"] = COOKIES_PATH
    base.update(extra)
    return base


def _format_duration(seconds) -> str:
    if not seconds:
        return "Unknown"
    seconds = int(seconds)
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def get_video_info(url: str) -> dict:
    cached = _cached_get(url)
    if cached:
        return cached
    try:
        with yt_dlp.YoutubeDL(_build_ydl_opts({})) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"yt-dlp error for {url}: {e}")
        raise ValueError(f"Could not retrieve video info: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error for {url}")
        raise ValueError(f"Unexpected error: {e}")

    formats     = info.get("formats", [])
    resolutions = sorted(
        list(set(f["height"] for f in formats if f.get("height") and f["height"] > 0)),
        reverse=True
    )
    result = {
        "title":       info.get("title", "Unknown Title"),
        "thumbnail":   info.get("thumbnail", ""),
        "duration":    _format_duration(info.get("duration")),
        "resolutions": resolutions,
    }
    _cache_set(url, result)
    return result


def download_video(url: str, resolution: int) -> str:
    outtmpl  = os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s")
    ydl_opts = _build_ydl_opts({
        "format":               f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]",
        "outtmpl":              outtmpl,
        "merge_output_format":  "mp4",
        "retries":              3,
        "postprocessors": [{
            "key":             "FFmpegVideoConvertor",
            "preferedformat":  "mp4",
        }],
    })
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info     = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            if not filepath.endswith(".mp4"):
                mp4 = os.path.splitext(filepath)[0] + ".mp4"
                if os.path.exists(mp4):
                    filepath = mp4
    except yt_dlp.utils.DownloadError as e:
        logger.error(f"Download error {url} @ {resolution}p: {e}")
        raise ValueError(f"Download failed: {e}")
    except Exception as e:
        logger.exception(f"Unexpected download error for {url}")
        raise ValueError(f"Unexpected error: {e}")

    if not is_safe_path(DOWNLOAD_FOLDER, filepath):
        raise ValueError("Path traversal detected. Aborting.")

    return filepath


# ═════════════════════════════════════════════════════════════════════════════
# ROUTES
# ═════════════════════════════════════════════════════════════════════════════

def _error(message: str, code: int = 400):
    return jsonify({"status": "error", "message": message, "code": code}), code


def _delete_after_send(filepath: str):
    def _rm():
        try:
            os.remove(filepath)
            logger.info(f"Cleaned up: {filepath}")
        except Exception as e:
            logger.warning(f"Could not delete {filepath}: {e}")
    threading.Thread(target=_rm, daemon=True).start()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_info", methods=["POST"])
def get_info():
    data = request.get_json(silent=True) or {}
    url  = (data.get("url") or "").strip()

    valid, err = validate_youtube_url(url)
    if not valid:
        return _error(err)

    try:
        info = get_video_info(url)
    except ValueError as e:
        return _error(str(e))

    return jsonify({"status": "ok", **info})


@app.route("/get_token", methods=["POST"])
def get_token():
    token = generate_unlock_token()
    logger.info("4K unlock token issued.")
    return jsonify({"status": "ok", "token": token})


@app.route("/download", methods=["POST"])
def download():
    url     = (request.form.get("url") or "").strip()
    res_raw = request.form.get("resolution")
    token   = (request.form.get("unlock_token") or "").strip()

    valid, err = validate_youtube_url(url)
    if not valid:
        return _error(err)

    valid, resolution, err = validate_resolution(res_raw)
    if not valid:
        return _error(err)

    if resolution == 2160:
        if not validate_unlock_token(token):
            return _error("4K unlock token missing or expired. Please complete the unlock step.", 403)

    try:
        filepath = download_video(url, resolution)
    except ValueError as e:
        return _error(str(e), 500)

    if not os.path.exists(filepath):
        return _error("File was not created. Try a different resolution.", 500)

    @after_this_request
    def cleanup(response):
        _delete_after_send(filepath)
        return response

    return send_file(filepath, as_attachment=True)


# ═════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
