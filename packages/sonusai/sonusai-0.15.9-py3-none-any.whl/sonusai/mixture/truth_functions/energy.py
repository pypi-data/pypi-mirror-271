from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.data import Data


def _core(data: Data, mapped: bool, snr: bool) -> Truth:
    import numpy as np

    from sonusai import SonusAIError
    from sonusai.mixture import calculate_mapped_snr_f
    from sonusai.utils import compute_energy_f

    snr_db_mean = None
    snr_db_std = None
    if mapped:
        if data.config.config is None:
            raise SonusAIError('Truth function mapped SNR missing config')

        parameters = ['snr_db_mean', 'snr_db_std']
        for parameter in parameters:
            if parameter not in data.config.config:
                raise SonusAIError(f'Truth function mapped_snr_f config missing required parameter: {parameter}')

        snr_db_mean = data.config.config['snr_db_mean']
        if len(snr_db_mean) != data.target_fft.bins:
            raise SonusAIError(f'Truth function mapped_snr_f snr_db_mean does not have {data.target_fft.bins} elements')

        snr_db_std = data.config.config['snr_db_std']
        if len(snr_db_std) != data.target_fft.bins:
            raise SonusAIError(f'Truth function mapped_snr_f snr_db_std does not have {data.target_fft.bins} elements')

    for index in data.zero_based_indices:
        if index + data.target_fft.bins > data.config.num_classes:
            raise SonusAIError('Truth index exceeds the number of classes')

    target_energy = compute_energy_f(time_domain=data.target_audio, transform=data.target_fft)
    noise_energy = None
    if snr:
        noise_energy = compute_energy_f(time_domain=data.noise_audio, transform=data.noise_fft)

    if len(target_energy) != len(data.offsets):
        raise SonusAIError(f'Number of frames in target_energy, {len(target_energy)},'
                           f' is not number of frames in truth, {len(data.offsets)}')

    for idx, offset in enumerate(data.offsets):
        tmp = target_energy[idx]

        if snr:
            old_err = np.seterr(divide='ignore', invalid='ignore')
            tmp /= noise_energy[idx]
            np.seterr(**old_err)

        tmp = np.nan_to_num(tmp, nan=-np.inf, posinf=np.inf, neginf=-np.inf)

        if mapped:
            tmp = calculate_mapped_snr_f(tmp, snr_db_mean, snr_db_std)

        for index in data.zero_based_indices:
            data.truth[offset:offset + data.frame_size, index:index + data.target_fft.bins] = tmp

    return data.truth


def energy_f(data: Data) -> Truth:
    """Frequency domain energy truth generation function

Calculates the true energy per bin:

Ti^2 + Tr^2

where T is the target STFT bin values.

Output shape: [:, bins]
    """
    return _core(data=data, mapped=False, snr=False)


def snr_f(data: Data) -> Truth:
    """Frequency domain SNR truth function documentation

Calculates the true SNR per bin:

(Ti^2 + Tr^2) / (Ni^2 + Nr^2)

where T is the target and N is the noise STFT bin values.

Output shape: [:, bins]
    """
    return _core(data=data, mapped=False, snr=True)


def mapped_snr_f(data: Data) -> Truth:
    """Frequency domain mapped SNR truth function documentation

Output shape: [:, bins]
    """
    return _core(data=data, mapped=True, snr=True)


def energy_t(data: Data) -> Truth:
    """Time domain energy truth function documentation

Calculates the true time domain energy of each frame:

For OLS:
    sum(x[0:N-1]^2) / N

For OLA:
    sum(x[0:R-1]^2) / R

where x is the target time domain data,
N is the size of the transform, and
R is the number of new samples in the frame.

Output shape: [:, 1]

Note: feature transforms can be defined to use a subset of all bins,
i.e., subset of 0:128 for N=256 could be 0:127 or 1:128. energy_t
will reflect the total energy over all bins regardless of the feature
transform config.
    """
    import numpy as np

    from sonusai import SonusAIError

    _, target_energy = data.target_fft.execute_all(data.target_audio)
    if len(target_energy) != len(data.offsets):
        raise SonusAIError(f'Number of frames in target_energy, {len(target_energy)},'
                           f' is not number of frames in truth, {len(data.offsets)}')

    for offset in data.offsets:
        data.truth[offset:offset + data.frame_size, data.zero_based_indices] = np.float32(target_energy)

    return data.truth
