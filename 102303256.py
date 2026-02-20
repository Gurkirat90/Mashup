
import sys
import os
import shutil
from yt_dlp import YoutubeDL
from pydub import AudioSegment

def validate_inputs(args):
    if len(args) != 5:
        print("Usage: python <program.py> <SingerName> <NumberOfVideos> <AudioDuration> <OutputFileName>")
        sys.exit(1)

    singer = args[1]
    
    try:
        num_videos = int(args[2])
        duration = int(args[3])
    except ValueError:
        print("NumberOfVideos and AudioDuration must be integers.")
        sys.exit(1)

    if num_videos <= 10:
        print("NumberOfVideos must be greater than 10.")
        sys.exit(1)

    if duration <= 20:
        print("AudioDuration must be greater than 20 seconds.")
        sys.exit(1)

    output_file = args[4]
    return singer, num_videos, duration, output_file


def download_videos(singer, num_videos):
    os.makedirs("downloads", exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
        'default_search': 'ytsearch'
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch{num_videos}:{singer} songs"])


def convert_and_trim(duration):
    os.makedirs("processed", exist_ok=True)

    for file in os.listdir("downloads"):
        file_path = os.path.join("downloads", file)
        try:
            audio = AudioSegment.from_file(file_path)
            trimmed = audio[:duration * 1000]
            trimmed.export(os.path.join("processed", file.split('.')[0] + ".mp3"), format="mp3")
        except Exception as e:
            print(f"Error processing {file}: {e}")


def merge_audios(output_file):
    combined = AudioSegment.empty()
    for file in os.listdir("processed"):
        audio = AudioSegment.from_mp3(os.path.join("processed", file))
        combined += audio
    combined.export(output_file, format="mp3")


def cleanup():
    shutil.rmtree("downloads", ignore_errors=True)
    shutil.rmtree("processed", ignore_errors=True)


def main():
    singer, num_videos, duration, output_file = validate_inputs(sys.argv)
    try:
        print("Downloading videos...")
        download_videos(singer, num_videos)

        print("Converting and trimming...")
        
        convert_and_trim(duration)

        print("Merging audios...")
        merge_audios(output_file)

        print("Mashup created successfully:", output_file)

    except Exception as e:
        print("Error occurred:", e)

    finally:
        cleanup()


if __name__ == "__main__":
    main()
