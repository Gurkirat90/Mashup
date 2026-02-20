
from flask import Flask, request, render_template_string
import os
import zipfile
import smtplib
from email.message import EmailMessage
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import shutil

app = Flask(__name__)

HTML_FORM = """
<h2>Mashup Generator</h2>
<form method="post">
Singer Name: <input name="singer"><br><br>
Number of Videos: <input name="num"><br><br>
Duration (sec): <input name="duration"><br><br>
Email: <input name="email"><br><br>
<input type="submit">
</form>
"""

def create_mashup(singer, num, duration, output_name):
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("processed", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'default_search': 'ytsearch'
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num}:{singer} songs"])

    for file in os.listdir("downloads"):
        audio = AudioSegment.from_file(os.path.join("downloads", file))
        trimmed = audio[:int(duration) * 1000]
        trimmed.export(os.path.join("processed", file.split('.')[0] + ".mp3"), format="mp3")

    combined = AudioSegment.empty()
    for file in os.listdir("processed"):
        audio = AudioSegment.from_mp3(os.path.join("processed", file))
        combined += audio

    combined.export(output_name, format="mp3")

    shutil.rmtree("downloads", ignore_errors=True)
    shutil.rmtree("processed", ignore_errors=True)


def send_email(receiver_email, file_path):
    sender_email = os.environ.get("EMAIL_USER")
    sender_password = os.environ.get("EMAIL_PASS")

    msg = EmailMessage()
    msg["Subject"] = "Your Mashup File"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    with open(file_path, "rb") as f:
        file_data = f.read()

    msg.add_attachment(file_data, maintype="audio", subtype="mp3", filename="mashup.mp3")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        singer = request.form["singer"]
        num = int(request.form["num"])
        duration = int(request.form["duration"])
        email = request.form["email"]

        output_name = "mashup.mp3"
        create_mashup(singer, num, duration, output_name)
        send_email(email, output_name)

        return "Mashup sent to your email!"

    return render_template_string(HTML_FORM)


if __name__ == "__main__":
    app.run(debug=True)
