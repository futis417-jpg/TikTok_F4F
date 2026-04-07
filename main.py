import os
import random
import gdown
from tiktok_uploader.upload import upload_video
from moviepy.editor import ImageClip, AudioFileClip

# 1. Configurar Cookies
cookies_data = os.getenv('TIKTOK_COOKIES')
if cookies_data:
    with open('cookies.json', 'w') as f:
        f.write(cookies_data)

# 2. Descargar material (Súper-Buscador)
def preparar_material():
    folder_id = os.getenv('DRIVE_FOLDER_ID')
    url = f'https://drive.google.com/drive/folders/{folder_id}'
    print(f"🛰️ Conectando con Drive ID: {folder_id}")
    
    # Descargamos todo
    try:
        gdown.download_folder(url, quiet=False, use_cookies=False)
    except Exception as e:
        print(f"❌ Error al descargar de Drive: {e}")
        return None
    
    # --- LÍNEA DE DEBUG (Para ver qué hay en el servidor) ---
    print("📂 Archivos detectados en el servidor:")
    for root, dirs, files in os.walk("."):
        for name in files:
            print(f"  > Encontrado: {os.path.join(root, name)}")
    # -------------------------------------------------------

    # Buscamos archivos válidos
    formatos = ('.mp4', '.mov', '.jpg', '.png', '.jpeg', '.heic')
    archivos_encontrados = []
    
    for root, dirs, files in os.walk("."):
        # Evitamos carpetas ocultas de sistema
        if ".github" in root or ".git" in root:
            continue
        for name in files:
            if name.lower().endswith(formatos):
                archivos_encontrados.append(os.path.join(root, name))
    
    if not archivos_encontrados:
        print("❌ El bot no ve ningún vídeo ni foto. Revisa que haya archivos DENTRO de la carpeta de Drive.")
        return None
        
    seleccionado = random.choice(archivos_encontrados)
    print(f"🎯 OBJETIVO LOCALIZADO: {seleccionado}")
    return seleccionado

# 3. Convertir imagen a vídeo
def procesar_archivo(ruta):
    if ruta.lower().endswith(('.mp4', '.mov')):
        return ruta
    
    print(f"🎬 Transformando foto en vídeo de 7 segundos...")
    video_path = "temp_video.mp4"
    
    if not os.path.exists("music.mp3"):
        print("❌ ERROR CRÍTICO: No has subido 'music.mp3' a tu repositorio de GitHub.")
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
        print(f"❌ Error en la edición de vídeo: {e}")
        return None

# 4. Ejecución Final
def start():
    archivo = preparar_material()
    if not archivo: return
    
    final_file = procesar_archivo(archivo)
    if not final_file: return
    
    frases = ["Sígueme y te sigo ✅ #F4F", "Apoyo mutuo! 🚀", "Cumplo siempre 👇"]

    print("🚀 LANZANDO VÍDEO A TIKTOK...")
    try:
        upload_video(
            final_file,
            description=random.choice(frases),
            cookies='cookies.json',
            browser='chromium'
        )
        print("🔥 ¡MISIÓN CUMPLIDA! Revisa tu TikTok.")
    except Exception as e:
        print(f"❌ Falló el último empujón a TikTok: {e}")

if __name__ == "__main__":
    start()
