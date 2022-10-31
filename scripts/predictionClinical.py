#################################
###Loading data and librairies###
#################################
import pandas as pd
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import RocCurveDisplay
import matplotlib.pyplot as plt

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



##We will use an exhaustive grid search method to find the parameters that corresponds the most to our dataset

param_grid = [
  {
  "max_depth" : [None] + [range(2,10)],
  "max_leaf_nodes" : [5,7,10, 15],
  "min_samples_leaf" : [0.01, 0.02, 0.05, 0.1]
  }
 ]


decision_tree = DecisionTreeClassifier(random_state=0)
grid_search = GridSearchCV(decision_tree, param_grid)
grid_search.fit(X_train,y_train)


optimal_parameters = grid_search.best_params_
print("optimal parameters are {}".format(optimal_parameters))


##Now that we have the optimal parameters, we fit a decision tree on the totality of the train set and evaluate it
final_model = DecisionTreeClassifier(**optimal_parameters, random_state=0)
final_model.fit(X_train,y_train)
X_test_predict =final_model.predict(X_test)
y_train = y_train
contigency_table = pd.crosstab(X_test_predict, y_test, rownames = ["predicted values"], colnames = ["true values"])
final_accuracy = final_model.score(X_test, y_test)

plt.figure()
plot_tree(final_model, feature_names = X_test.columns, class_names = ["non-diabetic", "diabetic"])
plt.savefig("Images/tree.png", dpi=300)
