import requests
import os
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', 'OycznW5gB4wDiOfid1lgexEa3PwIVGni1sMG938L6prTv1hwolo8xhCn')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY', '15437676-902d10abbfd81a7082c72661d')
CARPETA_SALIDA = 'videos/'
def buscar_videos_pexels(query, n=3):
    url = 'https://api.pexels.com/videos/search'
    headers = {'Authorization': PEXELS_API_KEY}
    params = {'query': query, 'per_page': 50, 'orientation': 'landscape'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"⚠️ [Pexels] Error de API: {response.status_code} para '{query}'")
        return []
    datos = response.json()
    videos = datos.get('videos', [])
    if not videos:
        return []
    todos_los_video_files = []
    for video_info in videos:
        video_files = video_info.get('video_files', [])
        for vf in video_files:
            if vf.get('file_type') == 'video/mp4':
                todos_los_video_files.append(vf)
    todos_los_video_files.sort(
        key=lambda x: (-x.get('width', 0), x.get('file_size', float('inf')))
    )
    links = []
    for vf in todos_los_video_files:
        links.append(vf['link'])
        if len(links) == n:
            break
    return links

def buscar_videos_pixabay(query, n=3):
    url = 'https://pixabay.com/api/videos/'
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'orientation': 'horizontal',
        'per_page': 10
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"⚠️ [Pixabay] Error de API: {response.status_code} para '{query}'")
        return []
    datos = response.json()
    hits = datos.get('hits', [])
    if not hits:
        return []
    todos_los_videos = []
    for hit in hits:
        videos_dict = hit.get('videos', {})
        # cada hit puede tener varias calidades: 'large', 'medium', 'small', 'tiny'
        for calidad, info in videos_dict.items():
            url_video = info.get('url')
            width = info.get('width', 0)
            size = info.get('size', float('inf'))
            if url_video:
                todos_los_videos.append({
                    'url': url_video,
                    'width': width,
                    'size': size
                })
    todos_los_videos.sort(
        key=lambda x: (-x['width'], x['size'])
    )
    links = []
    for vid in todos_los_videos:
        links.append(vid['url'])
        if len(links) == n:
            break
    return links

def descargar_video(url, ruta_destino):
    try:
        respuesta = requests.get(url, stream=True, timeout=20)
        if respuesta.status_code == 200:
            with open(ruta_destino, 'wb') as f:
                for chunk in respuesta.iter_content(1024):
                    f.write(chunk)
            print(f'✅ Video guardado: {ruta_destino}')
        else:
            print(f'❌ Error al descargar video: {url} (status {respuesta.status_code})')
    except Exception as e:
        print(f'⚠️ Error de red al descargar {url}: {e}')

def procesar_guion_y_descargar_videos(guion_dict,Hash,cantidad_videos):
    historial = set()
    for clave, escena in guion_dict.items():
        descripcion = escena.get("descripcion", "")
        if not descripcion:
            continue
        palabras_clave = list(dict.fromkeys(
            p.strip() for p in descripcion.split(',')
        ))
        carpeta_escena = os.path.join(CARPETA_SALIDA+Hash, clave)
        os.makedirs(carpeta_escena, exist_ok=True)
        for palabra in palabras_clave:
            clave_normalizada = palabra.lower()
            if clave_normalizada in historial:
                print(f"↪️ Ya se descargó '{palabra}', se omite.")
                continue
            print(f"\n🔍 Buscando HASTA {cantidad_videos} videos para '{palabra}' en la escena '{clave}'")
            videos_encontrados = buscar_videos_pexels(palabra, n=cantidad_videos)
            if len(videos_encontrados) < cantidad_videos:
                faltantes = cantidad_videos - len(videos_encontrados)
                videos_pixabay = buscar_videos_pixabay(palabra, n=faltantes)
                videos_encontrados.extend(videos_pixabay)
            if videos_encontrados:
                for idx, link in enumerate(videos_encontrados, start=1):
                    nombre_archivo = (
                        f"{palabra.replace(' ', '_').replace('/', '-')}"
                        f"_{idx}.mp4"
                    )
                    ruta_destino = os.path.join(carpeta_escena, nombre_archivo)
                    descargar_video(link, ruta_destino)
                historial.add(clave_normalizada)
            else:
                print(f"⚠️ No se encontraron videos para '{palabra}' en ninguna API.")