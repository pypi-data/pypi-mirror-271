from typing import Optional

from sonusai.mixture.datatypes import AudioF
from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import Feature


def get_feature_from_audio(audio: AudioT,
                           feature_mode: str,
                           num_classes: Optional[int] = 1,
                           truth_mutex: Optional[bool] = False) -> Feature:
    """Apply forward transform and generate feature data from audio data

    :param audio: Time domain audio data [samples]
    :param feature_mode: Feature mode
    :param num_classes: Number of classes
    :param truth_mutex: Whether to calculate 'other' label
    :return: Feature data [frames, strides, feature_parameters]
    """
    import numpy as np
    from pyaaware import FeatureGenerator

    from .augmentation import pad_audio_to_frame
    from .datatypes import TransformConfig
    from .helpers import forward_transform

    fg = FeatureGenerator(feature_mode=feature_mode,
                          num_classes=num_classes,
                          truth_mutex=truth_mutex)

    feature_step_samples = fg.ftransform_R * fg.decimation * fg.step
    audio = pad_audio_to_frame(audio, feature_step_samples)

    audio_f = forward_transform(audio=audio,
                                config=TransformConfig(N=fg.ftransform_N,
                                                       R=fg.ftransform_R,
                                                       bin_start=fg.bin_start,
                                                       bin_end=fg.bin_end,
                                                       ttype=fg.ftransform_ttype))

    samples = len(audio)
    transform_frames = samples // fg.ftransform_R
    feature_frames = samples // feature_step_samples

    feature = np.empty((feature_frames, fg.stride, fg.feature_parameters), dtype=np.float32)

    feature_frame = 0
    for transform_frame in range(transform_frames):
        fg.execute(audio_f[transform_frame])

        if fg.eof():
            feature[feature_frame] = fg.feature()
            feature_frame += 1

    return feature


def get_audio_from_feature(feature: Feature,
                           feature_mode: str,
                           num_classes: Optional[int] = 1,
                           truth_mutex: Optional[bool] = False,
                           trim: Optional[bool] = True) -> AudioT:
    """Apply inverse transform to feature data to generate audio data

    :param feature: Feature data [frames, strides, feature_parameters]
    :param feature_mode: Feature mode
    :param num_classes: Number of classes
    :param truth_mutex: Whether to calculate 'other' label
    :param trim: Whether to trim the audio data
    :return: Audio data [samples]
    """
    import numpy as np

    from pyaaware import FeatureGenerator

    from .datatypes import TransformConfig
    from .helpers import inverse_transform
    from sonusai.utils.stacked_complex import unstack_complex

    fg = FeatureGenerator(feature_mode=feature_mode,
                          num_classes=num_classes,
                          truth_mutex=truth_mutex)

    feature_complex = unstack_complex(feature)
    if feature_mode[0:1] == 'h':
        feature_complex = _power_uncompress(feature_complex)
    return np.squeeze(inverse_transform(transform=feature_complex,
                                        config=TransformConfig(N=fg.itransform_N,
                                                               R=fg.itransform_R,
                                                               bin_start=fg.bin_start,
                                                               bin_end=fg.bin_end,
                                                               ttype=fg.itransform_ttype),
                                        trim=trim))


def _power_uncompress(feature: AudioF) -> AudioF:
    import numpy as np

    mag = np.abs(feature)
    phase = np.angle(feature)
    mag = mag ** (1. / 0.3)
    real_uncompress = mag * np.cos(phase)
    imag_uncompress = mag * np.sin(phase)

    return real_uncompress + 1j * imag_uncompress
