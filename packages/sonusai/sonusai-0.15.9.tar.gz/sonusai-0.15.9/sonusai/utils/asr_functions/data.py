from dataclasses import dataclass
from typing import Any
from typing import Optional

from sonusai.mixture.datatypes import AudioT


@dataclass(frozen=True)
class Data:
    audio: AudioT
    whisper_model: Optional[Any] = None
    whisper_model_name: Optional[str] = None
    device: Optional[str] = None
    cpu_threads: Optional[int] = None
    compute_type: Optional[str] = None
    beam_size: Optional[int] = None
