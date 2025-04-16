import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np

def run_training():
    # Load the dataset
    data = pd.read_excel('Dataset Global Fashion Brands Brand Equity Ranking Growth Rate  COO ROO 2001-2021.xlsx')

    # Fill missing values
    data.fillna(0, inplace=True)

    # Convert relevant columns to numeric
    numeric_columns = data.columns[5:]  # Assuming the first five columns are non-numeric
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors='coerce')

    # Prepare data for training
    features = ['Rank2001', 'Rank2002', 'Equity2001', 'GrowthRate2001', 
                'GrowthRate2002', 'GrowthRate2003', 'GrowthRate2004']
    target = 'Equity2021'

    # Prepare the data
    X = data[features]
    y = data[target]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    return model, data  # returning both the model and the data

def predict_future_equity(brand_data, future_years):
    future_equities = []
    current_equity = brand_data['Equity2021']

    for year in future_years:
        growth_rate = brand_data[f'GrowthRate{year - 2001}'] if year - 2001 in range(1, 21) else 0
        current_equity *= (1 + growth_rate)  # Update equity based on growth rate
        future_equities.append(current_equity)

    return future_equities

# You can still test it standalone
if __name__ == "__main__":
    model, data = run_training()
    print("Model trained successfully!")