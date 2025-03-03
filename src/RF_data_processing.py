import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("../data/marine_insurance_dataset.csv")

# Convert dates explicitly
df['last_inspection_date'] = pd.to_datetime(df['last_inspection_date'], format="%d-%m-%Y", errors='coerce')

# Calculate vessel age
df['vessel_age'] = (pd.to_datetime("today") - df['last_inspection_date']).dt.days / 365

# Fill missing values
df.fillna(df.median(numeric_only=True), inplace=True)

# Ensure risk_score is created
if 'risk_score' not in df.columns:
    df['risk_score'] = (
        df['piracy_risk'] + df['war_zone_risk'] + df['storm_risk_score'] +
        df['historical_piracy_incidents'] + df['historical_collision_incidents'] +
        df['safety_incidents_last_5yrs']
    )

# One-hot encoding for categorical columns
categorical_cols = ['vessel_type', 'engine_type', 'flag_state', 'operator_company', 'region']
df = pd.get_dummies(df, columns=categorical_cols)

# Define features (excluding target)
features = [col for col in df.columns if col != 'risk_score']
target = 'risk_score'

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest Classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train_scaled, y_train)

# Predict risk categories
y_pred = classifier.predict(X_test_scaled)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Classification Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# Save preprocessed data & predictions
df['predicted_risk_score'] = classifier.predict(scaler.transform(df[features]))
df.to_csv("../data/processed_data_with_risk_ml.csv", index=False)
print("\nUpdated dataset saved as 'processed_data_with_risk.csv'.")
