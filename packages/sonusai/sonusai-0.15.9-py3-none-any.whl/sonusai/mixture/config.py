from sonusai.mixture.datatypes import ImpulseResponseFiles
from sonusai.mixture.datatypes import NoiseFiles
from sonusai.mixture.datatypes import SpectralMasks
from sonusai.mixture.datatypes import TargetFiles


def raw_load_config(name: str) -> dict:
    """Load YAML config file

    :param name: File name
    :return: Dictionary of config data
    """
    import yaml

    with open(file=name, mode='r') as f:
        config = yaml.safe_load(f)

    return config


def get_default_config() -> dict:
    """Load default SonusAI config

    :return: Dictionary of default config data
    """
    from sonusai import SonusAIError
    from .constants import DEFAULT_CONFIG

    try:
        return raw_load_config(DEFAULT_CONFIG)
    except Exception as e:
        raise SonusAIError(f'Error loading default config: {e}')


def load_config(name: str) -> dict:
    """Load SonusAI default config and update with given location (performing SonusAI variable substitution)

    :param name: Directory containing mixture database
    :return: Dictionary of config data
    """
    from os.path import join

    return update_config_from_file(name=join(name, 'config.yml'), config=get_default_config())


def update_config_from_file(name: str, config: dict) -> dict:
    """Update the given config with the config in the YAML file

    :param name: File name
    :param config: Config dictionary to update
    :return: Updated config dictionary
    """
    from copy import deepcopy

    from sonusai import SonusAIError
    from .constants import REQUIRED_CONFIGS
    from .constants import VALID_CONFIGS
    from .constants import VALID_NOISE_MIX_MODES

    updated_config = deepcopy(config)

    try:
        new_config = raw_load_config(name)
    except Exception as e:
        raise SonusAIError(f'Error loading config from {name}: {e}')

    # Check for unrecognized keys
    for key in new_config:
        if key not in VALID_CONFIGS:
            nice_list = '\n'.join([f'  {item}' for item in VALID_CONFIGS])
            raise SonusAIError(f'Invalid config parameter in {name}: {key}.\n'
                               f'Valid config parameters are:\n{nice_list}')

    # Use default config as base and overwrite with given config keys as found
    for key in updated_config:
        if key in new_config:
            if key not in ['truth_settings']:
                updated_config[key] = new_config[key]

    # Handle 'truth_settings' special case
    if 'truth_settings' in new_config:
        updated_config['truth_settings'] = deepcopy(new_config['truth_settings'])

    if not isinstance(updated_config['truth_settings'], list):
        updated_config['truth_settings'] = [updated_config['truth_settings']]

    default = deepcopy(config['truth_settings'])
    if not isinstance(default, list):
        default = [default]

    updated_config['truth_settings'] = update_truth_settings(updated_config['truth_settings'], default)

    # Check for required keys
    for key in REQUIRED_CONFIGS:
        if key not in updated_config:
            raise SonusAIError(f'Missing required config in {name}: {key}')

    # Check for non-empty spectral masks
    if len(updated_config['spectral_masks']) == 0:
        updated_config['spectral_masks'] = config['spectral_masks']

    # Check for valid noise_mix_mode
    if updated_config['noise_mix_mode'] not in VALID_NOISE_MIX_MODES:
        nice_list = '\n'.join([f'  {item}' for item in VALID_NOISE_MIX_MODES])
        raise SonusAIError(f'Invalid noise_mix_mode in {name}.\n'
                           f'Valid noise mix modes are:\n{nice_list}')

    return updated_config


