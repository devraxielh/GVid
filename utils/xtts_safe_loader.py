from torch.serialization import add_safe_globals

from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.utils.radam import RAdam

def registrar_clases_seguras_xtts():
    add_safe_globals([
        XttsConfig,
        XttsAudioConfig,
        XttsArgs,
        BaseDatasetConfig,
        RAdam  # ✅ necesario para tacotron2-DDC
    ])
