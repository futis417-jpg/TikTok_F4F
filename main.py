import os
import json
import random
import gdown
from tiktok_uploader.upload import upload_video

# 1. Preparamos las cookies
cookies_json = os.getenv('TIKTOK_COOKIES')
with open('cookies.json', 'w') as f:
    f.write(cookies_json)

# 2. Descargamos un vídeo aleatorio de tu Drive
def descargar_video():
    folder_id = os.getenv('DRIVE_FOLDER_ID')
    # Usamos gdown para listar y bajar (necesitas la carpeta pública con el link)
    url = f'https://drive.google.com/drive/folders/{folder_id}'
    files = gdown.download_folder(url, quiet=True, use_cookies=False)
    
    # Elegimos uno al azar de los que se acaban de descargar
    video_files = [f for f in os.listdir() if f.endswith(('.mp4', '.mov'))]
    return random.choice(video_files)

# 3. Subida masiva
def ejecutar():
    video = descargar_video()
    frases = [
        "Sígueme y te sigo al instante ✅ #F4F",
        "Apoyo mutuo real 🚀 Cumplo siempre",
        "Si buscas seguidores, sígueme y mira la magia ✨",
        "Día 1 intentando llegar a 10k con apoyo mutuo"
    ]
    
    print(f"Subiendo: {video}")
    upload_video(
        video,
        description=random.choice(frases),
        cookies='cookies.json',
        browser='chromium'
    )

if __name__ == "__main__":
    ejecutar()
