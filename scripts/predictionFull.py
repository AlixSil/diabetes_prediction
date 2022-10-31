#################################
###Loading data and librairies###
#################################
import pandas as pd
import random
from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import RocCurveDisplay
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from lce import LCEClassifier
random.seed(1234)

diabetes_raw = pd.read_csv("data/diabetes_data.csv", sep=";")
diabetes_raw = diabetes_raw.drop_duplicates()
numerical_features = "age"
categorical_features = "gender"
features_to_change  = { k:"int" for k in diabetes_raw.columns if not(k in (numerical_features + categorical_features))}
diabetes_df = diabetes_raw.astype(features_to_change)
diabetes_df["gender"] = pd.get_dummies(diabetes_df["gender"], drop_first = True)


y = diabetes_df.loc[:,"class"]
X = diabetes_df.drop("class", axis = 1)


X_train, X_test, y_train, y_test= train_test_split(X, y, test_size = 0.2, random_state=1234)

def gridCV() :
    model1 = RandomForestClassifier(random_state = 0)
    model2 = GradientBoostingClassifier(random_state=0)
    model3 = LCEClassifier(random_state=0)

    params1 = {
        "n_estimators" : [10, 50, 100, 150],
        "min_samples_leaf" : [1, 2, 3, 4, 5, 10, 15]
    }
    params2 = {
        "n_estimators" : [10, 50, 100, 150],
        "min_samples_leaf" : [1, 2, 3, 4, 5, 10, 15]
    }
    params3 = {
        "n_estimators" : [10, 50, 100, 150],
        "min_samples_leaf" : [1, 2, 3, 4, 5, 10, 15]
    }

    d = {
        "Random Forest" : (model1, params1),
        "XGBoost" : (model2, params2),
        "LCE" : (model3, params3)
    }

    results = {}
    for m_name, (model, params) in d.items():
        print("Currently treating {}".format(m_name))
        grid_search = GridSearchCV(model, params, verbose = 2, n_jobs=4)
        grid_search.fit(X_train,y_train)
        print(grid_search.cv_results_.keys())

        test_score = grid_search.score(X_test, y_test)

        results[m_name] = (grid_search.best_score_ , grid_search.best_params_, grid_search.refit_time_, test_score)
    return(results)

results = gridCV()

results_df = pd.DataFrame(results, index = ["mean Cross Validation accuracy", "estimator_parameters","Time for fit (s)", "Accuracy on test dataset"])
results_df = results_df.drop("estimator_parameters")
