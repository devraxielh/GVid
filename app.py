import json
import random
import string

from generador_guion import generar_guion_educativo
from buscar_videos import procesar_guion_y_descargar_videos
from generar_audio_por_escena import generar_audios_por_escena
def generar_hash_10_caracteres() -> str:
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=15))

if __name__ == "__main__":
    Hash = generar_hash_10_caracteres()
    tema = "Modelo MVC en programación"
    guion = generar_guion_educativo(tema, escenas=3, modelo="gemma3:27b",name_json=Hash)
    with open("./guiones/"+Hash+".json", 'r', encoding='utf-8') as archivo:
        guion_json = json.load(archivo)
    procesar_guion_y_descargar_videos(guion_json,Hash,cantidad_videos=1)
    generar_audios_por_escena(f'guiones/{Hash}.json',Hash)
