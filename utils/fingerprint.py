import os
import glob
import math
import librosa
import librosa.effects
import soundfile as sf
import numpy as np
from typing import Optional


class WavFingerprint(object):

    FREQ_BASES = 220        # A3
    OCTAVE_NUM = 12          # A3 ~ A8
    OCTAVE_RATIO = math.sqrt(2)
    DEFAULT_SAMPLE_RATE = 44100
    WINDOW_TIME = 0.02      # seconds
    MATCH_WINDOW_NUM = 3    # match window size
    FFT_WINDOW = 1024       # FFT window size

    def __init__(self, samples: np.ndarray, sample_rate: int):
        # args
        self.samples: np.ndarray = samples     # 1d array
        self.sample_rate: int = sample_rate    # Hz
        self.n_window = int(np.ceil(self.samples.shape[0] / (WavFingerprint.WINDOW_TIME * self.sample_rate)))
        self.n_samples_per_window: int = int(WavFingerprint.WINDOW_TIME * self.sample_rate)
        self.freq_scaling = self.n_samples_per_window / self.sample_rate
        self.fingerprint = self._generate_fingerprint()

    @staticmethod
    def load_file(
        path: str,
        resample_rate: Optional[int] = None,
        force_to_mono: bool = False,
        selected_channels: list[int] = None,
    ) -> list["WavFingerprint"]:
        samples, sample_rate = sf.read(path, always_2d=True)
        if force_to_mono:
            samples = samples.mean(axis=1, keepdims=True)
        if selected_channels is None:
            selected_channels = list(range(samples.shape[1]))

        channel_fingerprints: list["WavFingerprint"] = []
        for chn_idx in range(samples.shape[1]):
            if chn_idx not in selected_channels:
                continue
            chn_samples = samples[:, chn_idx]
            chn_samples = WavFingerprint.trim_silence(chn_samples)
            if resample_rate is not None and resample_rate != sample_rate:
                chn_samples = WavFingerprint.resample(chn_samples, sample_rate, resample_rate)
                sample_rate = resample_rate
            channel_fingerprints.append(WavFingerprint(samples=chn_samples, sample_rate=sample_rate))

        return channel_fingerprints

    # trim silence at head and tail on 1d array
    @staticmethod
    def trim_silence(samples: np.ndarray) -> np.ndarray:
        return librosa.effects.trim(samples, top_db=120, frame_length=1024, hop_length=256)[0]

    # resample to given rate on 1d array
    @staticmethod
    def resample(samples: np.ndarray, ori_sr: int, tgt_sr: int) -> np.ndarray:
        return librosa.resample(samples, ori_sr, tgt_sr)

    # generate fingerprint of given samples sequence
    # -> shape=(n_windows - 2, octave_num, octave_num, 3)
    def _generate_fingerprint(self) -> np.ndarray:

        # pad to make sure the last window has enough samples
        samples = self.samples
        samples = np.pad(samples, (0, self.n_window * self.n_samples_per_window - self.samples.shape[0]))

        # (n_samples,) -> (n_windows, n_samples_per_window)
        samples = samples.reshape(self.n_window, self.n_samples_per_window)

        # pad to FFT_WINDOW size
        samples = np.pad(samples, ((0, 0), (0, WavFingerprint.FFT_WINDOW - self.n_samples_per_window)))

        # FFT on each window
        spectrum = np.abs(np.fft.fft(samples, axis=1))

        # get feature
        feature = []
        for octave_idx in range(WavFingerprint.OCTAVE_NUM):
            # above freqs are scaled value
            min_freq_idx = (
                WavFingerprint.FREQ_BASES * (WavFingerprint.OCTAVE_RATIO ** octave_idx)
            ) * self.freq_scaling
            max_freq_idx = (
                WavFingerprint.FREQ_BASES * (WavFingerprint.OCTAVE_RATIO ** (octave_idx + 1))
            ) * self.freq_scaling
            strong_freq = np.argmax(        # shape=(n_windows,)
                spectrum[:, int(min_freq_idx):int(max_freq_idx)], axis=1
            ) + min_freq_idx
            feature.append(np.log2(strong_freq / min_freq_idx))
        feature = np.stack(feature, axis=1)     # shape=(n_windows, octave_num)

        # n_windows should be >= WavFingerprint.MATCH_WINDOW_NUM
        match_window_num = WavFingerprint.MATCH_WINDOW_NUM
        if feature.shape[0] < match_window_num:
            feature = np.pad(feature, ((0, match_window_num - feature.shape[0]), (0, 0)))

        # feature to fingerprint, shape=(n_windows - 2, octave_num, octave_num, 3)
        delta_t_features = [feature[:-(match_window_num - 1), :]]
        for delta_t in range(1, match_window_num):
            end_idx = - match_window_num + delta_t + 1
            if end_idx == 0:
                delta_t_features.append(feature[delta_t:, :])
            else:
                # end_idx < 0
                delta_t_features.append(feature[delta_t:end_idx, :])
        fingerprint = np.stack(
            [np.tile(delta_t_features[0][:, :, np.newaxis], (1, 1, WavFingerprint.OCTAVE_NUM))] + [
                np.tile(f[:, np.newaxis, :], (1, WavFingerprint.OCTAVE_NUM, 1))
                for f in delta_t_features[1:]
            ], axis=3
        )

        return fingerprint

    @staticmethod
    def match(wav_a: "WavFingerprint", wav_b: "WavFingerprint") -> np.ndarray:
        # let wav_a.n_window <= wav_b.n_window
        if wav_a.n_window > wav_b.n_window:
            wav_a, wav_b = wav_b, wav_a

        fingerprint_a = wav_a.fingerprint
        fingerprint_b = wav_b.fingerprint

        # pad fingerprint b with len(a) // 2 before convolution
        pad_len = fingerprint_a.shape[0] // 2
        fingerprint_b = np.pad(
            fingerprint_b,
            ((pad_len, pad_len), (0, 0), (0, 0), (0, 0)),
        )

        # convolution, but calculate cos similarity instead of product
        conv_len = fingerprint_b.shape[0] - fingerprint_a.shape[0] + 1
        similarity_array = np.zeros((conv_len,))
        for pos_idx in range(conv_len):
            distance = np.linalg.norm(fingerprint_a - fingerprint_b[pos_idx:pos_idx + fingerprint_a.shape[0]], axis=3)
            similarity_array[pos_idx] = np.sum(np.array(distance < 1e-6, dtype=np.int32))

        return similarity_array

    @staticmethod
    def _cos_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


