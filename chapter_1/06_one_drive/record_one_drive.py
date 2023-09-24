import sounddevice as sd
import soundfile as sf
import time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def printstuff(number):
    for i in range(number):
        print(i)

def async_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    print('can to execute this before finishing')
    printstuff(30)
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')

def upload_file(filename):
   
    # Autenticación con Google Drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Abre una ventana del navegador para autenticar
    # Crea una conexión a Google Drive
    drive = GoogleDrive(gauth)

    try:
        # Nombre que quieres darle al archivo en Google Drive
        drive_file_name = 'output_' + filename 
        # Sube el archivo al directorio raíz de Google Drive
        file = drive.CreateFile({'title': drive_file_name})
        # Establece el contenido del archivo desde la ubicación local
        file.SetContentFile(filename)
        file.Upload()
        # Verifica si la carga se realizó correctamente
        if file.uploaded:
            print('Archivo de audio subido a Google Drive con éxito.')

    except Exception as e:
        print('Se produjo un error en: ', e)

async_record('async_record.wav', 10, 16000, 1)
upload_file('async_record.wav')