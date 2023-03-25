from io import BytesIO
from dotenv import load_dotenv
import os
import openai
from pytube import YouTube
from pydub import AudioSegment
from tempfile import NamedTemporaryFile
import argparse


'''
sample1: 'https://www.youtube.com/watch?v=KBo7mZHlink'
sample2: 'https://www.youtube.com/watch?v=E2NBQY-AWpk'
sample3: 'https://www.youtube.com/watch?v=0fYi8SGA20k'
sampel4: 'https://www.youtube.com/watch?v=PLC_3ZHkNag', 2분54초
'''

load_dotenv()

# Need to update this code to tell size of the file

def main():
    
    # Allow user to put video link on the terminal for now
    parser=argparse.ArgumentParser(description='Process a video file.')
    parser.add_argument("--input", "-i", type=str, required=True)
    # 어짜피 유튜브링크를 삽입할거니까, type=str
    args=parser.parse_args()
    user_input=args.input
    
    # Use user-inputted video link
    VIDEO_LINK=user_input
    yt=YouTube(VIDEO_LINK) # Assign YouTube object


   
    temp_audio_file=NamedTemporaryFile(delete=False)
    '''Creates a temporary file using the NamedTemporaryFile function from the tempfile module. 
    The delete=False argument ensures that the file is not deleted automatically when it is closed. 
    This temporary file will be used to store the audio stream from the YouTube video.'''
    
     # Extract audio from video
    yt.streams.filter(only_audio=True).first().stream_to_buffer(temp_audio_file)

    # Gets the size of the audio stream in bytes by using the tell() method on the temporary file object.
    audio_size = temp_audio_file.tell()

    # flushes the contents of the temporary file to disk. This ensures that the audio stream is saved to the file and can be accessed later
    temp_audio_file.flush()

    # Reset file pointer to beginning of temporary file, it allows audio stream can be read from the beginning of the file when it is later used in the code
    temp_audio_file.seek(0)


    # Convert length of video from seconds to hours, minutes, and seconds
    length_seconds = yt.length
    length_hours = length_seconds // 3600
    length_minutes = (length_seconds % 3600) // 60
    length_seconds = length_seconds % 60

    # Print video title, length, file size in bytes and megabytes
    print(f"User input link: {user_input}")
    print(f"The title: {yt.title}")
    print(f"The length of the video: {length_hours} hrs {length_minutes} mins {length_seconds} secs")
    print(f"The file size is {audio_size} bytes")
    print(f"And it is {audio_size/1000000} MB")

    # 1MB=1000000bytes

    # check file size to handle with openai api, 기준 25MB
    if audio_size < 25000000:
        print("It's less than 25MB, Good size")
       
        transcribe(temp_audio_file)
    else:
        print("Filesize is over 25MB, Not okay")
        # chunk function 실행

    # close the temporary file created by `NamedTemporaryFile`
    temp_audio_file.close()



# Chunk audio file function

# def chunk():
#     pass





# Trascribe function

def transcribe(audio_file):
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")
    file_obj=BytesIO(audio_file.read())

    # If I don't set name, AttributeError: '_io.BytesIO' object has no attribute 'name' this error occurs
    file_obj.name = "audio_file.wav"
    transcript = openai.Audio.transcribe("whisper-1", file_obj)
    print(transcript['text'])




# # Translate function: 98개의 서로다른 언어를 영어로 번역가능

# def translate():
#     pass



if __name__=="__main__":
    main()