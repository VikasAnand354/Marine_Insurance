import pandas as pd

def categorize_risk(df):
    """Categorizes vessels into High, Medium, and Low risk based on risk score."""
    conditions = [
        (df['risk_score'] >= df['risk_score'].quantile(0.75)),  # Top 25% risk
        (df['risk_score'] >= df['risk_score'].quantile(0.25)) & (df['risk_score'] < df['risk_score'].quantile(0.75)),  # Middle 50%
        (df['risk_score'] < df['risk_score'].quantile(0.25))  # Bottom 25%
    ]
    
    categories = ['High', 'Medium', 'Low']
    df['new_risk_category'] = pd.cut(df['risk_score'], bins=[-float('inf'), df['risk_score'].quantile(0.25), df['risk_score'].quantile(0.75), float('inf')], labels=categories)
    return df

if __name__ == "__main__":
    file_path = "../data/processed_data.csv"
    df = pd.read_csv(file_path)
    df = categorize_risk(df)
    df.to_csv("../data/processed_data_with_risk.csv", index=False)
    print("Risk categorization completed and saved.")
