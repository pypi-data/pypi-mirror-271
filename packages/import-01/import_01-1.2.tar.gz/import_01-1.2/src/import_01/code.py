print('''# -*- coding: utf-8 -*-


!pip install pandas-profiling

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")
import pandas_profiling as pp

"""# Reading the data and getting a general idea"""

df = pd.read_csv("star_dataset - Copy.csv")

df.head()

df.shape

df.describe()

df.info()

"""### Plotting Pair wise realtionships"""

sns.pairplot(df, hue="Star type");

"""### correlation heatmap"""

figure= plt.figure(figsize=(4,4))
sns.heatmap(df.corr(), annot=True);

"""### Generating Pandas Profoling Report"""

pp.ProfileReport(df)

"""# 1 . Plot histogram for the class labels in the dataset and also print the individual class count."""

class_counts = df['Star type'].value_counts()

class_names = {
    0: 'Brown Dwarf',
    1: 'Red Dwarf',
    2: 'White Dwarf',
    3: 'Main Sequence',
    4: 'Supergiant',
    5: 'Hypergiant'
}
class_labels = df['Star type'].map(class_names)

class_counts = class_labels.value_counts()

# Plot histogram for class labels
plt.figure(figsize=(10, 6))
plt.bar(class_counts.index, class_counts.values, color='skyblue', alpha=0.7)
plt.xlabel('Star Type')
plt.ylabel('Count')
plt.title('Histogram of Star Types')
plt.xticks(rotation=45, ha='right')
plt.show()

# Print individual class counts with their actual names
print("Class Counts:")
print(class_counts)

"""### Countplot showing no. of stars of each color




"""

ax = sns.countplot( x= df["Star color"])
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
plt.show()

"""#### Red is the most common color for stars

### Spectral class of stars on basis of absolute magnitude
"""

ax = sns.scatterplot(data = df, x = "Spectral Class", y = "Absolute magnitude(Mv)", hue = "Star type")
ax.set_yscale('log')
plt.show()

"""# 2. Check for any missing data, if the data is missing use any technique to overcome this problem."""

df.isnull().sum()

"""There are some null values present. Their presence in terms of percentage is given below."""

df.isnull().mean()*100

df_new = df

"""## Performing simple Imputation
Since, the size of the dataset is already small, we deal with null values by performing mean imputation.
"""

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean', missing_values=np.nan)
imputer = imputer.fit(df_new[['Temperature (K)','Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']])
df_new[['Temperature (K)','Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']] = imputer.transform(df_new[['Temperature (K)','Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']])
df_new

"""Checking null value after imputation"""

df_new.isnull().sum()

"""And it looks like we the null not there anymore"""

df_new['Star type'].value_counts()

df_new['Spectral Class'].value_counts()

"""# 3. Check for any outliers.

We will first plot box plots to check if outliers are present or not. There are 4 numerial columns in this data i.e. Temperature (K), Luminosity(L/Lo), Radius(R/Ro), Absolute magnitude(Mv)
"""

col = ["Temperature (K)","Luminosity(L/Lo)","Radius(R/Ro)","Absolute magnitude(Mv)" ]
fig, axes = plt.subplots(2, 2, figsize=(18, 13))
axes = axes.flatten()
for i , column in enumerate(col):
    sns.boxplot(ax=axes[i], x= df_new[column], notch=False,
    flierprops={"marker": "o"},
    boxprops={"facecolor": (.4, .6, .8, .5)},
    )
    axes[i].set_xlabel(column, fontsize= 14, fontweight='bold')

    axes[i].set_title(f'Box Plot for {column}', fontsize= 16, fontweight='bold')
fig.tight_layout(pad=3.0)

"""So, it is clear that all the columns have outliers present. Now lets deal with them

\Since, as already mentioned above, there are only 240 rows in this dataset, removing the rows with oultliers will only decrease the size of our dataset. We need to apply some other method to deal with them

In order to find the correct method, we should first see their distribution plots and find out their skewness and kurtosis.
"""

col = ["Temperature (K)","Luminosity(L/Lo)","Radius(R/Ro)","Absolute magnitude(Mv)" ]
fig, axes = plt.subplots(2, 2, figsize=(18, 13))
axes = axes.flatten()
for i , column in enumerate(col):
    sns.histplot(data=df_new, x=column, kde=True, ax=axes[i], log_scale=True)
    axes[i].set_title(f'Distribution of {column}, kurt = {df_new[column].kurt()}')

"""They all are very skewed, heavy-tailed/Leptokurtic gaussian distributions

To deal with them, we are going to perform **Capping** of outliers.
First we will find the IQR(Inter Quartile Range), then the lower bound and upper bound for a column and the replace the outliers with the lower or upper bound
"""

fig, axes = plt.subplots(2,2, figsize=(12, 8))
axes = axes.flatten()

for i, column in enumerate(col):
    q1 = df_new[column].quantile(0.25)
    q3 = df_new[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df_new[column] = df_new[column].clip(lower=lower_bound, upper=upper_bound)

    sns.histplot(data=df_new, x=column, kde=True, ax=axes[i], log_scale=True)
    axes[i].set_title(f'Distribution of {column} (Log Scale)',  fontweight = "bold")

plt.tight_layout(pad = 3.0)
plt.show()

"""After capping, we have successfully removed outliers. Given below are the boxplots after the process"""

col = ["Temperature (K)","Luminosity(L/Lo)","Radius(R/Ro)","Absolute magnitude(Mv)" ]
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
axes = axes.flatten()
for i , column in enumerate(col):
    sns.boxplot(ax=axes[i], x= df_new[column], notch=False,
    flierprops={"marker": "o"},
    boxprops={"facecolor": (.4, .6, .8, .5)},
    )
    axes[i].set_xlabel(column, fontsize = 12)

    axes[i].set_title(f'Box Plot for {column}', fontsize= 16, fontweight = "bold")
fig.tight_layout(pad=3.0)

df_new.head(100)

"""Now before moving forward, it is best if we perform encoding of our categorical columns.

## One - hot Encoding our categorical features
"""

df_new['Star color'].value_counts()

df_new['Spectral Class'].value_counts()

"""in Star Color column there are multiple colors with same name. It us probably due to presence of white spaces with the names. we will first do some color mapping and then perform encoding."""

# Fix Star color overlapping
color_mapping = {
    'Blue ': 'Blue',
    'Blue white': 'Blue White',
    'Blue-white': 'Blue White',
    'Blue white ': 'Blue White',
    'Blue-White': 'Blue White',
    'white': 'White',
    'yellow-white': 'Yellowish White',
    'White-Yellow': 'Yellowish White',
    'yellowish': 'Yellowish'
}
df_new['Star color'] = df_new['Star color'].replace(color_mapping)

df_new['Star color'].value_counts()

def onehot_encode(df, column, prefix):
    df = df.copy()
    dummies = pd.get_dummies(df[column], prefix=prefix)
    df = pd.concat([df, dummies], axis=1)
    df = df.drop(column, axis=1)
    return df

df_new = onehot_encode(df_new, column='Star color', prefix="Color")
df_new = onehot_encode(df_new, column='Spectral Class', prefix="Class")

df_new

"""This is our final dataset. All the columns are numerical.

# 4. Create a balanced dataset for all the classes.

check if dataset is balanced or not.
"""

df_new['Star type'].value_counts()

"""So the data is completely balanced. none of the classes outnumbers other. So we dont really need to do anything here. The histplot for the same is given below."""

sns.histplot(x = df_new['Star type'],binwidth = 0.5, linewidth = 2);

"""## Splitting our dataset into independent and dependent features"""

X = df_new.drop('Star type', axis=1)
y = df_new['Star type']

X

"""# 6. Normalize, Scale the data if it is required.

## Scaling our data

We are going to scale our data using standard scaler
"""

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = pd.DataFrame(scaler.fit_transform(X),index=X.index, columns = X.columns)

X

"""## Splitting our data into Train and Test"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7, shuffle=True, random_state=1)

X_train

"""## logistic Regression

# 7. Create a machine learning model to classify the stars using any classification algorithm.
# 8. Create 2 models using different algorithms and compare the results.
# 9. Plot the confusion matrix and print the classification report.

## I have trained here two models - **Logistic Regression model** and **Decision Tree Classifier model** with **5-fold cross validation**

**Reason for choosing Logistic Regression:** Since our task here is to predict
simple class labels using using given data, a regression based classifier would be a simple and computationally efficient algorithm.


**Reason for choosing Decision Tree Classifier:** decison trees are great at modelling non-linear relationships between features and the target variable due to which their ability of  finding patterns is really good.


**Reason for cross validation:** Since the size of our data is really small, splitting it between train and test only decreased the size of our data for the model to train on.This can cause our models to have high bias. Using 5 fold cv can help deal with this issue.
"""

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import  KFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, classification_report,ConfusionMatrixDisplay

# Logistic Regression
logistic_model = LogisticRegression()
logistic_model.fit(X_train, y_train)
logistic_scores = cross_val_score(logistic_model, X_train, y_train, cv=5)
for i, score in enumerate(logistic_scores):
    print("Model {}: {:.2f}%".format(i+1, score * 100))
print("Mean: {:.2f}%".format(logistic_scores.mean() * 100))

"""## Confusion Matrix and Classification Report for Logistic Regression"""

y_pred_logistic = logistic_model.predict(X_test)
print(confusion_matrix(y_test, y_pred_logistic))
print(classification_report(y_test, y_pred_logistic))

cm = confusion_matrix(y_test, -y_pred_logistic, labels=logistic_model.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test, y_pred_logistic),
                              display_labels=logistic_model.classes_)
disp.plot(cmap='summer', values_format='d')
plt.title('Logistic Regression Confusion Matrix')

plt.show()

# Decision Tree Classifier
decision_tree_model = DecisionTreeClassifier()
decision_tree_model.fit(X_train, y_train)
decision_tree_scores = cross_val_score(decision_tree_model, X_train, y_train, cv=5)
for i, score in enumerate(decision_tree_scores):
    print("Model {}: {:.2f}%".format(i+1, score * 100))
print("Mean: {:.2f}%".format(decision_tree_scores.mean() * 100))

"""## Confusion Matrix and Classification Report for Decision Tree"""

y_pred_tree = decision_tree_model.predict(X_test)
print(confusion_matrix(y_test, y_pred_tree))
print(classification_report(y_test, y_pred_tree))

disp = ConfusionMatrixDisplay(confusion_matrix=confusion_matrix(y_test, y_pred_tree),
                              display_labels=logistic_model.classes_)
disp.plot(cmap='summer', values_format='d')
plt.title('Decision Tree Confusion Matrix')

plt.show()

"""### The generated decision tree"""

from sklearn import tree
tree.plot_tree(decision_tree_model ,
               filled = True);

"""# 10. Mention your inferences and findings.

The modelled acuracy for Logistic Regression model with 5 fold CV -

Model 1: 97.06%

Model 2: 94.12%

Model 3: 91.18%

Model 4: 96.97%

Model 5: 93.94%

Mean: 94.65%
"""

accuracies = [97.06, 94.12, 91.18, 96.97, 93.94]
models = ['Model 1', 'Model 2', 'Model 3', 'Model 4', 'Model 5']
mean_accuracy = 94.65

# Plot the bar graph
plt.figure(figsize=(8, 6))
plt.bar(models, accuracies, color='skyblue', alpha=0.7)
plt.axhline(y=mean_accuracy, color='red', linestyle='dashed', label='Mean Accuracy')
plt.xlabel('Model')
plt.ylabel('Accuracy (%)')
plt.title('Model Accuracies for Logistic Regression')
plt.ylim(90, 105)
plt.legend()
plt.grid(True)
plt.show()

"""For Decision Tree Classifier

Model 1: 97.06%

Model 2: 100.00%

Model 3: 97.06%

Model 4: 96.97%

Model 5: 100.00%

Mean: 98.22%
"""

accuracies = [97.06, 100.00, 97.06, 96.97, 100.00]
models = ['Model 1', 'Model 2', 'Model 3', 'Model 4', 'Model 5']
mean_accuracy = 98.22

# Plot the bar graph
plt.figure(figsize=(8, 6))
plt.bar(models, accuracies, color='skyblue', alpha=0.7)
plt.axhline(y=mean_accuracy, color='red', linestyle='dashed', label='Mean Accuracy')
plt.xlabel('Model')
plt.ylabel('Accuracy (%)')
plt.title('Model Accuracies for decison tree')
plt.ylim(90, 105)
plt.legend()
plt.grid(True)
plt.show()

"""The above results show us that the Decison Tree Classifier is more generalized that the logistic reg model"""

''')