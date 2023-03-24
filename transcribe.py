# from app import main
import os
import openai
from dotenv import load_dotenv
from ytconvert import main

# load environment variables from .env file
load_dotenv()

audio_file=main()

# media_file_path='Build and Deploy an Amazing 3D Web Developer Portfolio in React JS | Beginner Three.js Tutorial.mp3'
# media_file=open(media_file_path,'rb')

# Get response from the OPEN AI api with whiper model
response=openai.Audio.transcribe(
    model='whisper-1',
    api_key=os.getenv("OPENAI_API_KEY"),
    file=audio_file,
    response_format='text', #text,json,srt,vtt

)

print(response)




# ytconvert 파일의 main() 함수에서 추출한 오디오파일을 전달받아서 transcribe 시킬 함수
# def transcribe_audio():
#     pass


# if __name__=="__transcribe_audio__":
#     transcribe_audio()