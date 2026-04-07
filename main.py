import os
import random
import gdown
from tiktok_uploader.upload import upload_video
from moviepy.editor import ImageClip, AudioFileClip

# 1. Configurar Cookies desde los Secrets de GitHub
cookies_data = os.getenv('TIKTOK_COOKIES')
if cookies_data:
    with open('cookies.json', 'w') as f:
        f.write(cookies_data)

# 2. Descargar y buscar material en Drive (El Sabueso)
def preparar_material():
    folder_id = os.getenv('DRIVE_FOLDER_ID')
    url = f'https://drive.google.com/drive/folders/{folder_id}'
    print(f"🛰️ Conectando con Drive ID: {folder_id}")
    
    try:
        gdown.download_folder(url, quiet=True, use_cookies=False)
    except Exception as e:
        print(f"❌ Error al descargar de Drive: {e}")
        return None
    
    # Buscamos archivos en todas las carpetas bajadas
    formatos = ('.mp4', '.mov', '.jpg', '.png', '.jpeg', '.heic')
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

# 3. Convertir imagen a vídeo con música
def procesar_archivo(ruta):
    if ruta.lower().endswith(('.mp4', '.mov')):
        return ruta
    
    print(f"🎬 Creando vídeo de 7s con música...")
    video_path = "temp_video.mp4"
    
    if not os.path.exists("music.mp3"):
        print("❌ ERROR: No has subido 'music.mp3' a GitHub.")
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
        upload_video(
            final_file,
            description=random.choice(frases),
            cookies='cookies.json',
            browser='chromium',
            headless=True # Modo oculto para el servidor
        )
        print("🔥 ¡MISIÓN CUMPLIDA!")
    except Exception as e:
        print(f"❌ Fallo en TikTok: {e}")

if __name__ == "__main__":
    start()