def update_truth_settings(given: list[dict] | dict, default: list[dict] = None) -> list[dict]:
    """Update missing fields in given 'truth_settings' with default values

    :param given: The dictionary of given truth settings
    :param default: The dictionary of default truth settings
    :return: Updated dictionary of truth settings
    """
    from copy import deepcopy

    from sonusai import SonusAIError
    from .constants import VALID_TRUTH_SETTINGS

    if isinstance(given, list):
        truth_settings = deepcopy(given)
    else:
        truth_settings = [deepcopy(given)]

    if default is not None and len(truth_settings) != len(default):
        raise SonusAIError(f'Length of given does not match default')

    for n in range(len(truth_settings)):
        for key in truth_settings[n]:
            if key not in VALID_TRUTH_SETTINGS:
                nice_list = '\n'.join([f'  {item}' for item in VALID_TRUTH_SETTINGS])
                raise SonusAIError(f'Invalid truth_settings: {key}.\nValid truth_settings are:\n{nice_list}')

        for key in VALID_TRUTH_SETTINGS:
            if key not in truth_settings[n]:
                if default is not None and key in default[n]:
                    truth_settings[n][key] = default[n][key]
                else:
                    raise SonusAIError(f'Missing required truth_settings: {key}')

    for truth_setting in truth_settings:
        if not isinstance(truth_setting['index'], list):
            truth_setting['index'] = [truth_setting['index']]

    return truth_settings


def get_hierarchical_config_files(root: str, leaf: str) -> list[str]:
    """Get a hierarchical list of config files in the given leaf of the given root

    :param root: Root of the hierarchy
    :param leaf: Leaf under the root
    :return: List of config files found in the hierarchy
    """
    import os
    from pathlib import Path

    from sonusai import SonusAIError

    config_file = 'config.yml'

    root_path = Path(os.path.abspath(root))
    if not root_path.is_dir():
        raise SonusAIError(f'Given root, {root_path}, is not a directory.')

    leaf_path = Path(os.path.abspath(leaf))
    if not leaf_path.is_dir():
        raise SonusAIError(f'Given leaf, {leaf_path}, is not a directory.')

    common = os.path.commonpath((root_path, leaf_path))
    if os.path.normpath(common) != os.path.normpath(root_path):
        raise SonusAIError(f'Given leaf, {leaf_path}, is not in the hierarchy of the given root, {root_path}')

    top_config_file = os.path.join(root_path, config_file)
    if not Path(top_config_file).is_file():
        raise SonusAIError(f'Could not find {top_config_file}')

    current = leaf_path
    config_files = []
    while current != root_path:
        local_config_file = Path(os.path.join(current, config_file))
        if local_config_file.is_file():
            config_files.append(str(local_config_file))
        current = current.parent

    config_files.append(top_config_file)
    return list(reversed(config_files))


def update_config_from_hierarchy(root: str, leaf: str, config: dict) -> dict:
    """Update the given config using the hierarchical config files in the given leaf of the given root

    :param root: Root of the hierarchy
    :param leaf: Leaf under the root
    :param config: Config to update
    :return: Updated config
    """
    from copy import deepcopy

    new_config = deepcopy(config)
    config_files = get_hierarchical_config_files(root=root, leaf=leaf)
    for config_file in config_files:
        new_config = update_config_from_file(name=config_file, config=new_config)

    return new_config


def get_max_class(num_classes: int, truth_mutex: bool) -> int:
    """Get the maximum class index

    :param num_classes: Number of classes
    :param truth_mutex: Truth is mutex mode
    :return: Highest class index
    """
    max_class = num_classes
    if truth_mutex:
        max_class -= 1
    return max_class


def get_target_files(config: dict, show_progress: bool = False) -> TargetFiles:
    """Get the list of target files from a config

    :param config: Config dictionary
    :param show_progress: Show progress bar
    :return: List of target files
    """
    from itertools import chain

    from tqdm import tqdm

    from sonusai import SonusAIError
    from sonusai.utils import dataclass_from_dict
    from sonusai.utils import pp_tqdm_imap
    from .datatypes import TargetFiles

    truth_settings = config.get('truth_settings', list())
    level_type = config.get('target_level_type', None)
    target_files = list(chain.from_iterable([append_target_files(entry=entry,
                                                                 truth_settings=truth_settings,
                                                                 level_type=level_type)
                                             for entry in config['targets']]))

    progress = tqdm(total=len(target_files), disable=not show_progress)
    target_files = pp_tqdm_imap(_get_num_samples, target_files, progress=progress)
    progress.close()

    max_class = get_max_class(config['num_classes'], config['truth_mode'] == 'mutex')

    for target_file in target_files:
        target_file['truth_settings'] = update_truth_settings(target_file['truth_settings'], config['truth_settings'])

        for truth_setting in target_file['truth_settings']:
            if any(idx > max_class for idx in truth_setting['index']):
                raise SonusAIError('invalid truth index')

    return dataclass_from_dict(TargetFiles, target_files)


