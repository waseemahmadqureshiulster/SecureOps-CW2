import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
import argparse
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, classification_report

def main():
    # 1. Enable MLflow Autologging
    mlflow.sklearn.autolog()

    # 2. Load Data
    print("Loading data...")
    df = pd.read_csv("data/CIDDS-001-external-week1.csv")
    
    # 3. Preprocessing (Simplified from your CW1)
    # Target variable mapping
    df['class'] = df['class'].apply(lambda x: 0 if x == 'normal' else 1) # 0=Normal, 1=Attacker
    
    # Select features based on your CW1
    feature_cols = ["Duration", "Packets", "Bytes", "Proto", "Flags"]
    target_col = "class"
    
    # Clean Bytes (remove 'M' and convert to float)
    df['Bytes'] = df['Bytes'].astype(str).str.replace(' M', '').astype(float) * 1e6
    
    X = df[feature_cols]
    y = df[target_col]

    # 4. Define Preprocessing Pipeline
    numeric_features = ["Duration", "Packets", "Bytes"]
    categorical_features = ["Proto", "Flags"]

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', MinMaxScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # 5. Define Model
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', RandomForestClassifier(n_estimators=50))])

    # 6. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 7. Train & Log
    with mlflow.start_run():
        print("Training model...")
        clf.fit(X_train, y_train)
        
        # Evaluate
        print("Evaluating model...")
        preds = clf.predict(X_test)
        acc = accuracy_score(y_test, preds)
        
        print(f"Accuracy: {acc}")
        mlflow.log_metric("accuracy", acc)
        
        # Register the model in MLflow
        mlflow.sklearn.log_model(clf, "model", registered_model_name="CIDDS_IDS_Model")

if __name__ == "__main__":
    main()