import subprocess
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

PASSWORD = "556874"

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: Arial; 
            background:#ececec; 
            margin:0; 
            height: 100vh; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            flex-direction: column;
        }
        .server-status {
            position: absolute;
            top: 20px;
            font-size: 18px;
            color: green;
            font-weight: bold;
        }
        .box { 
            background:white; 
            padding:25px; 
            border-radius:10px; 
            width: 90%; 
            max-width: 400px; 
            box-sizing: border-box;
            text-align: center;
        }
        input, button { 
            width:100%; 
            padding:12px; 
            margin-top:10px; 
            border-radius:6px; 
            box-sizing: border-box; 
            font-size:16px;
        }
        button { 
            background:#007bff; 
            color:white; 
            border:none; 
        }
        h2 { 
            margin-bottom: 15px; 
        }
        p.error { color:red; margin-top:10px; }

        @media (max-width: 480px) {
            .box { padding: 15px; }
            input, button { padding: 10px; font-size: 14px; }
            h2 { font-size: 18px; }
            .server-status { font-size: 16px; }
        }
    </style>
</head>
<body>
    <div class="server-status">Server Active</div>
    <div class="box">
        <h2>Enter Password to Access</h2>
        <form method="POST">
            <input name="password" placeholder="Password" type="password" required>
            <button type="submit">Login</button>
        </form>
        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Stream Restream</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial; background:#ececec; padding:20px; margin:0; }
        .box { background:white; padding:20px; border-radius:10px; max-width: 100%; width: 100%; margin:auto; box-sizing: border-box; }
        input, button { width:100%; padding:12px; margin-top:10px; border-radius:6px; box-sizing: border-box; font-size:16px; }
        button { background:#007bff; color:white; border:none; }
        h2 { text-align:center; font-size:20px; }
        @media (max-width: 480px) {
            body { padding: 10px; }
            .box { padding: 15px; }
            input, button { padding: 10px; font-size: 14px; }
            h2 { font-size: 18px; }
        }

        /* Modal Styles */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0,0,0,0.5);
        }
        .modal-content {
            background-color: #fff;
            margin: 15% auto;
            padding: 20px;
            border-radius: 10px;
            max-width: 300px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
        }
        .close-btn {
            margin-top: 15px;
            padding: 10px 20px;
            background:#007bff;
            color:white;
            border:none;
            border-radius:6px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>Panel Restream</h2>
        <form method="POST" id="streamForm">
            <label>link Stream URL:</label>
            <input name="m3u8" placeholder="Enter Source link" required>

            <label>Facebook Stream Key:</label>
            <input name="key" placeholder="FB-xxxxxxxxxxxxx" required>

            <button type="submit">GO LIVE</button>
        </form>
    </div>

    <!-- Modal -->
    <div id="successModal" class="modal">
        <div class="modal-content">
            <p>Streaming started successfully!</p>
            <button class="close-btn" onclick="closeModal()">OK</button>
        </div>
    </div>

    <script>
        function closeModal() {
            document.getElementById("successModal").style.display = "none";
        }

        {% if success %}
            document.getElementById("successModal").style.display = "block";
        {% endif %}
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        password = request.form.get("password")
        if password == PASSWORD:
            return redirect(url_for("index"))
        else:
            error = "Incorrect password"
    return render_template_string(LOGIN_HTML, error=error)

@app.route("/stream", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        m3u8 = request.form["m3u8"]
        key = request.form["key"]

        fb_url = f"rtmps://live-api-s.facebook.com:443/rtmp/{key}"

        subprocess.Popen([
            "ffmpeg",
            "-re",
            "-i", m3u8,
            "-c:v", "copy",
            "-c:a", "copy",
            "-f", "flv",
            fb_url
        ])

        return render_template_string(HTML, success=True)

    return render_template_string(HTML)

app.run(host="0.0.0.0", port=6080)
