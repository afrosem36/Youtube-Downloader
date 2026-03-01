import os
import re
import time
import uuid
import secrets
import logging
import threading
import random
from urllib.parse import urlparse

import yt_dlp
from flask import Flask, render_template, request, send_file, jsonify, Response, stream_with_context

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

# =============================================================================
# CONSTANTS & ROTATING USER-AGENTS
# =============================================================================

ALLOWED_DOMAINS = {
    "youtube.com", "www.youtube.com",
    "youtu.be",    "www.youtu.be",
    "m.youtube.com", "music.youtube.com",
}
MAX_RESOLUTION    = 2160
VALID_RESOLUTIONS = [144, 240, 360, 480, 720, 1080, 1440, 2160]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15",
]

# =============================================================================
# CUSTOM EXCEPTIONS
# =============================================================================

class BotDetectionError(Exception):
    pass

class AgeRestrictedError(Exception):
    pass

class GeoblockingError(Exception):
    pass

class FormatUnavailableError(Exception):
    pass

# =============================================================================
# VALIDATORS
# =============================================================================

def validate_youtube_url(url: str):
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
    try:
        res_int = int(res)
    except (TypeError, ValueError):
        return False, 0, "Resolution must be a number."
    if res_int > MAX_RESOLUTION:
        return False, 0, f"Max resolution allowed is {MAX_RESOLUTION}p."
    if res_int not in VALID_RESOLUTIONS:
        return False, 0, f"Invalid resolution: {res_int}p."
    return True, res_int, ""

# =============================================================================
# SECURITY — UNLOCK TOKENS
# =============================================================================

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

# =============================================================================
# TASK TRACKER
# =============================================================================

_tasks: dict = {}
_tasks_lock = threading.Lock()


def _task_create(task_id: str):
    with _tasks_lock:
        _tasks[task_id] = {
            "status":   "queued",
            "progress": 0,
            "speed":    "",
            "eta":      "",
            "filepath": None,
            "error":    None,
        }


def _task_update(task_id: str, **kwargs):
    with _tasks_lock:
        if task_id in _tasks:
            _tasks[task_id].update(kwargs)


def _task_get(task_id: str) -> dict:
    with _tasks_lock:
        return dict(_tasks.get(task_id, {}))


def _task_cleanup(task_id: str):
    with _tasks_lock:
        _tasks.pop(task_id, None)

# =============================================================================
# YT-DLP HELPERS
# =============================================================================

def _random_sleep():
    time.sleep(random.uniform(0.8, 2.4))


def _classify_error(e: Exception) -> Exception:
    msg = str(e).lower()
    if any(k in msg for k in ("sign in", "bot", "403", "forbidden", "cookie")):
        return BotDetectionError(
            "YouTube blocked the request. Cookies may have expired. "
            "Please re-export your cookies.txt and redeploy."
        )
    if "age" in msg and ("restrict" in msg or "confirm" in msg):
        return AgeRestrictedError(
            "This video is age-restricted. Sign-in cookies are required."
        )
    if any(k in msg for k in ("not available in your country", "geoblocked", "geo")):
        return GeoblockingError(
            "This video is not available in the server's region."
        )
    if "requested format is not available" in msg:
        return FormatUnavailableError(
            "The selected resolution is not available for this video. "
            "Please choose a lower resolution."
        )
    return e


def _build_ydl_opts(extra: dict, task_id: str = None) -> dict:
    ua = random.choice(USER_AGENTS)
    base = {
        "quiet":          True,
        "no_warnings":    True,
        "socket_timeout": 20,
        "http_headers":   {"User-Agent": ua},
        "extractor_args": {
            "youtube": {
                "player_client": ["ios", "android", "web"],
            }
        },
    }

    if os.path.exists(COOKIES_PATH):
        base["cookiefile"] = COOKIES_PATH
        logger.info("Using cookies.txt for authentication.")
    else:
        logger.warning("No cookies.txt found — requests may be rate-limited.")

    if task_id:
        def _progress_hook(d):
            if d["status"] == "downloading":
                raw_pct = d.get("_percent_str", "0%").strip().replace("%", "")
                try:
                    pct = float(raw_pct)
                except ValueError:
                    pct = 0
                _task_update(task_id,
                             status="downloading",
                             progress=round(pct, 1),
                             speed=d.get("_speed_str", "").strip(),
                             eta=d.get("_eta_str", "").strip())
            elif d["status"] == "finished":
                _task_update(task_id, progress=99, status="downloading")

        base["progress_hooks"] = [_progress_hook]

    base.update(extra)
    return base


def _format_duration(seconds) -> str:
    if not seconds:
        return "Unknown"
    seconds = int(seconds)
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

# =============================================================================
# INFO CACHE
# =============================================================================

_info_cache: dict = {}
CACHE_TTL = 300


def _cached_get(url: str):
    entry = _info_cache.get(url)
    if entry and time.time() < entry["expires"]:
        logger.info(f"Cache hit: {url}")
        return entry["data"]
    return None


def _cache_set(url: str, data: dict):
    _info_cache[url] = {"data": data, "expires": time.time() + CACHE_TTL}

# =============================================================================
# CORE SERVICE FUNCTIONS
# =============================================================================

