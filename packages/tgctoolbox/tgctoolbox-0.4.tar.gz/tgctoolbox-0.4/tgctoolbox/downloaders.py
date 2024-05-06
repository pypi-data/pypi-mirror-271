import os
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

import requests
from moviepy.editor import AudioFileClip
from pytube import YouTube
from tqdm import tqdm

from .logger import setup_custom_logger as TGCLoggerSetup

logger = TGCLoggerSetup(__name__)


def download_vosk_model(model_name, destination_folder) -> bool:
    model_url = f"https://alphacephei.com/vosk/models/vosk-model-{model_name}.zip"

    try:
        # Creating destination folder if it doesn't exist
        Path(destination_folder).mkdir(parents=True, exist_ok=True)

        logger.info(f"Downloading model '{model_name}' from {model_url}")

        # Downloading the model
        response = requests.get(model_url)
        if response.status_code == 404:  # Model not found
            logger.error(
                f"Model '{model_name}' not found. Please check the model name and try again."
            )
            return False
        elif response.status_code != 200:  # Other HTTP error
            response.raise_for_status()

        # Unzipping the model
        with ZipFile(BytesIO(response.content)) as model_zip:
            model_zip.extractall(destination_folder)

        logger.info(
            f"Model '{model_name}' downloaded and extracted to {destination_folder}"
        )
        return True

    except requests.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}", exc_info=True)
    except Exception as err:
        print(f"An error occurred: {err}", exc_info=True)


def download_file(url, filename):
    """
    Download a file from a URL and display a progress bar.

    Args:
        url (str): The URL of the file to download.
        filename (str): The name to save the file as.
    """
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                progress_bar.update(len(chunk))
                if chunk:
                    file.write(chunk)

        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
    else:
        print(f"Failed to download file. HTTP response code: {response.status_code}")


def download_video_as_wav(youtube_link, output_filename):
    # Step 1: Download YouTube video
    yt = YouTube(youtube_link)
    video = yt.streams.filter(only_audio=True).first()
    download_path = video.download()

    # Step 2: Convert the downloaded file to WAV
    video_clip = AudioFileClip(download_path)
    video_clip.write_audiofile(f"{output_filename}.wav")

    # Optional: Remove the original download (if you want to keep only the WAV file)
    os.remove(download_path)
