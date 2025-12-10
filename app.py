from flask import Flask, request, jsonify
import requests
import yt_dlp
import os

app = Flask(__name__)

VERIFY_TOKEN = "MY_VERIFY_TOKEN"  
PAGE_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"
PAGE_ID = "YOUR_PAGE_ID"


def download_video(url):
    file = "video.mp4"
    ydl_opts = {"outtmpl": file}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return file


def upload_to_facebook_video(path):
    url = f"https://graph.facebook.com/{PAGE_ID}/videos"
    files = {"file": open(path, "rb")}
    data = {"access_token": PAGE_TOKEN}
    r = requests.post(url, files=files, data=data)
    return r.json()


def reply_to_comment(comment_id, message):
    url = f"https://graph.facebook.com/{comment_id}/comments"
    data = {"message": message, "access_token": PAGE_TOKEN}
    requests.post(url, data=data)


@app.route("/webhook", methods=["GET"])
def verify_webhook():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Error: Wrong verification token"


@app.route("/webhook", methods=["POST"])
def receive_updates():
    data = request.json

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "comment_id" in value:
            comment_id = value["comment_id"]
            message = value["message"]

            if "youtube.com" in message or "youtu.be" in message:

                # تحميل الفيديو
                path = download_video(message)

                # رفعه لصفحتك
                res = upload_to_facebook_video(path)

                video_id = res.get("id")
                link = f"https://facebook.com/{PAGE_ID}/videos/{video_id}/"

                # الرد على التعليق
                reply_to_comment(comment_id, f"تم تحويل الفيديو: {link}")

                os.remove(path)

    except Exception as e:
        print("Error:", e)

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080) 
