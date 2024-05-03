from sonusai.mixture import get_default_config


def doc_seed() -> str:
    default = f"\nDefault value: {get_default_config()['seed']}"
    return """
'seed' is a mixture database configuration parameter that sets the random number
generator seed.
""" + default


def doc_feature() -> str:
    default = f"\nDefault value: {get_default_config()['feature']}"
    return """
'feature' is a mixture database configuration parameter that sets the feature
to use.
""" + default


def doc_target_level_type() -> str:
    default = f"\nDefault value: {get_default_config()['target_level_type']}"
    return """
'target_level_type' is a mixture database configuration parameter that sets the
algorithm to use to determine target energy level for SNR calculations.
Supported values are:

 default    mean of squares
 speech     ITU-T P.56 active speech level method B
""" + default


def doc_targets() -> str:
    default = f"\nDefault value: {get_default_config()['targets']}"
    return """
'targets' is a mixture database configuration parameter that sets the list of
targets to use.

Required field:

 'name'
                File name. May be one of the following:

  audio         Supported formats are .wav, .mp3, .aif, .flac, and .ogg
  glob          Matches file glob patterns
  .yml          The given YAML file is parsed into the list
  .txt          Each line in the given text file indicates an item which
                may be anything in this list (audio, glob, .yml, or .txt)

Optional fields:

 'truth_settings'
                Local overrides for truth. Contains any or all of the
                following:

  'function'    Name of truth function <str>
  'config'      Truth function config <dict>
  'index'       Truth index <int> or list(<int>)

                'index' indicates which truth fields should be set.
                0 indicates none, 1 is first element in truth output
                vector, 2 2nd element, etc.

                Examples:
                  index = 5       truth in class 5, truth(4, 1)
                  index = [1, 5]  truth in classes 1 and 5, truth([0, 4], 1)

                In mutually-exclusive mode, a frame is expected to only
                belong to one class and thus all probabilities must sum to
                1, and there should be a class for "other" or "none". This
                is effectively truth for a classifier with multichannel
                softmax output. SonusAI will automatically calculate class
                num_classes as 1 - sum(truth(1:num_classes-1). For
                example, a classifier for (dog, cat) must have
                num_classes=3 to include "none" in truth(3).

                For multi-label classification each class is an individual
                probability for that class and any given frame can be
                assigned to multiple classes/labels, i.e., the classes are
                not mutually-exclusive. For example, a NN classifier with
                multichannel sigmoid output. In this case, index could
                also be a vector with multiple class indices. num_classes
                should be set to the number of classes/categories.

  'class_balancing_augmentation'
                Target-specific class balancing augmentation override.
                This target will not use the global class balancing
                augmentation rule, but will use this rule instead for
                class balancing operations. If this rule is specified and
                empty, then this target will not be used for class
                balancing.

  'target_level_type'
                Target-specific override for target_level_type.

Example:

targets:
  - name: data/esc50/ESC-50-master/audio/1-*.wav
    truth_settings:
      function: sed
      config:
        thresholds: [-38, -41, -48]
      index: 2
  - name: target.mp3
    truth_settings:
      function: sed
      config:
        thresholds: [-38, -41, -48]
      index: 5
    class_balancing_augmentation: { }
""" + default


def doc_num_classes() -> str:
    default = f"\nDefault value: {get_default_config()['num_classes']}"
    return """
'num_classes' is a mixture database configuration parameter that sets the number of
classes in this dataset. The number of classes is the total number of parameters
(or classes or labels) in the truth. This controls the size of the truth input to
the model.

Note that the model output 'parameters' dimension is NOT necessarily the same size
as the truth 'num_classes' dimension; there may be multiple truth functions combined
in the truth, e.g., for use in loss function calculations.
""" + default


def doc_class_labels() -> str:
    default = f"\nDefault value: {get_default_config()['class_labels']}"
    return """
'class_labels' is a mixture database configuration parameter that sets class labels
in this dataset.
""" + default


