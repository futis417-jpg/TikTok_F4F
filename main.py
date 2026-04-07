import os
import random
import gdown
from tiktok_uploader.upload import upload_video
from moviepy.editor import ImageClip, AudioFileClip

# 1. Preparar las llaves (Cookies)
cookies_json = os.getenv('TIKTOK_COOKIES')
if cookies_json:
    with open('cookies.json', 'w') as f:
        f.write(cookies_json)

# 2. Ir a por el botín (Google Drive)
def preparar_material():
    folder_id = os.getenv('DRIVE_FOLDER_ID')
    url = f'https://drive.google.com/drive/folders/{folder_id}'
    print(f"Conectando con la carpeta de Drive: {folder_id}")
    
    # Descargamos todo lo que hay en la carpeta
    gdown.download_folder(url, quiet=True, use_cookies=False)
    
    # Filtramos solo imágenes y vídeos
    formatos = ('.mp4', '.mov', '.jpg', '.png', '.jpeg')
    archivos = [f for f in os.listdir() if f.lower().endswith(formatos)]
    
    if not archivos:
        print("❌ No hay archivos válidos en la carpeta de Drive.")
        return None
        
    seleccionado = random.choice(archivos)
    print(f"✅ Seleccionado para hoy: {seleccionado}")
    return seleccionado

# 3. Convertir a vídeo si es una imagen
def procesar_archivo(ruta):
    if ruta.lower().endswith(('.mp4', '.mov')):
        return ruta
    
    print(f"🎬 Convirtiendo imagen a video con música...")
    video_temp = "subida_final.mp4"
    
    if not os.path.exists("music.mp3"):
        print("❌ ERROR: No has subido el archivo 'music.mp3' a GitHub.")
        return None

    try:
        # Creamos un clip de 7 segundos con la foto y la música
        clip = ImageClip(ruta).set_duration(7)
        audio = AudioFileClip("music.mp3").set_duration(7)
        video = clip.set_audio(audio)
        
        # Renderizamos el vídeo rápido
        video.write_videofile(video_temp, fps=24, codec="libx264", audio_codec="aac", logger=None)
        
        clip.close()
        audio.close()
        return video_temp
    except Exception as e:
        print(f"❌ Error procesando imagen: {e}")
        return None

# 4. El Gran Final: Subida a TikTok
def start():
    crudo = preparar_material()
    if not crudo: return
    
    listo = procesar_archivo(crudo)
    if not listo: return
    
    frases = [
        "Sígueme y te sigo al instante ✅ #F4F #apoyomutuo",
        "Apoyo mutuo real 🚀 Cumplo siempre, sígueme!",
        "Si quieres seguidores, sígueme y comenta 'LISTO' 👇",
        "Hagamos crecer esta cuenta juntos! 🌵"
    ]

    print("🚀 Subiendo a TikTok... espera un momento.")
    try:
        upload_video(
            listo,
            description=random.choice(frases),
            cookies='cookies.json',
            browser='chromium'
        )
        print("🔥 ¡VÍDEO PUBLICADO CON ÉXITO!")
    except Exception as e:
        print(f"❌ Fallo en el último paso (TikTok): {e}")

if __name__ == "__main__":
    start()
