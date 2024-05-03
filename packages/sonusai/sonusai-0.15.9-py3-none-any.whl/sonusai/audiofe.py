"""sonusai audiofe

usage: audiofe [-hvds] [--version] [-i INPUT] [-l LENGTH] [-m MODEL] [-k CKPT] [-a ASR] [-w WMODEL]

options:
    -h, --help
    -v, --verbose                   Be verbose.
    -d, --debug                     Write debug data to H5 file.
    -s, --show                      Show a list of available audio inputs.
    -i INPUT, --input INPUT         Input audio.
    -l LENGTH, --length LENGTH      Length of audio in seconds. [default: -1].
    -m MODEL, --model MODEL         PL model .py file path.
    -k CKPT, --checkpoint CKPT      PL checkpoint file with weights.
    -a ASR, --asr ASR               ASR method to use.
    -w WMODEL, --whisper WMODEL     Whisper model used in aixplain_whisper and whisper methods. [default: tiny].

Aaware SonusAI Audio Front End.

Capture LENGTH seconds of audio from INPUT. If LENGTH is < 0, then capture until key is pressed. If INPUT is a valid
audio file name, then use the audio data from the specified file. In this case, if LENGTH is < 0, process entire file;
otherwise, process min(length(INPUT), LENGTH) seconds of audio from INPUT. Audio is saved to
audiofe_capture_<TIMESTAMP>.wav.

If a model is specified, run prediction on audio data from this model. Then compute the inverse transform of the
prediction result and save to audiofe_predict_<TIMESTAMP>.wav.

If an ASR is specified, run ASR on the captured audio and print the results. In addition, if a model was also specified,
run ASR on the predict audio and print the results.

If the debug option is enabled, write capture audio, feature, reconstruct audio, predict, and predict audio to
audiofe_<TIMESTAMP>.h5.

"""
from os.path import exists
from select import select
from sys import stdin
from typing import Any

import h5py
import numpy as np
import pyaudio
import torch
from docopt import docopt
from docopt import printable_usage

import sonusai
from sonusai import create_file_handler
from sonusai import initial_log_messages
from sonusai import logger
from sonusai import update_console_handler
from sonusai.mixture import AudioT
from sonusai.mixture import CHANNEL_COUNT
from sonusai.mixture import SAMPLE_RATE
from sonusai.mixture import get_audio_from_feature
from sonusai.mixture import get_feature_from_audio
from sonusai.mixture import read_audio
from sonusai.utils import calc_asr
from sonusai.utils import create_timestamp
from sonusai.utils import get_input_device_index_by_name
from sonusai.utils import get_input_devices
from sonusai.utils import import_keras_model
from sonusai.utils import trim_docstring
from sonusai.utils import write_wav


def main() -> None:
    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)
    ts = create_timestamp()

    verbose = args['--verbose']
    length = float(args['--length'])
    input_name = args['--input']
    model_name = args['--model']
    ckpt_name = args['--checkpoint']
    asr_name = args['--asr']
    whisper_name = args['--whisper']
    debug = args['--debug']
    show = args['--show']

    capture_name = f'audiofe_capture_{ts}.wav'
    predict_name = f'audiofe_predict_{ts}.wav'
    h5_name = f'audiofe_{ts}.h5'

    if model_name is not None and ckpt_name is None:
        print(printable_usage(trim_docstring(__doc__)))
        exit(1)

    # Setup logging file
    create_file_handler('audiofe.log')
    update_console_handler(verbose)
    initial_log_messages('audiofe')

    if show:
        logger.info('List of available audio inputs:')
        logger.info('')
        p = pyaudio.PyAudio()
        for name in get_input_devices(p):
            logger.info(f'{name}')
        logger.info('')
        p.terminate()
        return

    if input_name is not None and exists(input_name):
        capture_audio = get_frames_from_file(input_name, length)
    else:
        try:
            capture_audio = get_frames_from_device(input_name, length)
        except ValueError as e:
            logger.exception(e)
            return

    write_wav(capture_name, capture_audio, SAMPLE_RATE)
    logger.info('')
    logger.info(f'Wrote capture audio with shape {capture_audio.shape} to {capture_name}')
    if debug:
        with h5py.File(h5_name, 'a') as f:
            if 'capture_audio' in f:
                del f['capture_audio']
            f.create_dataset('capture_audio', data=capture_audio)
        logger.info(f'Wrote capture audio with shape {capture_audio.shape} to {h5_name}')

    if asr_name is not None:
        capture_asr = calc_asr(capture_audio, engine=asr_name, whisper_model_name=whisper_name).text
        logger.info(f'Capture audio ASR: {capture_asr}')

    if model_name is not None:
        model = load_model(model_name=model_name, ckpt_name=ckpt_name)

        feature = get_feature_from_audio(audio=capture_audio, feature_mode=model.hparams.feature)
        if debug:
            with h5py.File(h5_name, 'a') as f:
                if 'feature' in f:
                    del f['feature']
                f.create_dataset('feature', data=feature)
            logger.info(f'Wrote feature with shape {feature.shape} to {h5_name}')

        # if debug:
        #     reconstruct_name = f'audiofe_reconstruct_{ts}.wav'
        #     reconstruct_audio = get_audio_from_feature(feature=feature, feature_mode=model.hparams.feature)
        #     samples = min(len(capture_audio), len(reconstruct_audio))
        #     max_err = np.max(np.abs(capture_audio[:samples] - reconstruct_audio[:samples]))
        #     logger.info(f'Maximum error between capture and reconstruct: {max_err}')
        #     write_wav(reconstruct_name, reconstruct_audio, SAMPLE_RATE)
        #     logger.info(f'Wrote reconstruct audio with shape {reconstruct_audio.shape} to {reconstruct_name}')
        #     with h5py.File(h5_name, 'a') as f:
        #         if 'reconstruct_audio' in f:
        #             del f['reconstruct_audio']
        #         f.create_dataset('reconstruct_audio', data=reconstruct_audio)
        #     logger.info(f'Wrote reconstruct audio with shape {reconstruct_audio.shape} to {h5_name}')

        with torch.no_grad():
            predict = model(torch.tensor(feature))
        if debug:
            with h5py.File(h5_name, 'a') as f:
                if 'predict' in f:
                    del f['predict']
                f.create_dataset('predict', data=predict)
            logger.info(f'Wrote predict with shape {predict.shape} to {h5_name}')

        predict_audio = get_audio_from_feature(feature=predict.numpy(), feature_mode=model.hparams.feature)
        write_wav(predict_name, predict_audio, SAMPLE_RATE)
        logger.info(f'Wrote predict audio with shape {predict_audio.shape} to {predict_name}')
        if debug:
            with h5py.File(h5_name, 'a') as f:
                if 'predict_audio' in f:
                    del f['predict_audio']
                f.create_dataset('predict_audio', data=predict_audio)
            logger.info(f'Wrote predict audio with shape {predict_audio.shape} to {h5_name}')

        if asr_name is not None:
            predict_asr = calc_asr(predict_audio, engine=asr_name, whisper_model_name=whisper_name).text
            logger.info(f'Predict audio ASR: {predict_asr}')


