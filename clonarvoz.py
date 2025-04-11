from torch.serialization import add_safe_globals

# Importar todas las clases que han causado errores
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsAudioConfig, XttsArgs
from TTS.config.shared_configs import BaseDatasetConfig

# Registrar todas como seguras para torch.load
add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])

# Importar y ejecutar TTS
from TTS.api import TTS

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(
    text="Este es un ejemplo de clonación de voz.",
    speaker_wav="Rodrigo.wav",
    language="es",
    file_path="voz_clonada.wav"
)
