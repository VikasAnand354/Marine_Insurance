import pandas as pd

# Load the dataset
file_path = "../data/marine_insurance_dataset.csv"
df = pd.read_csv(file_path)

# Checking summary statistics for risk-related factors grouped by risk_category
risk_factors = ['piracy_risk', 'war_zone_risk', 'storm_risk_score', 'historical_piracy_incidents']
print(df.groupby('risk_category')[risk_factors].mean())
