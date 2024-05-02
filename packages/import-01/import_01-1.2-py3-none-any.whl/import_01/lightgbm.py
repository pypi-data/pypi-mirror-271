print('''
import lightgbm as lgb
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

# Load dataset
iris = load_iris()
X = iris.data
y = iris.target

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define LightGBM classifier
lgb_classifier = lgb.LGBMClassifier()

# Define hyperparameters grid for tuning
param_grid = {
    'num_leaves': [20, 30, 40],
    'learning_rate': [0.05, 0.1, 0.2],
    'n_estimators': [50, 100, 150],
    'colsample_bytree': [0.6, 0.8, 1.0]
}

# Perform Grid Search Cross Validation for hyperparameter tuning
grid_search = GridSearchCV(estimator=lgb_classifier, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Get the best parameters
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

# Initialize LightGBM classifier with best parameters
best_lgb_classifier = lgb.LGBMClassifier(**best_params)

# Train the classifier with the best parameters
best_lgb_classifier.fit(X_train, y_train)

# Predict the labels for test set
y_pred = best_lgb_classifier.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


''')