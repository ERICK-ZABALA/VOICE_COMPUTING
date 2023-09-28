import spacy_features
# Alice’s Adventures in Wonderland = text
transcript = open('alice.txt', encoding='utf-8').read()

# python -m spacy download en_core_web_sm ---- verify
# vector size in function spacy_features

features, labels = spacy_features.spacy_featurize(transcript)

print('\nFeatures: ',features)
print('\nLabes:', labels)
print('\nLen features: ', len(features))
print('\nLen labels: ', len(labels))
