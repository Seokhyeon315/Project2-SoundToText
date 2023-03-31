'''
A program that takes a YouTube video link as an user input on terminal, extract high-quality of audio from the video.
Using Open AI whisper's translate function is used to translate the audio into English and transcribe it.
If audio file size is more than 25MB, it will be split into 25MB chunks and transcribe or translate each chunk.
Finally, the transcribe or translate function is done, print the text to the terminal.
Price of the API call is $0.006 per minute.
Make this code to integrate with Fast API.
'''

from dotenv import load_dotenv
import os
import openai
from pytube import YouTube
import argparse
from google.oauth2 import service_account
from google.cloud import translate_v3 as translate



load_dotenv()
GOOGLE_PROJECT_ID=os.getenv("GOOGLE_PROJECT_ID")
MAX_SIZE=25000000 # 25MB


# main 함수의 역할은 터미널에서 테스트하는 용도.
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", '-i', type=str,required=True, help="YouTube video link")
    args = parser.parse_args()
    url = args.input
    #extract_audio(url)

    # assign audio and audio_size as variable
    audio_stream, audio_size_MB =extract_audio(url)

    if audio_size_MB > MAX_SIZE:
        print("Audio size is more than 25MB, starting chunk files... ")
        # chunkAudio(audio_stream)
        # transcribe_to_english(chunked_files)
        
    else:
        # transcript audio to english
        ENG_TEXT=transcribe_to_english(audio_stream)
        translate_text(ENG_TEXT, GOOGLE_PROJECT_ID)
        

    return url



# extract audio from youtube video
# Maybe allow users to download extracted audio using this function and save it to their local machine.
def extract_audio(url: str):
    yt=YouTube(url)
    title = yt.title
    length = yt.length # length in seconds

    # Print video length in hrs, mins, secs
    hours = length // 3600
    minutes = (length % 3600) // 60
    seconds = length % 60
    print(f"Video title: {title} \n")
    print(f"Video length: {hours} hrs {minutes} mins {seconds} secs")

    # Get the highest resolution audio stream
    # Type of audio-stream is : <class 'pytube.streams.Stream'>
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first() # Orders streams by their audio bit rate (abr) in descending order, and finally selects the first (i.e., highest bit rate) audio stream.
    
    # audio size in bytes
    audio_size=audio_stream.filesize
    
    # audio size in MB, 1MB=1000000bytes
    audio_size_MB=audio_size/1000000

    print(f"Audio file size: {audio_size_MB} MB")

    return audio_stream, audio_size_MB




# Transcribe in English text
def transcribe_to_english(audio_stream):
    openai.api_key = os.getenv("OPENAI_API_KEY")
   
    # audio file path
    media_file_path=audio_stream.download(
        output_path=os.path.join(os.getcwd(), 'audio'),
        filename='audio.wav',

    )

    media_file=open(media_file_path, 'rb')
    
    # transcribe audio to english
    response=openai.Audio.translate(
      model='whisper-1',
      file=media_file,
      to_language='en',
    )
    
    #print(f"English text: \n {response.text}")

    # remove audio file
    os.remove(media_file_path)

    return response.text



# translate functiion using Google translate API 
# get english text from transcribe_to_en function



credentials = service_account.Credentials.from_service_account_file('credential.json')


def translate_text(text, project_id=GOOGLE_PROJECT_ID):
    client = translate.TranslationServiceClient(credentials=credentials)
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"
    response = client.translate_text(
        request={
           "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # mime types: text/plain, text/html
            "source_language_code": "en-US",
            "target_language_code": "ko",
        }
    )

    # Display the translated text from response
    print(f"Translated text: \n {response.translations[0].translated_text}")

    

# Chunk audio file into 25MB chunks and return a list of chunks
# def chunkAudio(audio_stream):
#     pass


if __name__ == "__main__":
    main()



'''
Traceback (most recent call last):
  File "/Users/seokhyeonbyun/Desktop/STT/backend/app.py", line 148, in <module>
    main()
  File "/Users/seokhyeonbyun/Desktop/STT/backend/app.py", line 43, in main
    translate_text(ENG_TEXT, GOOGLE_PROJECT_ID)
  File "/Users/seokhyeonbyun/Desktop/STT/backend/app.py", line 118, in translate_text
    client = translate.TranslationServiceClient()
  File "/Users/seokhyeonbyun/Desktop/STT/backend/stt-venv/lib/python3.10/site-packages/google/cloud/translate_v3/services/translation_service/client.py", line 436, in __init__
    self._transport = Transport(
  File "/Users/seokhyeonbyun/Desktop/STT/backend/stt-venv/lib/python3.10/site-packages/google/cloud/translate_v3/services/translation_service/transports/grpc.py", line 152, in __init__
    super().__init__(
  File "/Users/seokhyeonbyun/Desktop/STT/backend/stt-venv/lib/python3.10/site-packages/google/cloud/translate_v3/services/translation_service/transports/base.py", line 103, in __init__
    credentials, _ = google.auth.default(
  File "/Users/seokhyeonbyun/Desktop/STT/backend/stt-venv/lib/python3.10/site-packages/google/auth/_default.py", line 648, in default
    raise exceptions.DefaultCredentialsError(_CLOUD_SDK_MISSING_CREDENTIALS)
google.auth.exceptions.DefaultCredentialsError: Your default credentials were not found. To set up Application Default Credentials, see https://cloud.google.com/docs/authentication/external/set-up-adc for more information.
'''