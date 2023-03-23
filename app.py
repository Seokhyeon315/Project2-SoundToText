import os
from pytube import YouTube

# Download youtube [str]: i.e. pixegami chatgpt tutorial

'''sample1: 'https://www.youtube.com/watch?v=KBo7mZHlink'
sample2: 'https://www.youtube.com/watch?v=E2NBQY-AWpk'
sample3: 'https://www.youtube.com/watch?v=0fYi8SGA20k'
'''

VIDEO_LINK='https://www.youtube.com/watch?v=0fYi8SGA20k'
yt=YouTube(VIDEO_LINK) # Assign YouTube object

# Extract sound from video and download it
audio_stream=yt.streams.filter(only_audio=True).first() #excludes streams with audio tracks


# Set ouput path
output_path=os.path.join(os.getcwd(), 'Audio folder')

#Create directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)


# Download audio stream to the output path
audio_stream.download(output_path=output_path, filename=f"{yt.title}.mp3") #유튜브 제목대로 음성파일 다운로드하게함.


# Convert length of video from seconds to hours, minutes, and seconds
length_seconds = yt.length
length_hours = length_seconds // 3600
length_minutes = (length_seconds % 3600) // 60
length_seconds = length_seconds % 60

# Print video title and length in hours, minutes, and seconds
print(f"The title: {yt.title}")
print(f"The length of the video: {length_hours} hrs {length_minutes} mins {length_seconds} secs")
