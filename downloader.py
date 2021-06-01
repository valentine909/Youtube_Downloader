from pytube import YouTube


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    print(f"Downloaded {bytes_downloaded/1024/1024:.2f}Mb out of {total_size/1024/1024:.2f}Mb")


# video_url = input("Enter Youtube Video URL: ")
video_url = "https://www.youtube.com/watch?v=vvpb8IdDZZI"
youtube_obj = YouTube(video_url)
youtube_obj.register_on_progress_callback(on_progress)
youtube_obj.streams.filter(res='720p').first().download()
