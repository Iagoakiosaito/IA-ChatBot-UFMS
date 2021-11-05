import unicodedata
from loo_knn import loo_knn_def
from loo_dt import loo_dt_def


def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold()).encode("ASCII", "ignore").decode("ASCII")

def caseless_equal(left, right):
    return normalize_caseless(left) == normalize_caseless(right)

def identificador_intencao(text, x, y):
    clf = loo_dt_def(x, y)
    #model = loo_knn_def(x, y)
    
    predict = clf.predict(text)

    return predict