def doc_class_weights_threshold() -> str:
    default = f"\nDefault value: {get_default_config()['class_weights_threshold']}"
    return """
'class_weights_threshold' is a mixture database configuration parameter that sets
the threshold for class weights calculation to quantize truth to binary for counting.

Supports scalar or list:

 scalar     use for all classes
 list       must be of num_classes length
""" + default


def doc_truth_mode() -> str:
    default = f"\nDefault value: {get_default_config()['truth_mode']}"
    return """
'truth_mode' is a mixture database configuration parameter that sets the truth output
mode.

Supported values:

 normal     multi-label (no automatic calculation of other class)
            Set 'num_classes' to the actual number of classification categories.

 mutex      mutually-exclusive
            Set 'num_classes' to the actual number of classification categories plus 1
            to include a "none" category which will be set to 1 - truth (where truth is
            active for only one label) for all frames, to guarantee that the sum of all
            truth outputs is equal to 1. This is required to support softmax()
            neural-net outputs for multi-class classification (single label case).
""" + default


def doc_truth_reduction_function() -> str:
    default = f"\nDefault value: {get_default_config()['truth_reduction_function']}"
    return """
'truth_reduction_function' is a mixture database configuration parameter that set the
truth reduction function. It is used during feature generation to reduce sample-based
truth down to transform frame-based truth. The feature generator further reduces this
down to feature frame-based truth (based on stride and decimation).

Supported values:

 max        Returns the max value in a transform frame
 mean       Returns the mean of a transform frame
 index0     Returns the first value in a transform frame
""" + default


def get_truth_functions() -> str:
    from sonusai.mixture import truth_functions

    functions = [function for function in dir(truth_functions) if not function.startswith('__')]
    text = "\nSupported truth functions:\n\n"
    for function in functions:
        docs = getattr(truth_functions, function).__doc__
        if docs is not None:
            text += f"    {function}\n"
            for doc in docs.splitlines():
                text += f"        {doc}\n"
    return text


def doc_truth_settings() -> str:
    import yaml

    from sonusai.mixture import get_default_config
    default = f"\nDefault value:\n\n{yaml.dump(get_default_config()['truth_settings'])}"
    return """
'truth_settings' is a mixture database configuration parameter that sets the truth
generation settings for targets. There is a global 'truth_settings' and there may be
target-specific 'truth_settings'.

A truth setting creates a type of truth and is associated with target file(s).
Target files may have multiple truth settings.
Truth may be non-temporal, per sample, or per feature frame and each value may be scalar
or vector.

Note that there is a difference between transform frames and feature frames: a feature
frame can potentially have a stride dimension (which aggregates multiple transform
frames in a single feature).

There are two notions of truth data: truth_t and truth_f. truth_t is what the truth
functions always generate and it is in the time domain. truth_f, or truth in the feature
domain, is created from truth_t in the following manner. First, the
'truth_reduction_function' specified by the config reduces truth_t into truth data in
the transform frame domain. Then, this transform frame domain truth data is passed
into the feature generator which produces feature frame domain truth data. 

The 'truth_settings' parameter specifies the following:

 'function'     Name of truth function
 'config'       Truth function specific config dictionary
 'index'        Truth index is either a single int or a list of ints

                'index' indicates which truth fields should be set.
                0 indicates none, 1 is the first element in the truth output
                vector, 2 is the 2nd element, etc.

                Examples:
                  index = 5       truth in class 5, truth(4, 1)
                  index = [1, 5]  truth in classes 1 and 5, truth([0, 4], 1)

                In mutually-exclusive mode, a frame is expected to only
                belong to one class and thus all probabilities must sum to
                1, and there should be a class for "other" or "none". This
                is effectively truth for a classifier with multichannel
                softmax output. SonusAI will automatically calculate class
                num_classes as 1 - sum(truth(1:num_classes-1). For
                example, a classifier for (dog, cat) must have
                num_classes=3 to include "none" in truth(3).

                For multi-label classification each class is an individual
                probability for that class and any given frame can be
                assigned to multiple classes/labels, i.e., the classes are
                not mutually-exclusive. For example, a NN classifier with
                multichannel sigmoid output. In this case, index could
                also be a vector with multiple class indices. num_classes
                should be set to the number of classes/categories.
""" + get_truth_functions() + default


