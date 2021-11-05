#Imports
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import numpy as np
from dicts import getDict_ent, getDict_price
from functions_ia import identificador_intencao
from loo_knn import loo_knn_def, random_search
from loo_dt import loo_dt_def
from dataset import data_set_padrao
from text_to_num import text2num
from nltk.tokenize import word_tokenize
from functions_ia import normalize_caseless
nltk.download('rslp')

#utiliza um stem do tipo RSLP, compatível com a lingua portuguesa
#stem para uma frase. Com algumas tratativas, como deixar todas as palavras em lower case e sem acentuação
def stem_sentenca(text):

    texto_normalizado = normalize_caseless(text)
    
    texto_split = word_tokenize(texto_normalizado)
    
    stem_sentenca = []
    for palavra in texto_split:
        stem_sentenca.append(stemmer.stem(palavra))


    return stem_sentenca

#stem para uma lista, utilizada no dicionário
def stem_lista(lista):
    return([stemmer.stem(palavra) for palavra in lista])


#leitura do dataset(df) e definição do stemmer (stemmer)
df = data_set_padrao()
stemmer = nltk.stem.RSLPStemmer()


vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.6, strip_accents='unicode')
x = vectorizer.fit_transform(df.Sentença)
y = np.array(df.Intenção)

#KNN com LOO

loo_knn = loo_knn_def(x,y)

#Random search

#DESCOMENTAR, COMENTADO SOMENTE PARA MELHOR LEITURA DURANTE DESENVOLVIMENTO
#random_search(x, y)

#Árvore de decisão com LOO

loo_dt = loo_dt_def(x, y)


#Função principal, responsável por verificar entidades e construção da comanda
def main_function(data_input):
    #comandas
    comanda = []
    comanda_temp = []
    comanda_index_produto_temp = []
    comanda_index_quantidade_temp = []
    comanda_index_produto = []
    comanda_index_quantidade = []

    #mensagem, que será retornada ao usuário
    mensagem = ""

    #dicionário para as entidades
    dict_ent = getDict_ent()

    #dicionário para os precos
    dict_prec = getDict_price()

    #stem no dicionario
    stemmed_dict_ent = {}
    for key in dict_ent:
        stemmed_dict_ent[key] = stem_lista(dict_ent[key])

    
    #input do usuário e a tratativa para stem
    data_user = data_input
    data_user_split = data_user.split(" ")
    palavras = stem_sentenca(data_user)
    intencao = identificador_intencao(vectorizer.transform([normalize_caseless(data_user)]), x, y)

    #definição para o proceder das intenções    

    #caso seja uma intenção para listagem de produtos, é retornado a mensagem com a listagem pronta
    if intencao == "Produtos":
        mensagem = ("Claro, é pra já!\n")
        for produto in dict_ent["produto"]:
            mensagem += "\n• {}  -  R${}\n".format(produto, dict_prec[produto])

    #caso seja um pedido de produtos, será retornado uma mensagem, verificado as devidas entidades e montado uma comanda, que também será retornado
    elif intencao == "Pedido":
        mensagem = ("Claro, o que mais?")
        for palavra in palavras:
            for key, val in stemmed_dict_ent.items():
                if palavra in stemmed_dict_ent[key]:

                    if key == "produto":

                        comanda_index_produto_temp.append(int(palavras.index(palavra)))

                    if key == "quantidade":

                        comanda_index_quantidade_temp.append(int(palavras.index(palavra)))

                    if(len(comanda_index_produto_temp) == 1):
                        comanda_index_produto.append(comanda_index_produto_temp)
                        comanda_index_quantidade.append(comanda_index_quantidade_temp)   
                        comanda_index_produto_temp = []  
                        comanda_index_quantidade_temp = []

        #print("produtos: ", comanda_index_produto, "\nQuantidade: ", comanda_index_quantidade)

        #Utilizada a função "text2num", que transforma um número em extenso, em seu respectivo numeral, para ser adicionado na comanda definitiva
        while len(comanda_index_produto) != 0:
            for quantt in (comanda_index_quantidade):
                for quantidade in quantt:

                    if (data_user_split[quantidade] == "tres"):
                        data_user_split[quantidade] = "três"

                    if (len(data_user_split[quantidade]) > 1):
                        comanda_temp.append(text2num(data_user_split[quantidade], "pt"))
                    else:
                        comanda_temp.append(int(data_user_split[quantidade]))

                    comanda_index_quantidade.pop(comanda_index_quantidade.index(quantt))

                    for produtoo in (comanda_index_produto):

                        for produto in produtoo:
                            comanda_temp.append(data_user_split[produto])
                            comanda_index_produto.pop(comanda_index_produto.index(produtoo))
                            comanda.append(comanda_temp)
                            comanda_temp = []
                            #print(comanda)

    return mensagem, intencao, comanda



