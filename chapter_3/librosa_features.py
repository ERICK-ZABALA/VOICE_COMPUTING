import librosa
import numpy as np 

# get statistical features in numpy
def stats(matrix):
    mean=np.mean(matrix)
    std=np.std(matrix)
    maxv=np.amax(matrix)
    minv=np.amin(matrix)
    median=np.median(matrix)

    output=np.array([mean,std,maxv,minv,median])
    print(output)
    return output

# get labels for later 
def stats_labels(label, sample_list):
    mean=label+'_mean'
    std=label+'_std'
    maxv=label+'_maxv'
    minv=label+'_minv'
    median=label+'_median'
    sample_list.append(mean)
    sample_list.append(std)
    sample_list.append(maxv)
    sample_list.append(minv)
    sample_list.append(median)
    print(sample_list   )
    return sample_list

# featurize with librosa following documentation
# https://librosa.github.io/librosa/feature.html 
def librosa_featurize(filename, categorize):
    # if categorize == True, output feature categories 
    print('librosa featurizing: %s'%(filename))
    # initialize lists 
    onset_labels=list()
    y, sr = librosa.load(filename)
    # FEATURE EXTRACTION
    ######################################################
    # extract major features using librosa
    mfcc = librosa.feature.mfcc(y=y)
    print("MFC: ", mfcc)
    poly_features=librosa.feature.poly_features(y=y)
    chroma_cens=librosa.feature.chroma_cens(y=y)
    chroma_cqt=librosa.feature.chroma_cqt(y=y)
    chroma_stft=librosa.feature.chroma_stft(y=y)
    tempogram=librosa.feature.tempogram(y=y)

    spectral_centroid=librosa.feature.spectral_centroid(y=y)
    spectral_bandwidth=librosa.feature.spectral_bandwidth(y=y)
    spectral_contrast=librosa.feature.spectral_contrast(y=y)
    spectral_flatness=librosa.feature.spectral_flatness(y=y)
    spectral_rolloff=librosa.feature.spectral_rolloff(y=y)
    onset=librosa.onset.onset_detect(y=y)
    onset=np.append(len(onset),stats(onset))
    # append labels 
    onset_labels.append('onset_length')
    onset_labels=stats_labels('onset_detect', onset_labels)

    tempo=librosa.feature.rhythm.tempo(y=y)
    onset_features=np.append(onset,tempo)

    # append labels
    onset_labels.append('tempo')

    onset_strength=librosa.onset.onset_strength(y=y)
    onset_labels=stats_labels('onset_strength', onset_labels)
    zero_crossings=librosa.feature.zero_crossing_rate(y=y)
    rmse=librosa.feature.rms(y=y)

    # FEATURE CLEANING 
    ######################################################

    # onset detection features
    onset_features=np.append(onset_features,stats(onset_strength))


    # rhythm features (384) - take the first 13
    rhythm_features=np.concatenate(np.array([stats(tempogram[0]),
                                      stats(tempogram[1]),
                                      stats(tempogram[2]),
                                      stats(tempogram[3]),
                                      stats(tempogram[4]),
                                      stats(tempogram[5]),
                                      stats(tempogram[6]),
                                      stats(tempogram[7]),
                                      stats(tempogram[8]),
                                      stats(tempogram[9]),
                                      stats(tempogram[10]),
                                      stats(tempogram[11]),
                                      stats(tempogram[12])]))
    rhythm_labels=list()
    for i in range(13):
        rhythm_labels=stats_labels('rhythm_'+str(i), rhythm_labels)

    # spectral features (first 13 mfccs)
    spectral_features=np.concatenate(np.array([stats(mfcc[0]),
                                        stats(mfcc[1]),
                                        stats(mfcc[2]),
                                        stats(mfcc[3]),
                                        stats(mfcc[4]),
                                        stats(mfcc[5]),
                                        stats(mfcc[6]),
                                        stats(mfcc[7]),
                                        stats(mfcc[8]),
                                        stats(mfcc[9]),
                                        stats(mfcc[10]),
                                        stats(mfcc[11]),
                                        stats(mfcc[12]),
                                        stats(poly_features[0]),
                                        stats(poly_features[1]),
                                        stats(spectral_centroid),
                                        stats(spectral_bandwidth),
                                        stats(spectral_contrast),
                                        stats(spectral_flatness),
                                        stats(spectral_rolloff)])) 

    spectral_labels=list()
    for i in range(13):
        spectral_labels=stats_labels('mfcc_'+str(i), spectral_labels)
    for i in range(2):
        spectral_labels=stats_labels('poly_'+str(i), spectral_labels)
    spectral_labels=stats_labels('spectral_cenroid', spectral_labels)
    spectral_labels=stats_labels('spectral_bandwidth', spectral_labels)
    spectral_labels=stats_labels('spectral_contrast', spectral_labels)
    spectral_labels=stats_labels('spectral_flatness', spectral_labels)
    spectral_labels=stats_labels('spectral_rolloff', spectral_labels)

    # power features
    power_features=np.concatenate(np.array([stats(zero_crossings),
                                         stats(rmse)]))
    power_labels=list()
    power_labels=stats_labels('zero_crossings',power_labels)
    power_labels=stats_labels('RMSE', power_labels) 

    # you can also concatenate the features
    if categorize == True:
        # can output feature categories if true 
        features={'onset':onset_features,
                  'rhythm':rhythm_features,
                  'spectral':spectral_features,
                  'power':power_features}

        labels={'onset':onset_labels,
                'rhythm':rhythm_labels,
                'spectral':spectral_labels,
                'power': power_labels}
    else:
        # can output numpy array of everything if we don't need categorizations 
        features = np.concatenate(np.array([onset_features,
                                       rhythm_features,
                                       spectral_features,
                                       power_features]))
        labels=onset_labels+rhythm_labels+spectral_labels+power_labels

    return features, labels

features, labels =librosa_featurize('test.wav', True)
print(len(features['power']))
print(len(labels['power']))