import nltk
from nltk import text
from nltk.tokenize import word_tokenize
from functions_ia import normalize_caseless
nltk.download('rslp')
stemmer = nltk.stem.RSLPStemmer()

def stem_sentenca(text):

    texto_normalizado = normalize_caseless(text)

    texto_split = word_tokenize(texto_normalizado)
    stem_sentenca = []
    for palavra in texto_split:
        stem_sentenca.append(stemmer.stem(palavra))
    
    return stem_sentenca