def doc_asr_manifest() -> str:
    default = f"\nDefault value: {get_default_config()['asr_manifest']}"
    return """
'asr_manifest' is a mixture database configuration parameter that defines an
optional ASR manifest.

The parameter takes a list of manifest files to be used to populate ASR data
per target. Each line of the manifest should be in the following format:

{"audio_filepath": "/path/to/audio.wav", "text": "the transcription of the utterance", "duration": 23.147}

The audio_filepath field should provide an absolute path to the audio file corresponding
to the utterance. The text field should contain the full transcript for the utterance,
and the duration field should reflect the duration of the utterance in seconds.

Each entry in the manifest (describing one audio file) should be bordered by '{' and '}'
and must be contained on one line. The fields that describe the file should be separated
by commas, and have the form "field_name": value, as shown above.

Since the manifest specifies the path for each utterance, the audio files do not have to be
located in the same directory as the manifest, or even in any specific directory structure.
""" + default


def doc_augmentations() -> str:
    return """
Augmentation Rules

These rules may be specified for target and/or noise. Each rule will be
applied for each target/noise. The values may be specified as scalars, lists,
or random using the syntax: 'rand(<min>, <max>)'.

If a value is specified as a list, then the rule is repeated for each value in
the list.

If a value is specified using rand, then a randomized rule is generated
dynamically per use.

Rules may specify any or all of the following augmentations:

 'normalize'    Normalize audio file to the specified level (in dBFS).
 'gain'         Apply an amplification or an attenuation to the audio signal.
                The signal level is adjusted by the given number of dB; positive
                amplifies, negative attenuates, 0 does nothing.
 'pitch'        Change the audio pitch (but not its tempo). Pitch amount is
                specified as positive or negative 'cents' (i.e., 100ths of a
                semitone).
 'tempo'        Change the audio tempo (but not its pitch). Tempo amount is
                specified as the ratio of the new tempo to the old tempo. For
                example, '1.1' speeds up the tempo by 10% and '0.9' slows it
                down by 10%.
 'eq1'          Apply a two-pole peaking equalization filter. EQ parameters are
                specified as a [frequency, width, gain] triple where:
                  'frequency' gives the central frequency in Hz (20 - SR/2),
                  'width' gives the width as a Q-factor (0.3 - 2.0), and
                  'gain' gives the gain in dB (-20 - 20).
 'eq2'          Apply an additional band of EQ. Same as 'eq1'
 'eq3'          Apply an additional band of EQ. Same as 'eq1'
 'lpf'          Apply a low-pass Butterworth filter. The 3 dB point frequency is
                specified in Hz (20 - SR/2).
 'ir'           An index into a list of impulse responses (specified in the
                'impulse_responses' parameter).
                For targets, the impulse response is applied AFTER truth generation
                and the resulting audio is still aligned with the truth. Random
                syntax for 'ir' is simply 'rand' (i.e., do not specify <min> and <max>).

Only the specified augmentations for a given rule are applied; all others are
skipped in the given rule. For example, if a rule only specifies 'tempo',
then only a tempo augmentation is applied and all other possible augmentations
are ignored (e.g., 'gain', 'pitch', etc.).

Example:

target_augmentations:
  - normalize: -3.5
  - normalize: -3.5
    pitch: [-300, 300]
    tempo: [0.8, 1.2]
    eq1: [[1000, 0.8, 3], [600, 1.0, -4], [800, 0.6, 0]]
  - normalize: -3.5
    pitch: "rand(-300, 300)"
    eq1: ["rand(100, 6000)", "rand(0.6, 1.0)", "rand(-6, 6)"]
    lpf: "rand(1000, 8000)"
  - tempo: "rand(0.9, 1.1)"
    eq1: [["rand(100, 7500)", 0.8, -10], ["rand(100, 7500)", 0.8, 10]]

There are four rules given in this example.

The first rule is simple:
  - normalize: -3.5

This results in just one augmentation being applied to each target:

  normalize: -3.5

The second rule illustrates the use of lists to specify values:
  - normalize: -3.5
    pitch: [-300, 300]
    tempo: [0.8, 1.2]
    eq1: [[1000, 0.8, 3], [600, 1.0, -4], [800, 0.6, 0]]

There are two values given for pitch, two for tempo, and three for EQ. This
rule expands to 2 * 2 * 3 = 12 unique augmentations being applied to each
target:

  normalize: -3.5, pitch: -3, tempo: 0.8, eq1: [1000, 0.8,  3]
  normalize: -3.5, pitch: -3, tempo: 0.8, eq1: [ 600, 1.0, -4]
  normalize: -3.5, pitch: -3, tempo: 0.8, eq1: [ 800, 0.6,  0]
  normalize: -3.5, pitch: -3, tempo: 1.2, eq1: [1000, 0.8,  3]
  normalize: -3.5, pitch: -3, tempo: 1.2, eq1: [ 600, 1.0, -4]
  normalize: -3.5, pitch: -3, tempo: 1.2, eq1: [ 800, 0.6,  0]
  normalize: -3.5, pitch:  3, tempo: 0.8, eq1: [1000, 0.8,  3]
  normalize: -3.5, pitch:  3, tempo: 0.8, eq1: [ 600, 1.0, -4]
  normalize: -3.5, pitch:  3, tempo: 0.8, eq1: [ 800, 0.6,  0]
  normalize: -3.5, pitch:  3, tempo: 1.2, eq1: [1000, 0.8,  3]
  normalize: -3.5, pitch:  3, tempo: 1.2, eq1: [ 600, 1.0, -4]
  normalize: -3.5, pitch:  3, tempo: 1.2, eq1: [ 800, 0.6,  0]

The third rule shows the use of rand:
  - normalize: -3.5
    pitch: "rand(-300, 300)"
    eq1: ["rand(100, 6000)", "rand(0.6, 1.0)", "rand(-6, 6)"]
    lpf: "rand(1000, 8000)"

This rule is used to create randomized augmentations per use.

The fourth rule demonstrates the use of scalars, lists, and rand:
  - tempo: [0.9, 1, 1.1]
    eq1: [["rand(100, 7500)", 0.8, -10], ["rand(100, 7500)", 0.8, 10]]

This rule expands to 6 unique augmentations being applied to each target
(list of 3 * list of 2). Here is the expansion:

  tempo: 0.9, eq1: ["rand(100, 7500)", 0.8, -10]
  tempo: 1.0, eq1: ["rand(100, 7500)", 0.8, -10]
  tempo: 1.1, eq1: ["rand(100, 7500)", 0.8, -10]
  tempo: 0.9, eq1: ["rand(100, 7500)", 0.8, 10]
  tempo: 1.0, eq1: ["rand(100, 7500)", 0.8, 10]
  tempo: 1.1, eq1: ["rand(100, 7500)", 0.8, 10]"""


