import pandas as pd
import numpy as np
import joblib
import os
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split

# 1. Load the REAL dataset
df = pd.read_csv("Data/creditcard.csv")

# 2. Split features (V1-V28, Amount, Time) from the label (Class)
X = df.drop('Class', axis=1)
y = df['Class']

# 3. Train the Pro Brain
# We use 'scale_pos_weight' because fraud is so rare (492 vs 284,000)
model = XGBClassifier(scale_pos_weight=580) 
model.fit(X, y)

# 4. Save it
joblib.dump(model, "models/fraud_model.pkl")
print("✅ Real-world brain trained on 284k transactions!")


# 1. Setup
os.makedirs("models", exist_ok=True)
os.makedirs("Data", exist_ok=True)

print("🚀 Training the Pro-Level Shield...")

# 2. Generate "Smart" Synthetic Data 
# (In real life, replace this with your 280,000 row Kaggle CSV!)
X = np.random.randn(5000, 30) 
# Make fraud very rare (only 2% of cases) to mimic real life
y = np.random.choice([0, 1], size=5000, p=[0.98, 0.02]) 

# 3. Train XGBoost (High Performance)
# scale_pos_weight helps the AI find that 2% of fraud hidden in the 98%
model = XGBClassifier(n_estimators=100, max_depth=5, scale_pos_weight=40)
model.fit(X, y)

# 4. Save Assets
joblib.dump(model, "models/fraud_model.pkl")
df = pd.DataFrame(X, columns=[f'V{i}' for i in range(1, 29)] + ['Time', 'Amount'])
df['Class'] = y
df.to_csv("Data/creditcard.csv", index=False)

print("✅ Brain Created! Ready for Real-time action.")