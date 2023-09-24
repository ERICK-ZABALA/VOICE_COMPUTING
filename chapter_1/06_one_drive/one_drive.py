from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Autenticación con Google Drive
gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Abre una ventana del navegador para autenticar

# Crea una conexión a Google Drive
drive = GoogleDrive(gauth)

# Ruta local del archivo de audio
local_file_path = 'audio/one.mp3'

try:
    # Nombre que quieres darle al archivo en Google Drive
    drive_file_name = 'google_tts.mp3'
    # Sube el archivo al directorio raíz de Google Drive
    file = drive.CreateFile({'title': drive_file_name})
    # Establece el contenido del archivo desde la ubicación local
    file.SetContentFile(local_file_path)
    file.Upload()
    # Verifica si la carga se realizó correctamente
    if file.uploaded:
        print('Archivo de audio subido a Google Drive con éxito.')
    else:
        print('No se pudo cargar el archivo correctamente.')

except Exception as e:
    print('Se produjo un error en: ', e)
