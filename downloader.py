from pytube import YouTube
import ffmpeg


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    print(f"Downloaded {bytes_downloaded/1024/1024:.2f}Mb out of {total_size/1024/1024:.2f}Mb")


# video_url = input("Enter Youtube Video URL: ")
video_url = "https://www.youtube.com/watch?v=xET1aTbiHno"
youtube_obj = YouTube(video_url, on_progress_callback=on_progress)
# streams = list(youtube_obj.streams)
# print(*streams, sep='\n')
# streams = list(youtube_obj.streams.filter(mime_type="video/mp4"))
# print()
# print(*streams, sep='\n')
youtube_obj.streams.filter(file_extension='mp4', progressive=False).\
    order_by('resolution').desc().first().download(filename='video')
youtube_obj.streams.filter(mime_type="audio/mp4").first().download(filename='audio')
video_stream = ffmpeg.input('video.mp4')
audio_stream = ffmpeg.input('audio.mp4')
ffmpeg.output(audio_stream, video_stream, 'out1.mp4', vcodec='copy', acodec='aac').run()
