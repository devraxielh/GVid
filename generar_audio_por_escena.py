import os
import json
from TTS.api import TTS
from utils.xtts_safe_loader import registrar_clases_seguras_xtts

def generar_audios_por_escena(guion_json, hash_id):
    with open(guion_json, 'r', encoding='utf-8') as f:
        guion_json = json.load(f)
    CARPETA_SALIDA = f"audios/{hash_id}"
    os.makedirs(CARPETA_SALIDA, exist_ok=True)
    registrar_clases_seguras_xtts()
    tts = TTS(model_name="tts_models/es/css10/vits", gpu=True)#tts_models/es/mai/tacotron2-DDC

    for escena_id, contenido in guion_json.items():
        texto = contenido["voz_off"]
        ruta_audio = os.path.join(CARPETA_SALIDA, f"escena_{escena_id}.wav")
        print(f"🎙️ Generando audio: {ruta_audio}")
        tts.tts_to_file(text=texto, file_path=ruta_audio)