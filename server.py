from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import threading

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def clean_old_files():
    import time, glob
    while True:
        time.sleep(3600)  # Clean every hour
        for f in glob.glob("downloads/*"):
            if os.path.getctime(f) < time.time() - 3600:
                os.remove(f)

threading.Thread(target=clean_old_files, daemon=True).start()

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data["url"]
    format_id = data["format"]

    ydl_opts = {
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'noplaylist': False,
    }

    if format_id == "mp3":
        ydl_opts.update({
            'format': 'bestaudio',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        })
    else:
        ydl_opts['format'] = format_id if format_id != "best" else "bestvideo+bestaudio/best"

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if format_id == "mp3":
                filename = filename.rsplit(".", 1)[0] + ".mp3"
            return jsonify({
                "success": True,
                "title": info.get("title", "Video"),
                "file": "/" + filename
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route("/downloads/<path:filename>")
def serve_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
