"""sonusai torchl_onnx

usage: torchl_onnx [-hv] [-b BATCH] [-t TSTEPS] [-o OUTPUT] MODEL CKPT

options:
    -h, --help
    -v, --verbose                   Be verbose
    -b BATCH, --batch BATCH         Batch size [default: 1]
    -t TSTEPS, --tsteps TSTEPS      Timesteps [default: 1]
    -o OUTPUT, --output OUTPUT      Output directory.

Convert a trained Pytorch Lightning model to ONNX.  The model is specified as an
sctl_*.py model file (sctl: sonusai custom torch lightning) and a checkpoint file
for loading weights.

Inputs:
    MODEL       SonusAI Python custom model file.
    CKPT        A Pytorch Lightning checkpoint file
    BATCH       Batch size used in onnx conversion, overrides value in model ckpt. Defaults to 1.
    TSTEPS      Timestep dimension size using in onnx conversion, overrides value in model ckpt if
                the model has a timestep dimension.  Else it is ignored.

Outputs:
    OUTPUT/     A directory containing:
                    <CKPT>.onnx        Model file with batch_size and timesteps equal to provided parameters
                    <CKPT>-b1.onnx     Model file with batch_size=1 and if the timesteps dimension exists it
                                       is set to 1 (useful for real-time inference applications)
                    torchl_onnx.log

Results are written into subdirectory <MODEL>-<TIMESTAMP> unless OUTPUT is specified.

"""
from sonusai import logger


