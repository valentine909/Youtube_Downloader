from pytube import YouTube
import ffmpeg
from PyQt5 import QtWidgets, QtCore
import client_ui
import re


class YouTubeDownloaderApp(QtWidgets.QMainWindow, client_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.all_streams = None
        self.video_streams = None
        self.video_title = None
        self.translate = QtCore.QCoreApplication.translate
        self.listen()

    def listen(self):
        self.pushButton_get.pressed.connect(self.get_all_streams)
        self.pushButton_path.pressed.connect(self.select_folder)
        self.pushButton_apply.pressed.connect(self.apply_filters)
        self.pushButton_download.pressed.connect(self.download_selected_stream)

    def select_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory()
        self.lineEdit_path.setText(self.translate("MainWindow", path))
        self.lineEdit_path.setPlaceholderText(self.translate("MainWindow", path))
        self.statusBar.showMessage("New download folder selected.")

    def get_all_streams(self):
        try:
            url = self.textEdit_url.toPlainText()
            youtube_obj = YouTube(url)
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please, provide a valid url')
            self.statusBar.showMessage('Please, provide a valid url!')
            return
        self.video_title = youtube_obj.title
        self.lineEdit_video_title.setText(self.translate("MainWindow", self.video_title))
        self.all_streams = youtube_obj.streams
        self.video_streams = self.all_streams.filter(type='video', progressive=False)
        audio_streams = self.all_streams.filter(type='audio', progressive=False)
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
        self.statusBar.showMessage("Streams and filters loaded.")

    def apply_filters(self):
        resolution = self.comboBox_resolution.currentText()
        fps = int(self.comboBox_fps.currentText())
        mime_type = self.comboBox_mime_type.currentText()
        filtered_streams = self.video_streams.filter(resolution=resolution, fps=fps, mime_type=mime_type)
        self.comboBox_video.clear()
        self.comboBox_video.addItems([str(i) for i in filtered_streams])
        self.statusBar.showMessage("Filters applied.")

    def get_itag(self, stream_txt: str):
        result = re.search(r"[0-9]+", stream_txt)
        return self.all_streams.get_by_itag(int(result.group(0)))

    def download_selected_stream(self):
        stream_video_txt = self.comboBox_video.currentText()
        self.statusBar.showMessage("Downloading video stream...")
        self.get_itag(stream_video_txt).download(filename='video')
        stream_audio_txt = self.comboBox_audio.currentText()
        self.statusBar.showMessage("Downloading audio stream...")
        self.get_itag(stream_audio_txt).download(filename='audio')
        self.merge_streams_with_ffmpeg()

    def merge_streams_with_ffmpeg(self):
        video_stream = ffmpeg.input('video.mp4')
        audio_stream = ffmpeg.input('audio.mp4')
        self.statusBar.showMessage("Merging streams into output file...")
        ffmpeg.output(audio_stream, video_stream, f'{self.video_title}.mp4', vcodec='copy', acodec='aac').run()
        self.statusBar.showMessage("Done!.")


app = QtWidgets.QApplication([])
window = YouTubeDownloaderApp()
window.show()
app.exec()
