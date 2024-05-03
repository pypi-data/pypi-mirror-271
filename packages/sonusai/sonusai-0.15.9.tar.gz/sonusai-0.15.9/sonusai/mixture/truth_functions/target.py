from pyaaware import ForwardTransform

from sonusai.mixture.datatypes import AudioF
from sonusai.mixture.datatypes import AudioT
from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.data import Data


def target_f(data: Data) -> Truth:
    """Frequency domain target truth function

Calculates the true transform of the target using the STFT
configuration defined by the feature. This will include a
forward transform window if defined by the feature.

Output shape: [:, num_classes]
                    (target stacked real, imag; or real only for tdac-co)
    """

    from sonusai import SonusAIError

    if data.config.num_classes != data.feature_parameters:
        raise SonusAIError(f'Invalid num_classes for target_f truth: {data.config.num_classes}')

    target_freq = _execute_fft(data.target_audio, data.target_fft, len(data.offsets))
    for idx, offset in enumerate(data.offsets):
        data.truth = _stack_real_imag(data=target_freq[idx],
                                      offset=offset,
                                      frame_size=data.frame_size,
                                      zero_based_indices=data.zero_based_indices,
                                      bins=data.target_fft.bins,
                                      ttype=data.ttype,
                                      start=0,
                                      truth=data.truth)

    return data.truth


# TODO: Need Data to include mixture audio to do this correctly
def target_mixture_f(data: Data) -> Truth:
    """Frequency domain target and mixture truth function

Calculates the true transform of the target and the mixture
using the STFT configuration defined by the feature. This
will include a forward transform window if defined by the
feature.

Output shape: [:, 2 * num_classes]
                    (target stacked real, imag; or real only for tdac-co)
                    (mixture stacked real, imag; or real only for tdac-co)
    """
    from sonusai import SonusAIError

    if data.config.num_classes != 2 * data.feature_parameters:
        raise SonusAIError(f'Invalid num_classes for target_mixture_f truth: {data.config.num_classes}')

    target_freq = _execute_fft(data.target_audio, data.target_fft, len(data.offsets))
    mixture_freq = _execute_fft(data.mixture_audio, data.mixture_fft, len(data.offsets))

    for idx, offset in enumerate(data.offsets):
        data.truth = _stack_real_imag(data=target_freq[idx],
                                      offset=offset,
                                      frame_size=data.frame_size,
                                      zero_based_indices=data.zero_based_indices,
                                      bins=data.target_fft.bins,
                                      ttype=data.ttype,
                                      start=0,
                                      truth=data.truth)

        data.truth = _stack_real_imag(data=mixture_freq[idx],
                                      offset=offset,
                                      frame_size=data.frame_size,
                                      zero_based_indices=data.zero_based_indices,
                                      bins=data.target_fft.bins,
                                      ttype=data.ttype,
                                      start=data.target_fft.bins * 2,
                                      truth=data.truth)

    return data.truth


def target_swin_f(data: Data) -> Truth:
    """Frequency domain target with synthesis window truth function

Calculates the true transform of the target using the STFT
configuration defined by the feature. This will include a
forward transform window if defined by the feature and also
the inverse transform (or synthesis) window.

Output shape: [:, 2 * bins] (stacked real, imag)
    """
    import numpy as np

    from sonusai import SonusAIError

    if data.config.num_classes != 2 * data.target_fft.bins:
        raise SonusAIError(f'Invalid num_classes for target_swin_f truth: {data.config.num_classes}')

    for idx, offset in enumerate(data.offsets):
        target_freq, _ = data.target_fft.execute(
            np.multiply(data.target_audio[offset:offset + data.frame_size], data.swin))
        target_freq = target_freq.transpose()

        indices = slice(offset, offset + data.frame_size)
        for index in data.zero_based_indices:
            bins = _get_bin_slice(index, data.target_fft.bins)
            data.truth[indices, bins] = np.real(target_freq[idx])

            bins = _get_bin_slice(bins.stop, data.target_fft.bins)
            data.truth[indices, bins] = np.imag(target_freq[idx])

    return data.truth


def _execute_fft(audio: AudioT, transform: ForwardTransform, expected_frames: int) -> AudioF:
    from sonusai import SonusAIError

    freq, _ = transform.execute_all(audio)
    freq = freq.transpose()
    if len(freq) != expected_frames:
        raise SonusAIError(f'Number of frames, {len(freq)}, is not number of frames expected, {expected_frames}')
    return freq


def _get_bin_slice(start: int, length: int) -> slice:
    return slice(start, start + length)


def _stack_real_imag(data: AudioF,
                     offset: int,
                     frame_size: int,
                     zero_based_indices: list[int],
                     bins: int,
                     ttype: str,
                     start: int,
                     truth: Truth) -> Truth:
    import numpy as np

    i = _get_bin_slice(offset, frame_size)
    for index in zero_based_indices:
        b = _get_bin_slice(index + start, bins)
        truth[i, b] = np.real(data)

        if ttype != 'tdac-co':
            b = _get_bin_slice(b.stop, bins)
            truth[i, b] = np.imag(data)

    return truth
