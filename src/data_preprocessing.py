import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler

def load_data(file_path):
    """Loads the dataset from a CSV file."""
    return pd.read_csv(file_path)

def clean_data(df):
    """Handles missing values and converts date columns."""
    df['last_claim_date'] = pd.to_datetime(df['last_claim_date'], errors='coerce')
    df['last_inspection_date'] = pd.to_datetime(df['last_inspection_date'], errors='coerce').fillna(pd.to_datetime('2000-01-01'))
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    df.fillna(df.median(numeric_only=True), inplace=True)
    
    return df

def encode_categorical(df):
    """Encodes categorical variables using Label Encoding."""
    label_encoders = {}
    categorical_columns = [
        'vessel_type', 'engine_type', 'flag_state', 'operator_company', 
        'claim_reason', 'destination', 'port_of_departure', 'next_port', 
        'region', 'weather_condition'
    ]
    
    for col in categorical_columns:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
            label_encoders[col] = le
    
    return df, label_encoders

def scale_features(df, excluded_cols):
    """Scales numerical features using StandardScaler, excluding specified columns."""
    scaler = StandardScaler()
    numerical_cols = [col for col in df.select_dtypes(include=['float64', 'int64']).columns if col not in excluded_cols]
    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    return df, scaler

def create_risk_score(df):
    """Creates an improved risk score based on piracy, war, storms, inspections, and vessel age."""
    df['vessel_age'] = (pd.to_datetime('today') - df['last_inspection_date']).dt.days / 365

    df['risk_score'] = (
        (df['piracy_risk'] * 2.0) +  
        (df['war_zone_risk'] * 2.0) +  
        (df['storm_risk_score'] * 1.5) +  
        (df['historical_piracy_incidents'] * 1.2) +   
        (df['vessel_age'] * 0.5) +  
        (df['weather_condition'] * 1.2)  
    )
    
    return df

def normalize_risk_score(df):
    """Scales the risk score between 0 and 100."""
    scaler = MinMaxScaler(feature_range=(0, 100))
    df[['risk_score']] = scaler.fit_transform(df[['risk_score']])
    return df

def preprocess_data(file_path):
    """Main function to preprocess the dataset."""
    df = load_data(file_path)
    df = clean_data(df)
    df, label_encoders = encode_categorical(df)

    excluded_cols = ['vessel_name', 'vessel_type', 'engine_type', 'flag_state', 
                     'operator_company', 'claim_reason', 'destination', 'port_of_departure', 
                     'next_port', 'region', 'weather_condition', 'latitude', 'longitude']

    df, scaler = scale_features(df, excluded_cols)
    df = create_risk_score(df)
    df = normalize_risk_score(df)
    
    return df, label_encoders, scaler

if __name__ == "__main__":
    file_path = "../data/marine_insurance_dataset.csv"
    processed_df, label_encoders, scaler = preprocess_data(file_path)
    processed_df.to_csv("../data/processed_data.csv", index=False)
    print("Data preprocessing completed.")
