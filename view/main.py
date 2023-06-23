import os
import glob
import numpy as np
from typing import Optional, Callable

from PySide6.QtWidgets import QMainWindow, QFileDialog
from PySide6.QtGui import QDesktopServices, QTextCursor
from PySide6.QtCore import QUrl, Qt

from .ui.main_window import Ui_MainWindow
from .utils.async_task import AsyncTaskThread
from utils.audio_loader import AudioData, soundfile_loader, moviepy_loader
from utils.fingerprint import WavFingerprint


# Loader for different ext
LOADER_DICT: dict[str, Callable[[str], AudioData]] = {
    ".wav": soundfile_loader,
    ".mp3": soundfile_loader,
    ".mov": moviepy_loader,
    ".mp4": moviepy_loader,
    ".avi": moviepy_loader,
    ".flv": moviepy_loader,
    ".mkv": moviepy_loader,
}

# Output path
OUTPUT_PATH = os.path.abspath("./result")


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, stylesheet = None):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        self.stylesheet = stylesheet

        # input file info
        self.input_file_path = None     # clear input path
        self.input_file_available = False
        self.input_file_data: Optional[AudioData] = None
        self.input_fingerprints: list[WavFingerprint] = []
        self.pushButtonBrowseInput.clicked.connect(self.on_click_browse_input)

        # search dir info
        self.searching_path = None      # clear searching path
        self.searching_path_available = False
        self.pushButtonBrowseSearching.clicked.connect(self.on_click_browse_searching)
        self.searching_path_file_result: dict[str, int] = {}

        # run searching panel
        self.on_update_progress(0.0)
        self.pushButtonRun.clicked.connect(self.on_click_run_searching)

        # output file info
        self.output_file_path = os.path.abspath(OUTPUT_PATH)
        self.on_output_path_updated()
        self.pushButtonOpenOutput.clicked.connect(self.on_click_open_output_folder)

    def set_component_color(self, component, style):
        component.setProperty("class", style)
        if self.stylesheet is not None:
            component.setStyleSheet(self.stylesheet)

    # get input file path from lineEditInputFile
    @property
    def input_file_path(self) -> Optional[str]:
        path = self.lineEditInputFile.text()
        if len(path) == 0:
            return None
        if not os.path.exists(path):
            return None
        return path

    # set input file path
    @input_file_path.setter
    def input_file_path(self, path: str):
        # set color disable
        self.set_component_color(self.lineEditInputFile, "warning")
        self.set_component_color(self.pushButtonBrowseInput, "warning")
        self.input_file_available = False

        if path is None:
            return
        if not os.path.exists(path):
            return
        if not os.path.isfile(path):
            return
        self.lineEditInputFile.setText(os.path.abspath(path))
        self.input_file_available = True
        self.set_component_color(self.lineEditInputFile, "success")
        self.set_component_color(self.pushButtonBrowseInput, "success")

        # show abstract audio data
        audio_data = LOADER_DICT[os.path.splitext(path)[1].lower()](path)
        self.lineEditInputChannel.setText(str(audio_data.channels))
        self.lineEditInputSampleRate.setText(str(audio_data.sample_rate))
        self.lineEditInputDuration.setText("%.3f" % audio_data.duration)
        self.input_file_data = audio_data

    # pushButtonBrowseInput clicked
    def on_click_browse_input(self):
        # open a file dialog with ext of ".wav", ".mp3"
        default_path = self.input_file_path
        if default_path is None:
            default_path = os.path.abspath(".")     # current dir
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select the input file", default_path,
            "Audio Files (%s)" % " ".join(["*" + ext for ext in LOADER_DICT.keys()]),
        )
        self.input_file_path = file_path

    # get searching path from lineEditSearchingPath
    @property
    def searching_path(self) -> Optional[str]:
        path = self.lineEditSearchingPath.text()
        if len(path) == 0:
            return None
        if not os.path.exists(path):
            return None
        return path

    # set searching path
    @searching_path.setter
    def searching_path(self, path: str):
        # set color disable
        self.set_component_color(self.lineEditSearchingPath, "warning")
        self.set_component_color(self.pushButtonBrowseSearching, "warning")
        self.searching_path_available = False

        if path is None:
            return
        if not os.path.exists(path):
            return
        if not os.path.isdir(path):
            return
        self.lineEditSearchingPath.setText(os.path.abspath(path))
        self.set_component_color(self.lineEditSearchingPath, "success")
        self.set_component_color(self.pushButtonBrowseSearching, "success")
        self.searching_path_available = True

        # show abstract dir info
        self.searching_path_file_result = {
            path: 0
            for path in list(glob.glob(os.path.join(path, "**", "*.wav"), recursive=True))
        }
        self.lineEditSearchWavNum.setText(str(len(self.searching_path_file_result)))

    # pushButtonBrowseSearching clicked
    def on_click_browse_searching(self):
        default_path = self.searching_path
        if default_path is None:
            default_path = os.path.abspath(".")     # current dir
        file_path = QFileDialog.getExistingDirectory(
            self, "Select the searching path", default_path,
        )
        self.searching_path = file_path

    # update progress bar, progress: 0.0 ~ 1.0
    def on_update_progress(self, progress: float):
        self.progressBar.setValue(int(progress * 100))

    # pushButtonRun clicked
    def on_click_run_searching(self):
        if not (self.input_file_available and self.searching_path_available):
            print("[ERROR]Input File or Searching Path not available.")
            return

        # prepare gui
        self.on_update_progress(0.0)
        self.setEnabled(False)
        print("Parsing input file...")

        # generate input fingerprints
        self.input_fingerprints = []
        for q_chn_idx in range(self.input_file_data.channels):
            samples = self.input_file_data.samples[:, q_chn_idx]
            ori_sample_rate = self.input_file_data.sample_rate
            samples = WavFingerprint.trim_silence(samples)
            samples = WavFingerprint.resample(samples, ori_sample_rate, WavFingerprint.DEFAULT_SAMPLE_RATE)
            self.input_fingerprints.append(WavFingerprint(samples, WavFingerprint.DEFAULT_SAMPLE_RATE))

        # start search thread
        print("Start searching...")
        search_thread = AsyncTaskThread(
            task_worker=self.generate_search_task(),
            task_args=[],
            task_length=len(self.searching_path_file_result),
            on_progress=self.on_update_progress,
            on_task_result=self.on_file_matched,
            on_finish=self.on_search_thread_finished,
            parent=self
        )
        search_thread.start()

    # generate a task closure
    def generate_search_task(self):

        def search_task() -> tuple[int, str, int]:
            for wav_idx, key_wav_path in enumerate(self.searching_path_file_result.keys()):
                key_fingerprint = WavFingerprint.load_file(
                    path=key_wav_path,
                    resample_rate=WavFingerprint.DEFAULT_SAMPLE_RATE,
                    selected_channels=[0],
                )[0]
                scores = np.array([
                    WavFingerprint.match(q_chn_fingerprint, key_fingerprint)
                    for q_chn_fingerprint in self.input_fingerprints
                ])
                yield wav_idx, key_wav_path, np.max(scores)

        return search_task

    # match with one file in search thread
    def on_file_matched(self, match_info: tuple[int, str, int]):
        file_idx = match_info[0]
        file_path = match_info[1]
        match_score = match_info[2]
        print("\r[%d/%d]%s" % (
            file_idx + 1, len(self.searching_path_file_result), os.path.basename(file_path)
        ), end="")
        self.searching_path_file_result[file_path] = match_score

    # search thread finished
    def on_search_thread_finished(self):

        # output result
        print()
        print("Search finished.")
        result_output_path = os.path.join(
            OUTPUT_PATH,
            os.path.splitext(os.path.basename(self.input_file_path))[0] + ".csv"
        )
        result_list = [(path, score) for path, score in self.searching_path_file_result.items()]
        result_list.sort(key=lambda r: r[1], reverse=True)
        with open(result_output_path, "w") as f:
            print("Path,Score", file=f)
            for path, score in result_list:
                print("%s,%d" % (path, score), file=f)
            print("Result saved to '%s'." % result_output_path)
        if len(result_list) > 0:
            print("Top5 Matched Audio:")
            for result_idx in range(min(len(result_list), 5)):
                path, score = result_list[result_idx]
                print("Score: %d, Path: %s" % (score, path))

        # restore gui
        self.on_update_progress(1.0)
        self.setEnabled(True)

    # update lineEditOutputFolder
    def on_output_path_updated(self):
        self.lineEditOutputFolder.setText(self.output_file_path)
        if not os.path.exists(self.output_file_path):
            os.makedirs(self.output_file_path)

    # pushButtonOpenOutput clicked
    def on_click_open_output_folder(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile(self.output_file_path))
