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

#Imports
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import numpy as np
from functions_ia import identificador_intencao
from loo_knn import loo_knn_def, random_search
from loo_dt import loo_dt_def
from dataset import data_set_padrao
from text_to_num import text2num
from nltk import text
from nltk.tokenize import word_tokenize
from functions_ia import normalize_caseless
nltk.download('rslp')


df = data_set_padrao()
stemmer = nltk.stem.RSLPStemmer()


vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.6, strip_accents='unicode')
x = vectorizer.fit_transform(df.Sentença)
y = np.array(df.Intenção)

#KNN com LOO

loo_knn = loo_knn_def(x,y)

#Random search

#random_search(x, y)

#Árvore de decisão com LOO

loo_dt = loo_dt_def(x, y)


#====================================
#               Parte 2
#====================================

#comandas, a comanda temporária existe para a criação de uma matriz com um 4
comanda = []
comanda_temp = []
comanda_index_produto_temp = []
comanda_index_quantidade_temp = []

comanda_index_produto = []
comanda_index_quantidade = []

#dicionário para as entidades
dict_ent = {

    "produto" : ["caderno", "lapis", "livro", "livros", "caneta", "canetas", "canetinha", "canetinhas", "papel", "papeis", "eva", "evas", "borracha", "borrachas"],
    "quantidade" : ["um", "uma", "dois", "duas", "tres", "quatro", "cinco", "seis", "sete", "oito", "nove", "dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", "dezessete", "dezoito", "dezenove", "vinte", 
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]

}

#dicionário para os precos
dict_prec = {
    "caderno": 15.5, "cadernos": 15.5, "lapis": 2.5, "lápis": 2.5, "livro": 50 , "livros" : 50, "caneta" : 3.5, "canetas" : 3.5, "canetinha": 12.80, "canetinhas": 12.80,
    "papel" : 32.90, "papeis" : 32.9, "eva" : 5.0, "evas" : 5.0, "borracha" : 2.5, "borrachas" : 2.5
}

#stem no dicionario
stemmed_dict_ent = {}
for key in dict_ent:
    stemmed_dict_ent[key] = stem_lista(dict_ent[key])

breaker = False

while breaker != True:
    #input do usuário e a tratativa para stem
    data_user = input(str("Usuário:"))
    data_user_split = data_user.split(" ")
    palavras = stem_sentenca(data_user)
    intencao = identificador_intencao(vectorizer.transform([normalize_caseless(data_user)]), x, y)

    #definição para o proceder das intenções    
    if intencao == "Saudação":
        print("Olá, seja bem-vindo(a), o que deseja?")

    if intencao == "Produtos":
        print("Claro, é pra já!\n")
        for produto in dict_ent["produto"]:
            print(produto)

    elif intencao == "Pedido":
        print("Claro, o que mais?")

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

    elif intencao == "Finalizar":
        preco = 0
        print("\nCerto! \nO pedido de: ")
        i = 1
        for item in comanda:
            print("{} -- ".format(i), item[0], " {}".format(item[1]))
            i += 1

        for item in comanda:
            preco += item[0] * dict_prec[item[1]]
            
        print("Preço final: R$", preco)
        breaker = True


    