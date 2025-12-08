import subprocess
from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Stream Restream</title>
    <style>
        body { font-family: Arial; background:#ececec; padding:40px; }
        .box { background:white; padding:25px; border-radius:10px; width:400px; margin:auto; }
        input, button { width:100%; padding:12px; margin-top:12px; border-radius:6px; }
        button { background:#007bff; color:white; border:none; }
        h2 { text-align:center; }
    </style>
</head>
<body>
    <div class="box">
        <h2>M3U8 → Facebook Live</h2>
        <form method="POST">
            <label>M3U8 Stream URL:</label>
            <input name="m3u8" placeholder="Enter m3u8 link" required>

            <label>Facebook Stream Key:</label>
            <input name="key" placeholder="FB-xxxxxxxxxxxxx" required>

            <button type="submit">Start Streaming</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        m3u8 = request.form["m3u8"]
        key = request.form["key"]

        fb_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"

        cmd = [
            "ffmpeg",
            "-re",
            "-i", m3u8,
            "-c:v", "copy",
            "-c:a", "copy",
            "-f", "flv",
            fb_url
        ]

        subprocess.Popen(cmd)
        return "Streaming started successfully!"

    return render_template_string(HTML)

app.run(host="0.0.0.0", port=6080)
