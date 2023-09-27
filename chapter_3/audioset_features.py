
import os, shutil, json 
import sounddevice as sd
import soundfile as sf
import numpy as np
import tensorflow as tf

################################################################################
##                         HELPER FUNCTIONS                                  ##
################################################################################

# define some initial helper functions 
def sync_record(filename, duration, fs, channels):
    print('recording')
    myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()
    sf.write(filename, myrecording, fs)
    print('done recording')

def setup_audioset(curdir):
    # Upgrade pip first.
    os.system('python -m pip install --upgrade pip')

    # Install dependences. Resampy needs to be installed after NumPy and SciPy
    # are already installed.
    os.system('pip install numpy scipy')
    os.system('pip install resampy tensorflow six')

    # Clone TensorFlow models repo into a 'models' directory.
    if 'models' not in os.listdir():
        try:
            os.system('git clone https://github.com/tensorflow/models.git')
            os.chdir(curdir+'/models/research/audioset/vggish')
            print('pass change directory...')
            # add modified file in the current folder 
            # Definir la ruta completa al archivo de origen
            source_file = os.path.join(curdir, 'models', 'research', 'audioset', 'vggish', 'vggish_inference_demo.py')

            # Definir la ruta completa al archivo de destino
            destination_file = os.path.join(curdir, 'vggish_inference_demo.py')

            # Copiar el archivo
            shutil.copy(source_file, destination_file)
        except Exception as e:
            print("Existe un error: " + str(e))
    #os.remove('vggish_inference_demo.py')
    #shutil.copy(curdir+'\models\research\audioset\vggish\ggish_inference_demo.py', os.getcwd()+'\vggish_inference_demo.py')
    print('passed copy...')
    
    if 'audioset' not in os.listdir():
        try:
            # Download data files into same directory as code.
            os.system('curl -O https://storage.googleapis.com/audioset/vggish_model.ckpt')
            os.system('curl -O https://storage.googleapis.com/audioset/vggish_pca_params.npz')
            print('pass download')
                    
            # copy back into main directory and delete unnecessary models 
            shutil.copytree(curdir+'/models/research/audioset/', curdir+'/audioset')
            print('Move audioset folder ...')
        except Exception as e:
            print("Existe un error: " + str(e))
        
    ##shutil.rmtree(curdir+'/models')
    else:
        try:
            os.chdir('audioset/vggish/')
            cwd_test = os.getcwd()
            print("Directorio de trabajo actual antes del cambio: \n", cwd_test)
            print("\nTesting: vggish_smoke_test.py ...")
            os.system('python vggish_smoke_test.py')
        except Exception as e:
                print("Existe un error: " + str(e))
            
    
def audioset_featurize(filename):
    # textfile definition to dump terminal outputs
    # ruta = "'processdir/test3.wav'""audioset/vggish/test2.wav"
    partes = filename.split('/')
    nombre_archivo = partes[-1].split('.')[0]  # Esto obtiene "test2" sin la extensión .wav
    #print(nombre_archivo)  # Esto imprimirá "test2"

    jsonfile=nombre_archivo+'.json'
    print('JSON File: ', jsonfile)
    # audioset folder
    #os.chdir('audioset/vggish/')
    #os.chdir(os.getcwd()+'/processdir')
    cwd_test = os.getcwd()
    print("Directorio de trabajo actual antes del ejecutar vggish_inference_demo.py ... \n", cwd_test)
    
    cwd_dir = os.getcwd()+'\processdir'
    comando = 'python vggish_inference_demo.py --wav_file %s\%s.wav'%(cwd_dir, nombre_archivo)
    print('Executing Command: ', comando)
    os.system(comando)

    #os.system('mkdir processdir')
    # now reference this .JSON file
    #os.chdir('processdir/')
    os.chdir(os.getcwd()+'/processdir')
    
    cwd_test = os.getcwd()
    print("Directorio de trabajo actual antes crear JSON File... \n", cwd_test)
    
    datafile=json.load(open(jsonfile))
    print('data File:',list(datafile))
    features=datafile['features']

    # GET MEAN FEATURES 

    # initialize numpy array to add features into
    new_features_mean=np.zeros(len(features[0]))
    for i in range(len(features)):
        new_features_mean=new_features_mean+np.array(features[i])

    # now take mean of all these features 
    new_features_mean=(1.0/len(features))*new_features_mean

    # GET STD FEATURES
    new_features_std=list()
    for i in range(len(features[0])):
        # i=element in array to std 
        tlist=list()
        for j in range(len(features)):
            tlist.append(features[j][i])
        feature=np.array(tlist)
        std_feature=np.std(feature)
        new_features_std.append(std_feature)
    new_features_std=np.array(new_features_std)

    # append new features into mean and std 
    new_features=np.append(new_features_mean, new_features_std)

    # output VGGish feature array and compressed means/stds 

    return features, new_features 

################################################################################
##                               MAIN SCRIPT                                  ##
################################################################################

# get current directory 
curdir=os.getcwd()
print('curldir: ', curdir)
# download audioset files if audioset not in current directory 
if 'audioset' not in os.listdir():
    try:
        setup_audioset(curdir)
    except Exception as e:
        print('there was an error installing audioset: ' + str(e))

else:
         print('You did the Instalation the form correct...!')

# record a 10 second, mono 16k Hz audio file in the current directory
os.chdir('audioset/vggish/')
os.system('mkdir processdir')
cwd_test = os.getcwd()
print("Creando Directorio de trabajo: processdir ... \n", cwd_test)
 
filename='processdir/test3.wav'
sync_record(filename,10,16000,1)

# now let's featurize an audio sample in the current directory, test.wav 
features, new_features =audioset_featurize(filename)
print('new features')   
print(new_features)
print(len(new_features))




    
