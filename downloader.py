from pytube import YouTube
import ffmpeg
from PyQt5 import QtWidgets, QtCore
import client_ui

# TODO Solve the problem of incorrect URL input: UI hanging, python - Qt interaction


class YouTubeDownloaderApp(QtWidgets.QMainWindow, client_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.video_streams = None
        self.listen()

    def listen(self):
        self.pushButton_go.pressed.connect(self.get_all_streams)
        self.pushButton_path.pressed.connect(self.select_folder)
        self.pushButton_apply.pressed.connect(self.apply_filters)
        self.pushButton_download.pressed.connect(self.download_selected_stream)

    def select_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory()
        _translate = QtCore.QCoreApplication.translate
        self.lineEdit_path.setText(_translate("MainWindow", path))
        self.lineEdit_path.setPlaceholderText(_translate("MainWindow", path))

    def get_all_streams(self):
        # is_not_url_provided = True
        # e = None
        # while is_not_url_provided:
        #     try:
        #         url = self.textEdit.toPlainText()
        #     except Exception as e:
        #         QtWidgets.QMessageBox.warning(self, 'Error', 'Please, provide a valid url')
        #         self.listen()
        #     else:
        #         if e is None:
        #             is_not_url_provided = False
        url = 'https://www.youtube.com/watch?v=g94j-ahVR78'
        youtube_obj = YouTube(url)
        self.video_streams = youtube_obj.streams.filter(type='video', progressive=False)
        audio_streams = youtube_obj.streams.filter(type='audio', progressive=False)
        self.comboBox_video.addItems([str(i) for i in self.video_streams])
        self.comboBox_audio.addItems([str(i) for i in audio_streams])
        self.process_filters()

    def process_filters(self):
        resolutions = sorted(list(set(str(i.resolution) for i in self.video_streams)))
        self.comboBox_resolution.addItems(resolutions)
        fpss = sorted(list(set(str(i.fps) for i in self.video_streams)))
        self.comboBox_fps.addItems(fpss)
        mime_types = sorted(list(set(str(i.mime_type) for i in self.video_streams)))
        self.comboBox_mime_type.addItems(mime_types)

    def apply_filters(self):
        resolution = self.comboBox_resolution.currentText()
        fps = int(self.comboBox_fps.currentText())
        mime_type = self.comboBox_mime_type.currentText()
        filtered_streams = self.video_streams.filter(resolution=resolution, fps=fps, mime_type=mime_type)
        self.comboBox_video.clear()
        self.comboBox_video.addItems([str(i) for i in filtered_streams])

    def download_selected_stream(self):
        ...
        # youtube_obj.streams.filter(file_extension='mp4', progressive=False). \
        #     order_by('resolution').desc().first().download(filename='video')
        # youtube_obj.streams.filter(mime_type="audio/mp4").first().download(filename='audio')
        # video_stream = ffmpeg.input('video.mp4')
        # audio_stream = ffmpeg.input('audio.mp4')
        # ffmpeg.output(audio_stream, video_stream, 'out1.mp4', vcodec='copy', acodec='aac').run()




# # video_url = input("Enter Youtube Video URL: ")
# video_url = "https://www.youtube.com/watch?v=xET1aTbiHno"
# youtube_obj = YouTube(video_url, on_progress_callback=on_progress)
# # streams = list(youtube_obj.streams)
# # print(*streams, sep='\n')
# # streams = list(youtube_obj.streams.filter(mime_type="video/mp4"))
# # print()
# # print(*streams, sep='\n')
# youtube_obj.streams.filter(file_extension='mp4', progressive=False).\
#     order_by('resolution').desc().first().download(filename='video')
# youtube_obj.streams.filter(mime_type="audio/mp4").first().download(filename='audio')
# video_stream = ffmpeg.input('video.mp4')
# audio_stream = ffmpeg.input('audio.mp4')
# ffmpeg.output(audio_stream, video_stream, 'out1.mp4', vcodec='copy', acodec='aac').run()


app = QtWidgets.QApplication([])
window = YouTubeDownloaderApp()
window.show()
app.exec()
