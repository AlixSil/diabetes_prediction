#################################
###Loading data and Librairies###
#################################
import pandas as pd
import scipy.stats as ss
import itertools
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy

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

def cramersV(x : pd.Series, y: pd.Series) -> float :
    """ calculate Cramers V statistic for categorial-categorial association.
        uses correction from Bergsma and Wicher,
        Journal of the Korean Statistical Society 42 (2013): 323-328
    """
    contigency_table  = pd.crosstab(x, y)
    #Those are the elements of classic Cramer's V
    n = contigency_table.sum().sum()
    chi2 = ss.chi2_contingency(contigency_table)[0]
    phi2 = chi2/n
    k, r = contigency_table.shape

    #Computation of the unbiased versions
    phi2 = max(0, phi2 - ((k-1)*(r-1)/(n-1)))
    k = k - ((k-1)**2 /(n-1))
    r = r - ((r-1)**2 /(n-1))
    V = np.sqrt(phi2/min(k-1, r-1))
    return(V)


cramer_info = pd.DataFrame(itertools.product(categorical_features, categorical_features), columns = ["cat1", "cat2"])

def applyCramerV(lineOfCramerInfo) -> float :
    return(cramersV(  diabetes_df.loc[:,lineOfCramerInfo.cat1],  diabetes_df.loc[:,lineOfCramerInfo.cat2]))

cramer_info["cramer"] = cramer_info.apply(applyCramerV,axis=1)
cramer_info.cat1 = cramer_info.cat1.apply(lambda x : x.replace("_", " "))
cramer_info.cat2 = cramer_info.cat2.apply(lambda x : x.replace("_", " "))
cramer_info = cramer_info.pivot(index = "cat1", columns = "cat2", values = "cramer")

## We use a hierarchical clustering to order nicely the features, but this clustering in itself does not carry much value
Z = hierarchy.ward(cramer_info)
leaf_order = hierarchy.leaves_list(hierarchy.optimal_leaf_ordering(Z, cramer_info)).tolist()
leaf_order = [cramer_info.columns.tolist()[i] for i in leaf_order]

cramer_info = cramer_info.reindex(leaf_order)
cramer_info = cramer_info[leaf_order]


plt.figure()
ax = sns.heatmap(cramer_info, cmap="YlOrRd")
plt.title("Cramer's V relationship")
ax.set_ylabel('')
ax.set_xlabel('')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
plt.savefig("Images/cramersVrelationship.png", bbox_inches = "tight")