def load_model(model_name: str, ckpt_name: str) -> Any:
    batch_size = 1
    timesteps = 0

    # Load checkpoint first to get hparams if available
    try:
        checkpoint = torch.load(ckpt_name, map_location=lambda storage, loc: storage)
    except Exception as e:
        logger.exception(f'Error: could not load checkpoint from {ckpt_name}: {e}')
        raise SystemExit(1)

    # Import model definition file
    logger.info(f'Importing {model_name}')
    litemodule = import_keras_model(model_name)

    if 'hyper_parameters' in checkpoint:
        logger.info(f'Found checkpoint file with hyper-parameters')
        hparams = checkpoint['hyper_parameters']
        if hparams['batch_size'] != batch_size:
            logger.info(
                f'Overriding model default batch_size of {hparams["batch_size"]} with batch_size of {batch_size}')
            hparams["batch_size"] = batch_size

        if hparams['timesteps'] != 0 and timesteps == 0:
            timesteps = hparams['timesteps']
            logger.warning(f'Using model default timesteps of {timesteps}')

        logger.info(f'Building model with {len(hparams)} total hparams')
        try:
            model = litemodule.MyHyperModel(**hparams)
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_name} failed: {e}')
            raise SystemExit(1)
    else:
        logger.info(f'Found checkpoint file with no hyper-parameters')
        logger.info(f'Building model with defaults')
        try:
            tmp = litemodule.MyHyperModel()
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_name} failed: {e}')
            raise SystemExit(1)

        if tmp.batch_size != batch_size:
            logger.info(f'Overriding model default batch_size of {tmp.batch_size} with batch_size of {batch_size}')

        if tmp.timesteps != 0 and timesteps == 0:
            timesteps = tmp.timesteps
            logger.warning(f'Using model default timesteps of {timesteps}')

        model = litemodule.MyHyperModel(timesteps=timesteps, batch_size=batch_size)

    logger.info(f'Loading weights from {ckpt_name}')
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    return model


def get_frames_from_device(input_name: str | None, length: float, chunk: int = 1024) -> AudioT:
    p = pyaudio.PyAudio()

    input_devices = get_input_devices(p)
    if not input_devices:
        raise ValueError('No input audio devices found')

    if input_name is None:
        input_name = input_devices[0]

    try:
        device_index = get_input_device_index_by_name(p, input_name)
    except ValueError:
        msg = f'Could not find {input_name}\n'
        msg += f'Available devices:\n'
        for input_device in input_devices:
            msg += f'  {input_device}\n'
        raise ValueError(msg)

    logger.info(f'Capturing from {p.get_device_info_by_index(device_index).get("name")}')
    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNEL_COUNT,
                    rate=SAMPLE_RATE,
                    input=True,
                    input_device_index=device_index)
    stream.start_stream()

    print()
    print('+---------------------------------+')
    print('| Press Enter to stop             |')
    print('+---------------------------------+')
    print()

    elapsed = 0.0
    seconds_per_chunk = float(chunk) / float(SAMPLE_RATE)
    raw_frames = []
    while elapsed < length or length == -1:
        raw_frames.append(stream.read(num_frames=chunk, exception_on_overflow=False))
        elapsed += seconds_per_chunk
        if select([stdin, ], [], [], 0)[0]:
            stdin.read(1)
            length = elapsed

    stream.stop_stream()
    stream.close()
    p.terminate()
    frames = np.frombuffer(b''.join(raw_frames), dtype=np.float32)
    return frames


def get_frames_from_file(input_name: str, length: float) -> AudioT:
    logger.info(f'Capturing from {input_name}')
    frames = read_audio(input_name)
    if length != -1:
        num_frames = int(length * SAMPLE_RATE)
        if len(frames) > num_frames:
            frames = frames[:num_frames]
    return frames


if __name__ == '__main__':
    main()
