from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

# أوامر مسموحة فقط (للحماية)
ALLOWED_CMDS = [
    "ls", "pwd", "whoami", "uname", "df -h", "uptime",
    "cat", "id", "ps", "date"
]

@app.route("/")
def index():
    return render_template("terminal.html")

@app.route("/run", methods=["POST"])
def run():
    cmd = request.json.get("cmd", "").strip()

    # منع الأوامر الخطيرة مثل rm أو shutdown
    dangerous = ["rm", "shutdown", "reboot", "mv", "kill", "nano", "vi", "wget", "curl"]
    if any(cmd.startswith(d) for d in dangerous):
        return jsonify({"output": "❌ Command not allowed for safety."})

    # تنفيذ الأمر
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
    except Exception as e:
        result = str(e)

    return jsonify({"output": result})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000) 