if __name__ == '__main__':

    # record_path = os.path.join("test_wav", "raw_SFX_UI_GiveLike.wav")
    # record_path = os.path.join("test_wav", "RecordClipLike.wav")
    # record_path = os.path.join("test_wav", "RecordClipGun.wav")
    # record_path = os.path.join("test_wav", "RecordClipGun2.wav")
    record_path = os.path.join("test_wav", "RecordClipKill.wav")
    # record_path = os.path.join("test_wav", "RecordClipAce.wav")
    # record_path = os.path.join("test_wav", "raw_VO_en_Ace.wav")
    query_fingerprints = WavFingerprint.load_file(record_path, resample_rate=WavFingerprint.DEFAULT_SAMPLE_RATE)

    wav_repo = os.path.join("test_wav", "repo")
    key_wav_path_list = list(glob.glob(os.path.join(wav_repo, "**", "*.wav"), recursive=True))
    similarity_list = []
    for key_idx, key_wav_path in enumerate(key_wav_path_list):
        print("[%d/%d]Matching %s" % (key_idx + 1, len(key_wav_path_list), key_wav_path))
        key_fingerprints = WavFingerprint.load_file(key_wav_path, resample_rate=WavFingerprint.DEFAULT_SAMPLE_RATE)
        scores = np.array([
            WavFingerprint.match(q_chn_fingerprint, key_fingerprints[0])
            for q_chn_fingerprint in query_fingerprints
        ])
        similarity_list.append((key_wav_path, np.max(scores)))

    similarity_list.sort(key=lambda x: x[1])
    for key_wav_path, key_simi in similarity_list:
        print("%s:%.4f" % (key_wav_path, key_simi))

    print("end")