def append_target_files(entry: dict | str,
                        truth_settings: list[dict],
                        level_type: str | None,
                        tokens: dict = None) -> list[dict]:
    """Process target files list and append as needed

    :param entry: Target file entry to append to the list
    :param truth_settings: Truth settings
    :param level_type: Target level type
    :param tokens: Tokens used for variable expansion
    :return: List of target files
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from sonusai import SonusAIError
    from .audio import validate_input_file
    from .tokenized_shell_vars import tokenized_expand
    from .tokenized_shell_vars import tokenized_replace

    if tokens is None:
        tokens = {}

    if isinstance(entry, dict):
        if 'name' in entry:
            in_name = entry['name']
        else:
            raise SonusAIError('Target list contained record without name')

        if 'truth_settings' in entry:
            truth_settings = entry['truth_settings']
        if 'target_level_type' in entry:
            level_type = entry['target_level_type']
    else:
        in_name = entry

    in_name, new_tokens = tokenized_expand(in_name)
    tokens.update(new_tokens)
    names = sorted(glob(in_name))
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')

    target_files: list[dict] = []
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                target_files.extend(append_target_files(entry=child,
                                                        truth_settings=truth_settings,
                                                        level_type=level_type,
                                                        tokens=tokens))
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expand(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                target_files.extend(append_target_files(entry=child,
                                                                        truth_settings=truth_settings,
                                                                        level_type=level_type,
                                                                        tokens=tokens))
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'targets' in yml_config:
                            for record in yml_config['targets']:
                                target_files.extend(append_target_files(entry=record,
                                                                        truth_settings=truth_settings,
                                                                        level_type=level_type,
                                                                        tokens=tokens))
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    validate_input_file(name)
                    target_file: dict = {
                        'expanded_name': name,
                        'name':          tokenized_replace(name, tokens),
                    }
                    if len(truth_settings) > 0:
                        target_file['truth_settings'] = truth_settings
                        for truth_setting in target_file['truth_settings']:
                            if 'function' in truth_setting and truth_setting['function'] == 'file':
                                truth_setting['config']['file'] = splitext(target_file['name'])[0] + '.h5'
                    if level_type is not None:
                        target_file['level_type'] = level_type
                    target_files.append(target_file)
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')

    return target_files


def get_noise_files(config: dict, show_progress: bool = False) -> NoiseFiles:
    """Get the list of noise files from a config

    :param config: Config dictionary
    :param show_progress: Show progress bar
    :return: List of noise file
    """
    from itertools import chain

    from tqdm import tqdm

    from sonusai.utils import dataclass_from_dict
    from sonusai.utils import pp_tqdm_imap
    from .datatypes import NoiseFiles

    noise_files = list(chain.from_iterable([append_noise_files(entry=entry) for entry in config['noises']]))

    progress = tqdm(total=len(noise_files), disable=not show_progress)
    noise_files = pp_tqdm_imap(_get_num_samples, noise_files, progress=progress)
    progress.close()

    return dataclass_from_dict(NoiseFiles, noise_files)


def append_noise_files(entry: dict | str, tokens: dict = None) -> list[dict]:
    """Process noise files list and append as needed

    :param entry: Noise file entry to append to the list
    :param tokens: Tokens used for variable expansion
    :return: List of noise files
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from sonusai import SonusAIError
    from .audio import validate_input_file
    from .tokenized_shell_vars import tokenized_expand
    from .tokenized_shell_vars import tokenized_replace

    if tokens is None:
        tokens = {}

    if isinstance(entry, dict):
        if 'name' in entry:
            in_name = entry['name']
        else:
            raise SonusAIError('Noise list contained record without name')
    else:
        in_name = entry

    in_name, new_tokens = tokenized_expand(in_name)
    tokens.update(new_tokens)
    names = sorted(glob(in_name))
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')

    noise_files: list[dict] = []
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                noise_files.extend(append_noise_files(entry=child, tokens=tokens))
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expand(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                noise_files.extend(append_noise_files(entry=child, tokens=tokens))
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'noises' in yml_config:
                            for record in yml_config['noises']:
                                noise_files.extend(append_noise_files(entry=record, tokens=tokens))
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    validate_input_file(name)
                    noise_file: dict = {
                        'expanded_name': name,
                        'name':          tokenized_replace(name, tokens),
                    }
                    noise_files.append(noise_file)
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')

    return noise_files


def get_impulse_response_files(config: dict, show_progress: bool = False) -> ImpulseResponseFiles:
    """Get the list of impulse response files from a config

    :param config: Config dictionary
    :param show_progress: Show progress bar
    :return: List of impulse response files
    """
    from itertools import chain

    return list(
        chain.from_iterable([append_impulse_response_files(entry=entry) for entry in config['impulse_responses']]))


def append_impulse_response_files(entry: str, tokens: dict = None) -> list[str]:
    """Process impulse response files list and append as needed

    :param entry: Impulse response file entry to append to the list
    :param tokens: Tokens used for variable expansion
    :return: List of impulse response files
    """
    from glob import glob
    from os import listdir
    from os.path import dirname
    from os.path import isabs
    from os.path import isdir
    from os.path import join
    from os.path import splitext

    from sonusai import SonusAIError
    from .audio import validate_input_file
    from .tokenized_shell_vars import tokenized_expand
    from .tokenized_shell_vars import tokenized_replace

    if tokens is None:
        tokens = {}

    in_name, new_tokens = tokenized_expand(entry)
    tokens.update(new_tokens)
    names = sorted(glob(in_name))
    if not names:
        raise SonusAIError(f'Could not find {in_name}. Make sure path exists')

    impulse_response_files: list[str] = []
    for name in names:
        ext = splitext(name)[1].lower()
        dir_name = dirname(name)
        if isdir(name):
            for file in listdir(name):
                child = file
                if not isabs(child):
                    child = join(dir_name, child)
                impulse_response_files.extend(append_impulse_response_files(entry=child, tokens=tokens))
        else:
            try:
                if ext == '.txt':
                    with open(file=name, mode='r') as txt_file:
                        for line in txt_file:
                            # strip comments
                            child = line.partition('#')[0]
                            child = child.rstrip()
                            if child:
                                child, new_tokens = tokenized_expand(child)
                                tokens.update(new_tokens)
                                if not isabs(child):
                                    child = join(dir_name, child)
                                impulse_response_files.extend(append_impulse_response_files(entry=child, tokens=tokens))
                elif ext == '.yml':
                    try:
                        yml_config = raw_load_config(name)

                        if 'impulse_responses' in yml_config:
                            for record in yml_config['impulse_responses']:
                                impulse_response_files.extend(
                                    append_impulse_response_files(entry=record, tokens=tokens))
                    except Exception as e:
                        raise SonusAIError(f'Error processing {name}: {e}')
                else:
                    validate_input_file(name)
                    impulse_response_files.append(tokenized_replace(name, tokens))
            except SonusAIError:
                raise
            except Exception as e:
                raise SonusAIError(f'Error processing {name}: {e}')

    return impulse_response_files


def get_spectral_masks(config: dict) -> SpectralMasks:
    """Get the list of spectral masks from a config

    :param config: Config dictionary
    :return: List of spectral masks
    """
    from sonusai import SonusAIError
    from sonusai.utils import dataclass_from_dict
    from .datatypes import SpectralMasks

    try:
        return dataclass_from_dict(SpectralMasks, config['spectral_masks'])
    except Exception as e:
        raise SonusAIError(f'Error in spectral_masks: {e}')


def _get_num_samples(entry: dict) -> dict:
    from .audio import get_num_samples

    entry['samples'] = get_num_samples(entry['expanded_name'])
    del entry['expanded_name']
    return entry
