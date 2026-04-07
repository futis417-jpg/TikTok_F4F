import os
import random
import gdown
from tiktok_uploader.upload import upload_video
from moviepy.editor import ImageClip, AudioFileClip

# 1. Configurar Cookies
cookies_data = os.getenv('TIKTOK_COOKIES')
with open('cookies.json', 'w') as f:
    f.write(cookies_data)

# 2. Descargar material de tu Drive
def preparar_material():
    folder_id = os.getenv('DRIVE_FOLDER_ID')
    url = f'https://drive.google.com/drive/folders/{folder_id}'
    print("Sincronizando con Drive...")
    
    # Descargamos los archivos
    gdown.download_folder(url, quiet=True, use_cookies=False)
    
    # Buscamos vídeos e imágenes descargados
    formatos = ('.mp4', '.mov', '.jpg', '.png', '.jpeg')
    archivos = [f for f in os.listdir() if f.lower().endswith(formatos)]
    return random.choice(archivos) if archivos else None

# 3. Convertir imagen a vídeo con tu music.mp3
def procesar_archivo(ruta):
    if ruta.lower().endswith(('.mp4', '.mov')):
        return ruta
    
    print(f"Procesando imagen con música: {ruta}")
    video_path = "temp_video.mp4"
    clip = ImageClip(ruta).set_duration(7) # 7 segundos de duración
    audio = AudioFileClip("music.mp3").set_duration(7)
    clip.set_audio(audio).write_videofile(video_path, fps=24, codec="libx264", audio_codec="aac", logger=None)
    return video_path

# 4. Ejecución
def start():
    archivo = preparar_material()
    if not archivo: return
    
    final_file = procesar_archivo(archivo)
    
    frases = [
        "Sígueme y te sigo al instante ✅ #F4F",
        "Apoyo mutuo real 🚀 Cumplo siempre",
        "Mutual Follow? Comenta 'listo' 👇",
        "Hagamos crecer esta cuenta juntos! 🌵"
    ]

    upload_video(
        final_file,
        description=random.choice(frases),
        cookies='cookies.json',
        browser='chromium'
    )

if __name__ == "__main__":
    start()
