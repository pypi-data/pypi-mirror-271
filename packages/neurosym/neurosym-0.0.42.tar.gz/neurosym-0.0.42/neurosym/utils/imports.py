import warnings


def import_pytorch_lightning():
    with warnings.catch_warnings():
        import pytorch_lightning as pl
    return pl