def main() -> None:
    from docopt import docopt

    import sonusai
    from sonusai.utils import trim_docstring

    args = docopt(trim_docstring(__doc__), version=sonusai.__version__, options_first=True)

    verbose = args['--verbose']
    batch_size = args['--batch']
    timesteps = args['--tsteps']
    model_path = args['MODEL']
    ckpt_path = args['CKPT']
    output_dir = args['--output']

    from os import makedirs
    from os.path import basename, splitext
    from sonusai.utils import import_keras_model

    # Import model definition file first to check
    model_base = basename(model_path)
    model_root = splitext(model_base)[0]
    logger.info(f'Importing model from {model_base}')
    try:
        litemodule = import_keras_model(model_path)  # note works for pytorch lightning as well as keras
    except Exception as e:
        logger.exception(f'Error: could not import model from {model_path}: {e}')
        raise SystemExit(1)

    # Load checkpoint first to get hparams if available
    from torch import load as load
    ckpt_base = basename(ckpt_path)
    ckpt_root = splitext(ckpt_base)[0]
    logger.info(f'Loading checkpoint from {ckpt_base}')
    try:
        checkpoint = load(ckpt_path, map_location=lambda storage, loc: storage)
    except Exception as e:
        logger.exception(f'Error: could not load checkpoint from {ckpt_path}: {e}')
        raise SystemExit(1)

    from os.path import join, isdir, dirname, exists
    from sonusai import create_file_handler
    from sonusai import initial_log_messages
    from sonusai import update_console_handler
    from torch import randn
    from sonusai.utils import create_ts_name

    from sonusai.utils import create_ts_name
    from torchinfo import summary

    if batch_size is not None:
        batch_size = int(batch_size)
    if batch_size != 1:
        batch_size = 1
        logger.info(f'For now prediction only supports batch_size = 1, forcing it to 1 now')

    if timesteps is not None:
        timesteps = int(timesteps)

    if output_dir is None:
        output_dir = dirname(ckpt_path)
    else:
        if not isdir(output_dir):
            makedirs(output_dir, exist_ok=True)

    ofname = join(output_dir, ckpt_root + '.onnx')
    # First try, then add date
    if exists(ofname):
        # add hour-min-sec if necessary
        from datetime import datetime
        ts = datetime.now()
        ofname = join(output_dir, ckpt_root + '-' + ts.strftime('%Y%m%d') + '.onnx')
    ofname_root = splitext(ofname)[0]

    # Setup logging file
    create_file_handler(ofname_root + '-onnx.log')
    update_console_handler(verbose)
    initial_log_messages('torchl_onnx')
    logger.info(f'Imported model from {model_base}')
    logger.info(f'Loaded checkpoint from {ckpt_base}')

    if 'hyper_parameters' in checkpoint:
        hparams = checkpoint['hyper_parameters']
        logger.info(f'Found hyper-params on checkpoint named {checkpoint["hparams_name"]} '
                    f'with {len(hparams)} total hparams.')
        if batch_size is not None and hparams['batch_size'] != batch_size:
            if batch_size != 1:
                batch_size = 1
                logger.info(f'For now prediction only supports batch_size = 1, forcing it to 1 now')
            logger.info(f'Overriding batch_size: default = {hparams["batch_size"]}; specified = {batch_size}.')
            hparams["batch_size"] = batch_size

        if timesteps is not None:
            if hparams['timesteps'] == 0 and timesteps != 0:
                logger.warning(f'Model does not contain timesteps; ignoring override.')
                timesteps = 0

            if hparams['timesteps'] != 0 and timesteps == 0:
                logger.warning(f'Model contains timesteps; ignoring override of 0, using model default.')
                timesteps = hparams['timesteps']

            if hparams['timesteps'] != timesteps:
                logger.info(f'Overriding timesteps: default = {hparams["timesteps"]}; specified = {timesteps}.')
                hparams['timesteps'] = timesteps

        logger.info(f'Building model with hparams and batch_size={batch_size}, timesteps={timesteps}')
        try:
            model = litemodule.MyHyperModel(**hparams)  # use hparams
            # litemodule.MyHyperModel.load_from_checkpoint(ckpt_name, **hparams)
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_base} failed: {e}')
            raise SystemExit(1)
    else:
        logger.info(f'Warning: found checkpoint with no hyper-parameters, building model with defaults')
        try:
            tmp = litemodule.MyHyperModel()  # use default hparams
        except Exception as e:
            logger.exception(f'Error: model build (MyHyperModel) in {model_base} failed: {e}')
            raise SystemExit(1)

        if batch_size is not None:
            if tmp.batch_size != batch_size:
                logger.info(f'Overriding batch_size: default = {tmp.batch_size}; specified = {batch_size}.')
        else:
            batch_size = tmp.batch_size  # inherit

        if timesteps is not None:
            if tmp.timesteps == 0 and timesteps != 0:
                logger.warning(f'Model does not contain timesteps; ignoring override.')
                timesteps = 0

            if tmp.timesteps != 0 and timesteps == 0:
                logger.warning(f'Model contains timesteps; ignoring override.')
                timesteps = tmp.timesteps

            if tmp.timesteps != timesteps:
                logger.info(f'Overriding timesteps: default = {tmp.timesteps}; specified = {timesteps}.')
        else:
            timesteps = tmp.timesteps

        logger.info(f'Building model with default hparams and batch_size= {batch_size}, timesteps={timesteps}')
        model = litemodule.MyHyperModel(timesteps=timesteps, batch_size=batch_size)

    logger.info('')
    # logger.info(summary(model))
    # from lightning.pytorch import Trainer
    # from lightning.pytorch.callbacks import ModelSummary
    # trainer = Trainer(callbacks=[ModelSummary(max_depth=2)])
    # logger.info(trainer.summarize())
    logger.info('')
    logger.info(f'feature       {model.hparams.feature}')
    logger.info(f'num_classes   {model.num_classes}')
    logger.info(f'batch_size    {model.hparams.batch_size}')
    logger.info(f'timesteps     {model.hparams.timesteps}')
    logger.info(f'flatten       {model.flatten}')
    logger.info(f'add1ch        {model.add1ch}')
    logger.info(f'truth_mutex   {model.truth_mutex}')
    logger.info(f'input_shape   {model.input_shape}')
    logger.info('')
    logger.info(f'Loading weights from {ckpt_base}')
    # model = model.load_from_checkpoint(ckpt_path)     # weights only, has problems - needs investigation
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    insample_shape = model.input_shape
    insample_shape.insert(0, batch_size)
    input_sample = randn(insample_shape)
    logger.info(f'Creating onnx model ...')
    for m in model.modules():
        if 'instancenorm' in m.__class__.__name__.lower():
            logger.info(f'Forcing train=false for instancenorm instance {m}, {m.__class__.__name__.lower()}')
            m.train(False)
            # m.track_running_stats=True  # has problems
    model.to_onnx(file_path=ofname, input_sample=input_sample, export_params=True)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Canceled due to keyboard interrupt')
        exit()