def doc_target_augmentations() -> str:
    import yaml

    from sonusai.mixture import get_default_config
    default = f"\nDefault value:\n\n{yaml.dump(get_default_config()['target_augmentations'])}"
    return """
'target_augmentations' is a mixture database configuration parameter that
specifies a list of augmentation rules to use for each target.

See 'augmentations' for details on augmentation rules.
""" + default


def doc_class_balancing_augmentation() -> str:
    import yaml

    from sonusai.mixture import get_default_config
    default = f"\nDefault value:\n\n{yaml.dump(get_default_config()['class_balancing_augmentation'])}"
    return """
'class_balancing_augmentation' is a mixture database configuration parameter
that sets the default augmentation rule to use for generating class balancing
target data. This rule must contain at least one random entry in order to
guarantee unique additional data.

See 'augmentations' for details on augmentation rules.
""" + default


def doc_class_balancing() -> str:
    default = f"\nDefault value: {get_default_config()['class_balancing']}"
    return """
'class_balancing' is a mixture database configuration parameter that
enables/disables class balancing.

Class balancing ensures that each class in a sound classification dataset is
represented equally (i.e., each class has the same number of augmented targets).
This is achieved by creating new class balancing augmentation rules and applying
them to targets in underrepresented classes to create more augmented targets
for those classes.
""" + default


