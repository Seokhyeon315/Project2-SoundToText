'''
A program that takes a YouTube video link as an user input on terminal, extract high-quality of audio from the video.
Open AI whisper's translate function is used to translate the audio into English and transcribe it.
If the audio is English, it transcribes the audio into text using Open AI Whisper API's transcribe function.
If audio file size is more than 25MB, it will be split into 25MB chunks and transcribe or translate each chunk.
Finally, the transcribe or translate function is done, print the text to the terminal and price of the API call.
Price of the API call is $0.006 per minute.
'''

from dotenv import load_dotenv
import os
import openai
from pytube import YouTube
import argparse
from io import BytesIO
from tempfile import NamedTemporaryFile
from googletrans import Translator


load_dotenv()
MAX_SIZE=25000000 # 25MB


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", '-i', type=str,required=True, help="YouTube video link")
    args = parser.parse_args()
    url = args.input
    yt = YouTube(url)
    title = yt.title
    length = yt.length # length in seconds
    # video detail
    detail = yt.description
    print(f"Video title: {title}")

    if detail is None:
        print("No video description")
    else:
        # print(f"Video description: {detail}")
        pass

    # Print video length in hrs, mins, secs
    hours = length // 3600
    minutes = (length % 3600) // 60
    seconds = length % 60
    print(f"Video length: {hours} hrs {minutes} mins {seconds} secs")


    # Get the highest resolution audio stream
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first() # Orders streams by their audio bit rate (abr) in descending order, and finally selects the first (i.e., highest bit rate) audio stream.
    print(f"Audio file size: {audio_stream.filesize} bytes")
    print(f"Audio file size: {audio_stream.filesize/1000000} MB") # 1MB=1000000bytes

    temp_audio_file=NamedTemporaryFile(delete=False, suffix=".wav")
    audio_stream.stream_to_buffer(temp_audio_file)

    # audio_size
    audio_size=temp_audio_file.tell()

    # Flush the contents of the temporary file to disk
    temp_audio_file.flush()
    temp_audio_file.seek(0)

    # If audio file size is more than 25MB, split into 25MB chunks and transcribe or translate each chunk based on detected language
    if audio_size > MAX_SIZE:
        print("It supports only below 25 MB of audio file size. ")
    else:
       transcribe_to_en(temp_audio_file)
       
    temp_audio_file.close()


# transcribe function using Open AI Whisper API's translate
def transcribe_to_en(audio_file):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    file_obj=BytesIO(audio_file.read())
    file_obj.name="audio_file.wav"
    response=openai.Audio.translate("whisper-1", file_obj, file_obj.name, to_language="en")
    #print(f"Translate into English: {response['text']}")

    # pass response['text'] to google_translate function 
    google_translate(audio_file)

    return response['text']


# translate functiion using Google translate API get english text from transcribe_to_en function
def google_translate(audio):
    translator = Translator()
    ENG_TEXT = transcribe_to_en(audio)
    result=translator.translate(ENG_TEXT, dest='kr')
    
    print(f"한글번역: {result.text}")
    
    

if __name__ == "__main__":
    main()