def get_video_info(url: str) -> dict:
    cached = _cached_get(url)
    if cached:
        return cached

    _random_sleep()

    try:
        with yt_dlp.YoutubeDL(_build_ydl_opts({"skip_download": True})) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as e:
        raise _classify_error(e)
    except Exception as e:
        logger.exception(f"Unexpected error fetching info for {url}")
        raise _classify_error(e)

    formats = info.get("formats", [])
    resolutions = sorted(
        list(set(f["height"] for f in formats if f.get("height") and f["height"] > 0)),
        reverse=True,
    )
    result = {
        "title":       info.get("title", "Unknown Title"),
        "thumbnail":   info.get("thumbnail", ""),
        "duration":    _format_duration(info.get("duration")),
        "resolutions": resolutions,
    }
    _cache_set(url, result)
    return result


def _download_worker(task_id: str, url: str, resolution: int):
    safe_name = f"{uuid.uuid4().hex}.mp4"
    filepath  = os.path.join(DOWNLOAD_FOLDER, safe_name)

    ydl_opts = _build_ydl_opts({
        "format":              f"bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]",
        "outtmpl":             filepath,
        "merge_output_format": "mp4",
        "retries":             5,
        "fragment_retries":    5,
        "postprocessors": [{
            "key":            "FFmpegVideoConvertor",
            "preferedformat": "mp4",
        }],
    }, task_id=task_id)

    _random_sleep()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if not os.path.exists(filepath):
            candidates = [
                f for f in os.listdir(DOWNLOAD_FOLDER)
                if f.startswith(safe_name.replace(".mp4", ""))
            ]
            if candidates:
                filepath = os.path.join(DOWNLOAD_FOLDER, candidates[0])
            else:
                raise FileNotFoundError("Downloaded file not found on disk.")

        _task_update(task_id, status="done", progress=100, filepath=filepath)
        logger.info(f"Task {task_id} complete: {filepath}")

    except yt_dlp.utils.DownloadError as e:
        err = _classify_error(e)
        logger.error(f"Task {task_id} failed: {err}")
        _task_update(task_id, status="error", error=str(err))
    except Exception as e:
        err = _classify_error(e)
        logger.exception(f"Task {task_id} unexpected error")
        _task_update(task_id, status="error", error=str(err))

# =============================================================================
# HELPERS
# =============================================================================

def _error(message: str, code: int = 400):
    return jsonify({"status": "error", "message": message, "code": code}), code


def _stream_and_delete(filepath: str):
    try:
        with open(filepath, "rb") as f:
            while True:
                chunk = f.read(1024 * 256)
                if not chunk:
                    break
                yield chunk
    finally:
        try:
            os.remove(filepath)
            logger.info(f"Streamed & deleted: {filepath}")
        except Exception as ex:
            logger.warning(f"Could not delete {filepath}: {ex}")

# =============================================================================
# ROUTES
# =============================================================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/get_info", methods=["POST"])
def route_get_info():
    data = request.get_json(silent=True) or {}
    url  = (data.get("url") or "").strip()

    valid, err = validate_youtube_url(url)
    if not valid:
        return _error(err)

    try:
        info = get_video_info(url)
    except BotDetectionError as e:
        return _error(str(e), 503)
    except AgeRestrictedError as e:
        return _error(str(e), 451)
    except GeoblockingError as e:
        return _error(str(e), 451)
    except FormatUnavailableError as e:
        return _error(str(e), 422)
    except Exception as e:
        return _error(f"Could not retrieve video info: {e}", 500)

    return jsonify({"status": "ok", **info})


@app.route("/get_token", methods=["POST"])
def route_get_token():
    token = generate_unlock_token()
    logger.info("4K unlock token issued.")
    return jsonify({"status": "ok", "token": token})


@app.route("/start_download", methods=["POST"])
def route_start_download():
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

    task_id = uuid.uuid4().hex
    _task_create(task_id)

    t = threading.Thread(
        target=_download_worker,
        args=(task_id, url, resolution),
        daemon=True,
    )
    t.start()

    return jsonify({"status": "ok", "task_id": task_id})


@app.route("/task_status/<task_id>", methods=["GET"])
def route_task_status(task_id: str):
    task = _task_get(task_id)
    if not task:
        return _error("Task not found.", 404)
    return jsonify({"status": "ok", **task})


@app.route("/fetch_file/<task_id>", methods=["GET"])
def route_fetch_file(task_id: str):
    task = _task_get(task_id)
    if not task:
        return _error("Task not found.", 404)
    if task["status"] != "done":
        return _error("File not ready yet.", 409)

    filepath = task.get("filepath")
    if not filepath or not os.path.exists(filepath):
        return _error("File missing on server.", 500)

    file_size = os.path.getsize(filepath)
    _task_cleanup(task_id)

    return Response(
        stream_with_context(_stream_and_delete(filepath)),
        mimetype="video/mp4",
        headers={
            "Content-Disposition": 'attachment; filename="video.mp4"',
            "Content-Length":      str(file_size),
        },
    )


# Legacy /download route — kept for backwards compatibility with index.html
@app.route("/download", methods=["POST"])
def route_download_legacy():
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
            return _error("4K unlock token missing or expired.", 403)

    task_id = uuid.uuid4().hex
    _task_create(task_id)
    _download_worker(task_id, url, resolution)

    task = _task_get(task_id)
    if task["status"] == "error":
        _task_cleanup(task_id)
        return _error(task["error"], 500)

    filepath = task.get("filepath")
    if not filepath or not os.path.exists(filepath):
        _task_cleanup(task_id)
        return _error("File was not created. Try a different resolution.", 500)

    file_size = os.path.getsize(filepath)
    _task_cleanup(task_id)

    return Response(
        stream_with_context(_stream_and_delete(filepath)),
        mimetype="video/mp4",
        headers={
            "Content-Disposition": 'attachment; filename="video.mp4"',
            "Content-Length":      str(file_size),
        },
    )


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
