import json
from pydantic import BaseModel, Field,RootModel
from typing import Dict
import ollama
class Escena(BaseModel):
    voz_off: str = Field(..., description="Texto narrado")
    descripcion: str = Field(..., description="Palabras clave separadas por 'or'")
class GuionEducativo(RootModel[Dict[str, Escena]]):
    pass
def generar_guion_educativo(tema: str,escenas:int, modelo: str = "gemma3:4b", name_json:str="Not Name") -> GuionEducativo:
    prompt = (
        f"Genera un guion educativo dividido en {escenas} escenas sobre el tema '{tema}'. "
        "Para cada escena, proporciona un objeto con 'voz_off' en español. 'descripcion'. "
        "La 'descripcion' debe ser una una cadena de palabras clave separadas por coma, comenzando con términos relacionados directamente con el tema principal '{tema}' en ingles y luego complementando con conceptos claves extraídos del contenido de 'voz_off'"
        "Devuelve la respuesta en **formato JSON**, sin texto adicional, con la siguiente estructura:"
        """
            {{
            "1": {{
                "voz_off": "Texto de la escena 1",
                "descripcion": "palabraClaveIngles1, palabraClaveIngles2, palabraClaveIngles3, palabraClaveIngles4"
            }},
            "2": {{
                "voz_off": "Texto de la escena 2",
                "descripcion": "palabraClaveIngles1, palabraClaveIngles2, palabraClaveIngles3, palabraClaveIngles4"
            }},
            ...
            "{escenas}": {{
                "voz_off": "Texto de la escena {escenas}",
                "descripcion": "palabraClaveIngles1, palabraClaveIngles2, palabraClaveIngles3, palabraClaveIngles4"
            }}
            }}
        ¡¡Atención!! Asegúrate de devolver exactamente {escenas} escenas y no incluyas nada más fuera de las llaves.
        """
    )
    respuesta = ollama.chat(
        model=modelo,
        messages=[{"role": "user", "content": prompt}],
        format=GuionEducativo.model_json_schema(),
        stream=False
    )
    guion = GuionEducativo.model_validate_json(respuesta['message']['content'])
    with open("./guiones/"+name_json+".json", "w", encoding="utf-8") as f:
        json.dump(guion.model_dump(), f, ensure_ascii=False, indent=2)
    return guion
