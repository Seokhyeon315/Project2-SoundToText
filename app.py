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
import magic

load_dotenv()
MAX_SIZE=25000000 # 25MB


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", '-i', type=str,required=True, help="YouTube video link")
    args = parser.parse_args()
    url = args.input
    yt = YouTube(url)
    title = yt.title
    length = yt.length
    # video detail
    detail = yt.description
    print(f"Video title: {title}")

    if detail is None:
        print("No video description")
    else:
        print(f"Video description: {detail}")

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
        print("Audio file size is more than 25MB. Splitting into 25MB chunks...")
        split_audio(temp_audio_file)
    else:
       transcribe_to_en(temp_audio_file)
       #transcribe(temp_audio_file)

    temp_audio_file.close()


# split audio function
def split_audio(audio_file):
    # Split audio file into 25MB chunks
    chunk_size=MAX_SIZE
    chunk_num=0
    while True:
        chunk=audio_file.read(chunk_size)
        if not chunk:
            break
        chunk_num+=1
        chunk_file=NamedTemporaryFile(delete=False, suffix=".wav")
        chunk_file.write(chunk)

        chunk_file.flush()
        chunk_file.seek(0)
        transcribe_to_en(chunk_file)
        #transcribe(chunk_file)
        chunk_file.close()
        print(f"Chunk {chunk_num} transcribed or translated successfully!")



# # transcribe function using Open AI Whisper API
# def transcribe(audio_file):
#     openai.api_key = os.getenv("OPENAI_API_KEY")

#     file_obj=BytesIO(audio_file.read())
#     file_obj.name="audio_file.wav"
#     response=openai.Audio.translate("whisper-1", file_obj)
#     print(response['text'])
   


# translate function using Open AI Whisper API
def transcribe_to_en(audio_file):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    
    file_obj=BytesIO(audio_file.read())
    file_obj.name="audio_file.wav"
    response=openai.Audio.translate("whisper-1", file_obj , to_language="en")
    print(response['text'])




   


if __name__ == "__main__":
    main()


'''translation to english works for both below and above 25MB audio file size
But, I got this error after trancribe_to_en of more than 25MB audio file size, Traceback (most recent call last):
  File "/Users/seokhyeonbyun/Desktop/STT/backend/app.py", line 121, in <module>
    main()
  File "/Users/seokhyeonbyun/Desktop/STT/backend/app.py", line 68, in main
    split_audio(temp_audio_file)
  File "/Users/seokhyeonbyun/Desktop/STT/backend/app.py", line 90, in split_audio
    transcribe_to_en(chunk_file)
  File "/Users/seokhyeonbyun/Desktop/STT/backend/app.py", line 113, in transcribe_to_en
    response=openai.Audio.translate("whisper-1", file_obj , to_language="en")
  File "/Users/seokhyeonbyun/Desktop/STT/backend/stt-venv/lib/python3.10/site-packages/openai/api_resources/audio.py", line 76, in translate
    response, _, api_key = requestor.request("post", url, files=files, params=data)
  File "/Users/seokhyeonbyun/Desktop/STT/backend/stt-venv/lib/python3.10/site-packages/openai/api_requestor.py", line 226, in request
    resp, got_stream = self._interpret_response(result, stream)
  File "/Users/seokhyeonbyun/Desktop/STT/backend/stt-venv/lib/python3.10/site-packages/openai/api_requestor.py", line 619, in _interpret_response
    self._interpret_response_line(
  File "/Users/seokhyeonbyun/Desktop/STT/backend/stt-venv/lib/python3.10/site-packages/openai/api_requestor.py", line 682, in _interpret_response_line
    raise self.handle_error_response(
openai.error.InvalidRequestError: Invalid file format. Supported formats: ['m4a', 'mp3', 'webm', 'mp4', 'mpga', 'wav', 'mpeg']
'''