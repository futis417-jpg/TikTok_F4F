import os
import json
import random
import gdown
from tiktok_uploader.upload import upload_video
from moviepy.editor import ImageClip, AudioFileClip

# 1. Cargar Cookies de forma segura
def obtener_cookies():
    cookies_raw = os.getenv('TIKTOK_COOKIES')
    if not cookies_raw:
        print("❌ ERROR: No se encontró el Secret TIKTOK_COOKIES en GitHub.")
        return None
    try:
        # Intentamos cargar el JSON directamente
        return json.loads(cookies_raw)
    except Exception as e:
        print(f"❌ ERROR al leer las cookies: {e}")
        return None

# 2. Descargar material (El Sabueso)
def preparar_material():
    folder_id = os.getenv('DRIVE_FOLDER_ID')
    url = f'https://drive.google.com/drive/folders/{folder_id}'
    print(f"🛰️ Conectando con Drive ID: {folder_id}")
    
    try:
        gdown.download_folder(url, quiet=True, use_cookies=False)
    except Exception as e:
        print(f"❌ Error al descargar de Drive: {e}")
        return None
    
    formatos = ('.mp4', '.mov', '.jpg', '.png', '.jpeg')
    archivos_encontrados = []
    for root, dirs, files in os.walk("."):
        if ".github" in root or ".git" in root: continue
        for name in files:
            if name.lower().endswith(formatos):
                archivos_encontrados.append(os.path.join(root, name))
    
    if not archivos_encontrados:
        print("❌ No se encontró material válido.")
        return None
        
    seleccionado = random.choice(archivos_encontrados)
    print(f"🎯 OBJETIVO: {seleccionado}")
    return seleccionado

# 3. Convertir imagen a vídeo
def procesar_archivo(ruta):
    if ruta.lower().endswith(('.mp4', '.mov')):
        return ruta
    
    print(f"🎬 Creando vídeo de 7s con música...")
    video_path = "temp_video.mp4"
    if not os.path.exists("music.mp3"):
        print("❌ ERROR: Sube 'music.mp3' a tu repositorio de GitHub.")
        return None
        
    try:
        clip = ImageClip(ruta).set_duration(7)
        audio = AudioFileClip("music.mp3").set_duration(7)
        video = clip.set_audio(audio)
        video.write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
        clip.close()
        audio.close()
        return video_path
    except Exception as e:
        print(f"❌ Error en edición: {e}")
        return None

# 4. El Lanzamiento
def start():
    # Primero cargamos las cookies
    cookies_list = obtener_cookies()
    if not cookies_list: return

    archivo = preparar_material()
    if not archivo: return
    
    final_file = procesar_archivo(archivo)
    if not final_file: return
    
    frases = [
        "Sígueme y te sigo ✅ #F4F #apoyomutuo",
        "Apoyo mutuo real 🚀 Cumplo siempre!",
        "Mutual Follow? Comenta 'LISTO' 👇"
    ]

    print("🚀 LANZANDO A TIKTOK...")
    try:
        # Pasamos las cookies como una LISTA directamente
        upload_video(
            final_file,
            description=random.choice(frases),
            cookies=cookies_list, # <--- CAMBIO CLAVE AQUÍ
            browser='chromium',
            headless=True
        )
        print("🔥 ¡MISIÓN CUMPLIDA! Mira tu perfil.")
    except Exception as e:
        print(f"❌ Fallo en TikTok: {e}")

if __name__ == "__main__":
    start()
