"""Train the diabetes decision tree and save model + preprocessing artifacts."""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv('diabetes_prediction_dataset.csv')
df_model = pd.get_dummies(df, columns=['gender', 'smoking_history'], drop_first=True)

X = df_model.drop('diabetes', axis=1)
y = df_model['diabetes']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

dt = DecisionTreeClassifier(class_weight='balanced', random_state=42)
dt.fit(X_train, y_train)

import joblib
joblib.dump(dt, 'model/diabetes_tree.joblib')
joblib.dump(list(X.columns), 'model/feature_names.json')

print('train acc:', dt.score(X_train, y_train))
print('test acc :', dt.score(X_test, y_test))
