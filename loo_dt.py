from sklearn.model_selection import LeaveOneOut
from sklearn import tree
from sklearn import metrics

def loo_dt_def (x, y):
    loo = LeaveOneOut()
    loo.get_n_splits(x)
    scores_dt = []
    for train_index, test_index in loo.split(x):

        x_treino, x_teste = x[train_index], x[test_index]
        y_treino, y_teste = y[train_index], y[test_index]
        
        clf = tree.DecisionTreeClassifier()
        clf.fit(x_treino,y_treino)
        pred = clf.predict(x_teste)
        scores_dt.append(metrics.accuracy_score(y_teste,pred))
        return clf

    return clf