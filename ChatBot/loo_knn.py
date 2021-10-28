from sklearn.model_selection import LeaveOneOut
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import RandomizedSearchCV



def loo_knn_def(x,y):
    global model
    loo = LeaveOneOut()
    loo.get_n_splits(x)
    scores_knn = []
    for train_index, test_index in loo.split(x):

        x_treino, x_teste = x[train_index], x[test_index]
        y_treino, y_teste = y[train_index], y[test_index]
        
        model = KNeighborsClassifier(n_neighbors=9, weights= "uniform")
        model.fit(x_treino,y_treino)
        predi = model.predict(x_teste)
        scores_knn.append(metrics.accuracy_score(y_teste,predi))
        return model
    
    return model

def random_search(x, y):
    knn = loo_knn_def(x, y)
    parameters = {'n_neighbors':range(1,10),'weights':['uniform','distance']}
    rs = RandomizedSearchCV(model,parameters,n_iter=10,refit=True)
    rs.fit(x,y)
    print(rs.best_params_)