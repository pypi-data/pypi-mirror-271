print('''import sweetviz as sv
my_report = sv.analyze(my_dataframe)
my_report.show_html()

#plots
import matplotlib.pyplot as plt
import seaborn as sns
col = ['id', 'MonsoonIntensity', 'TopographyDrainage', 'RiverManagement',
       'Deforestation', 'Urbanization', 'ClimateChange', 'DamsQuality',
       'Siltation', 'AgriculturalPractices', 'Encroachments',
       'IneffectiveDisasterPreparedness', 'DrainageSystems',
       'CoastalVulnerability', 'Landslides', 'Watersheds',
       'DeterioratingInfrastructure', 'PopulationScore', 'WetlandLoss',
       'InadequatePlanning', 'PoliticalFactors', 'FloodProbability']
fig, axes = plt.subplots(11,2, figsize = (30, 30))
axes = axes.flatten()
for i , column in enumerate(col):
    sns.histplot(data = df , x = column, kde = True , ax = axes[i])



from sklearn.model_selection import GridSearchCV
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.05, 0.1]
}

grid_search = GridSearchCV(estimator=model, param_grid=param_grid, scoring='neg_mean_squared_error', cv=3, verbose=2)



grid_search.fit(X_train, y_train)

# Get the best parameters and best score
best_params = grid_search.best_params_
best_score = grid_search.best_score_

# Evaluate the best model on the test set
best_model = grid_search.best_estimator_
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)



from sklearn.metrics import r2_score
r2_score(y_test , y_pred)


def onehot_encode(df, column, prefix):
    df = df.copy()
    dummies = pd.get_dummies(df[column], prefix=prefix)
    df = pd.concat([df, dummies], axis=1)
    df = df.drop(column, axis=1)
    return df

df_new = onehot_encode(df_new, column='Star color', prefix="Color")
df_new = onehot_encode(df_new, column='Spectral Class', prefix="Class")



from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = pd.DataFrame(scaler.fit_transform(X),index=X.index, columns = X.columns)


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
print("Mean: {:.2f}%".format(logistic_scores.mean() * 100))''')