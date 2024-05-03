from sonusai.utils import ASRResult
from sonusai.utils.asr_functions.data import Data


def fastwhisper(data: Data) -> ASRResult:
    from os import getpid
    from timeit import default_timer as timer

    from faster_whisper import WhisperModel

    from sonusai import SonusAIError

    whisper_model = data.whisper_model
    pid = getpid()
    # print(f'{pid}: Loading model ...')
    retry = 2
    count = 0
    while True:
        try:
            # To pre-download model, first provide whisper_model_name without whisper_model (or =None)
            if whisper_model is None:
                model = WhisperModel(data.whisper_model_name,
                                     device=data.device,
                                     cpu_threads=data.cpu_threads,
                                     compute_type=data.compute_type)
            else:
                model = WhisperModel(whisper_model,
                                     device=data.device,
                                     cpu_threads=data.cpu_threads,
                                     compute_type=data.compute_type,
                                     local_files_only=True)

            # print(f'{pid}: Done Loading, now transcribing ...')
            s_time = timer()
            segments, info = model.transcribe(data.audio, beam_size=int(data.beam_size))
            segments = list(segments)  # The transcription will actually run here.
            e_time = timer()
            elapsed = e_time - s_time
            transcription = "".join(segment.text for segment in segments)
            # print(f'{pid}: Done transcribing.')
            tmp = ASRResult(text=transcription,
                            lang=info.language,
                            lang_prob=info.language_probability,
                            duration=info.duration,
                            num_segments=len(segments),
                            asr_cpu_time=elapsed
                            )
            return tmp
        except Exception as e:
            count += 1
            print(f'{pid}: Warning: fastwhisper exception: {e}')
            if count >= retry:
                raise SonusAIError(f'{pid}: Fastwhisper exception: {e.args}')


"""
Whisper results:
{
  'text': ' The birch canoe slid on the smooth planks.',
  'segments': [
    {
      'id': 0,
      'seek': 0,
      'start': 0.0,
      'end': 2.4,
      'text': ' The birch canoe slid on the smooth planks.',
      'tokens': [
        50363,
        383,
        35122,
        354,
        47434,
        27803,
        319,
        262,
        7209,
        1410,
        591,
        13,
        50483
      ],
      'temperature': 0.0,
      'avg_logprob': -0.4188103675842285,
      'compression_ratio': 0.8571428571428571,
      'no_speech_prob': 0.003438911633566022
    }
  ],
  'language': 'en'
}
"""
