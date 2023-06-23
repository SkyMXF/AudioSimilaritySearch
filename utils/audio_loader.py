import soundfile as sf
import numpy as np
import moviepy.editor


class AudioData(object):

    def __init__(
        self,
        path: str,
        sample_rate: int,
        samples: np.ndarray,     # (n_samples, n_channels)
    ):
        self.path: str = path
        self.sample_rate: int = sample_rate
        self.samples: np.ndarray = samples

    @property
    def channels(self) -> int:
        return self.samples.shape[1]

    @property
    def duration(self) -> float:
        return self.samples.shape[0] / self.sample_rate


def soundfile_loader(path: str) -> AudioData:
    samples, sample_rate = sf.read(path, always_2d=True)
    return AudioData(path=path, sample_rate=sample_rate, samples=samples)


def moviepy_loader(path: str) -> AudioData:
    video_clip = moviepy.editor.VideoFileClip(path)
    samples = video_clip.audio.to_soundarray()
    if len(samples.shape) < 2:
        samples = samples[:, np.newaxis]
    return AudioData(
        path=path,
        sample_rate=video_clip.audio.fps,
        samples=samples
    )