def doc_noises() -> str:
    default = f"\nDefault value: {get_default_config()['class_balancing']}"
    return """
'noises' is a mixture database configuration parameter that sets the list of
noises to use.

Required field:

 'name'
                File name. May be one of the following:

   audio        Supported formats are .wav, .mp3, .aif, .flac, and .ogg
   glob         Matches file glob patterns
   .yml         The given YAML file is parsed into the list
   .txt         Each line in the given text file indicates an item which
                may be anything in this list (audio, glob, .yml, or .txt)
""" + default


def doc_noise_augmentations() -> str:
    import yaml

    from sonusai.mixture import get_default_config
    default = f"\nDefault value:\n\n{yaml.dump(get_default_config()['noise_augmentations'])}"
    return """
'noise_augmentations' is a mixture database configuration parameter that
specifies a list of augmentation rules to use for each noise.

See 'augmentations' for details on augmentation rules.
""" + default


def doc_snrs() -> str:
    default = f"\nDefault value: {get_default_config()['snrs']}"
    return """
'snrs' is a mixture database configuration parameter that specifies a list
of required signal-to-noise ratios (in dB).

All other augmentations are applied to both target and noise and then the
energy levels are measured and the appropriate noise gain calculated to
achieve the desired SNR.

Special values:

 -99    Noise only mixture (no target)
 99     Target only mixture (no noise)
""" + default


def doc_random_snrs() -> str:
    default = f"\nDefault value: {get_default_config()['random_snrs']}"
    return """
'random_snrs' is a mixture database configuration parameter that specifies a
list of random signal-to-noise ratios. The value(s) must be specified as
random using the syntax: 'rand(<min>, <max>)'.

Random SNRs behave slightly differently from regular or ordered SNRs. As with
ordered SNRs, all other augmentations are applied to both target and noise and
then the energy levels are measured and the appropriate noise gain calculated
to achieve the desired SNR. However, unlike ordered SNRs, the desired SNR is
randomized (per the given rule(s)) for each mixture, i.e., previous random
SNRs are not saved and reused.
""" + default


def doc_noise_mix_mode() -> str:
    default = f"\nDefault value: {get_default_config()['noise_mix_mode']}"
    return """
'noise_mix_mode' is a mixture database configuration parameter that sets
how to mix noises with targets.

Supported modes:

 exhaustive          Use every noise/augmentation with every target/augmentation.
 non-exhaustive      Cycle through every target/augmentation without necessarily
                     using all noise/augmentation combinations (reduced data set).
 non-combinatorial   Combine a target/augmentation with a single cut of a
                     noise/augmentation non-exhaustively (each target/augmentation
                     does not use each noise/augmentation). Cut has a random start
                     and loops back to the beginning if the end of a
                     noise/augmentation is reached.
""" + default


def doc_impulse_responses() -> str:
    default = f"\nDefault value: {get_default_config()['impulse_responses']}"
    return """
'impulse_responses' is a mixture database configuration parameter that specifies a
list of impulse response files to use.

See 'augmentations' for details.
""" + default


def doc_spectral_masks() -> str:
    default = f"\nDefault value: {get_default_config()['spectral_masks']}"
    return """
'spectral_masks' is a mixture database configuration parameter that specifies
a list of spectral mask rules.

All other augmentations are applied including SNR and a mixture is generated
and then the spectral mask rules are applied to the resulting mixture feature.

Rules must specify all the following parameters:

 'f_max_width'      Frequency mask maximum width in bins
 'f_num'            Number of frequency masks to apply (set to 0 to apply none)
 't_max_width'      Time mask maximum width in frames
 't_num'            Number of time masks to apply (set to 0 to apply none)
 't_max_percent'    Upper bound on the width of the time mask in percent
""" + default


def doc_config() -> str:
    from sonusai.mixture import VALID_CONFIGS

    text = '\n'
    text += 'The SonusAI database is defined using a config.yml file.\n\n'
    text += 'See the following for details:\n\n'
    for c in VALID_CONFIGS:
        text += f' {c}\n'
    return text
