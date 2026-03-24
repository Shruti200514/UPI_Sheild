import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Load dataset
df = pd.read_csv("Data/creditcard.csv")

X = df.drop("Class", axis=1)
y = df["Class"]

# Stratify is crucial for imbalanced fraud data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Create a Pipeline: This bundles scaling + model into one object
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=500, # Handles imbalance
        random_state=42
    ))
])

# Train the entire pipeline
pipeline.fit(X_train, y_train)

# Quick Evaluation
y_pred = pipeline.predict(X_test)
print(f"ROC-AUC Score: {roc_auc_score(y_test, pipeline.predict_proba(X_test)[:, 1])}")
print(classification_report(y_test, y_pred))

# Save the entire pipeline (no need to save scaler separately!)
joblib.dump(pipeline, "models/fraud_model.pkl")
print("Pipeline saved successfully!")