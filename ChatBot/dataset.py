import pandas as pd


def data_set_padrao():
    url = "https://raw.githubusercontent.com/Iagoakiosaito/DataSet-IA/main/Chatter-DB.csv"
    df=pd.read_csv(url)
    df = df[df['Orador'].notna()]
    df = df[df['Sentença'].notna()]
    df = df[df['Intenção'].notna()]
    df = df[(df.Orador == '<')]
    
    return df



