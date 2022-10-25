#################################
###Loading data and Librairies###
#################################
import pandas as pd
import scipy.stats as ss


diabetes_raw = pd.read_csv("data/diabetes_data.csv", sep=";")

################################################
###Dataset shape, type and summary statistics###
################################################
print("shame of dataset is {}".format(diabetes_raw.shape))
print("-"*20)
print("Columns automaticly detected type is")
print(diabetes_raw.dtypes)
print("-"*20)
print("output of describe is")
print(diabetes_raw.describe())
print("-"*20)
print("Number unique values")
print(diabetes_raw.nunique())

###############################
###Checking for missing data###
###############################
def numberna_in_col(c : pd.Series) -> int:
    return(c.isna().sum())

number_na_per_column = diabetes_raw.apply(numberna_in_col)
print("-"*20)
print("Missing data")
print(number_na_per_column)

###########################################
###Features variability and correlations###
###########################################

##Transforming binary features into boolean class (except gender for clarity)
numerical_features = "age"
categorical_features = "gender"
features_to_change  = { k:"bool" for k in diabetes_raw.columns if not(k in (numerical_features + categorical_features))}
diabetes_df = diabetes_raw.astype(features_to_change)
categorical_features = [c for c in diabetes_raw.columns if not (c in numerical_features)]

##Computing Cramer's V (based on chisquare) to our categorical variables

    # """ calculate Cramers V statistic for categorial-categorial association.
    #     uses correction from Bergsma and Wicher,
    #     Journal of the Korean Statistical Society 42 (2013): 323-328
    # """

test_crosstab = pd.crosstab(diabetes_df["gender"], diabetes_df["obesity"])
chi2 = ss.chi2_contingency(confusion_matrix)[0]
