from dataclasses import dataclass
from typing import Any
from typing import Optional

from sonusai.mixture import AudioT


@dataclass(frozen=True)
class ASRResult:
    text: str
    confidence: Optional[float] = None
    lang: Optional[str] = None
    lang_prob: Optional[float] = None
    duration: Optional[float] = None
    num_segments: Optional[int] = None
    asr_cpu_time: Optional[float] = None


def calc_asr(audio: AudioT | str,
             engine: Optional[str] = 'deepgram',
             whisper_model: Optional[Any] = None,
             whisper_model_name: Optional[str] = 'tiny',
             device: Optional[str] = 'cpu',
             cpu_threads: Optional[int] = 1,
             compute_type: Optional[str] = 'int8',
             beam_size: Optional[int] = 5) -> ASRResult:
    """Run ASR on audio

    :param audio: Numpy array of audio samples or location of an audio file
    :param engine: Type of ASR engine to use
    :param whisper_model: A preloaded Whisper ASR model
    :param whisper_model_name: Name of Whisper ASR model to use if none was provided
    :param device: the device to put the ASR model into
    :param cpu_threads: int specifying threads to use when device is cpu
           note: must be 1 if this func is run in parallel
    :param compute_type: the precision of ASR model to use
    :param beam_size: int specifying beam_size to use
    :return: ASRResult object containing text and confidence
    """
    from copy import copy

    import numpy as np

    from sonusai import SonusAIError
    from sonusai.mixture import read_audio
    from sonusai.utils import asr_functions
    from sonusai.utils.asr_functions.data import Data

    if not isinstance(audio, np.ndarray):
        audio = copy(read_audio(audio))

    data = Data(audio, whisper_model, whisper_model_name, device, cpu_threads, compute_type, beam_size)

    try:
        return getattr(asr_functions, engine)(data)
    except AttributeError:
        raise SonusAIError(f'Unsupported ASR function: {engine}')
