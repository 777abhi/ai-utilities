import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tabulate import tabulate
import os
import datetime

def parse_execution_time(time_str):
    # Format usually: "H:MM:SS" or "D days, H:MM:SS"
    try:
        if 'day' in time_str:
            days_part, time_part = time_str.split(',')
            days = int(days_part.split()[0])
            time_part = time_part.strip()
        else:
            days = 0
            time_part = time_str

        h, m, s = map(int, time_part.split(':'))
        return days * 86400 + h * 3600 + m * 60 + s
    except Exception as e:
        print(f"Error parsing time '{time_str}': {e}")
        return 0

def load_data():
    data = []
    data_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'train'))

    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} not found.")
        return []

    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            with open(os.path.join(data_dir, filename)) as f:
                data.append(json.load(f))

    # Flatten list of lists
    return [item for sublist in data for item in sublist]

def main():
    print("Loading training data...")
    data = load_data()
    if not data:
        print("No data found. Please run 'src/utils/data-prep-training.py' first.")
        return

    df = pd.json_normalize(data)

    # Preprocessing
    print("Preprocessing data...")
    df['duration_seconds'] = df['execution_time'].apply(parse_execution_time)

    # Select features
    feature_cols = ['test_id', 'environment.os', 'environment.python_version']
    X = df[feature_cols]
    y = df['duration_seconds']

    # Encode categorical variables
    X = pd.get_dummies(X, columns=feature_cols)

    # Handle missing columns in test set if we were doing real inference,
    # but for this simple train/test split within script, it's fine.

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train model
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluate
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)

    print(f"\nModel Performance:")
    print(f"Mean Absolute Error: {mae:.2f} seconds")
    print(f"Root Mean Squared Error: {np.sqrt(mse):.2f} seconds")

    # Display sample predictions
    results_df = pd.DataFrame({
        'Actual (s)': y_test,
        'Predicted (s)': y_pred,
        'Difference (s)': y_test - y_pred
    })

    # Add back original features for display
    original_test_data = df.loc[y_test.index, feature_cols]
    display_df = results_df.join(original_test_data)

    # Reorder columns
    cols = feature_cols + ['Actual (s)', 'Predicted (s)', 'Difference (s)']
    display_df = display_df[cols]

    print("\nSample Predictions (Test Set):")
    print(tabulate(display_df.head(10), headers='keys', tablefmt='grid', floatfmt=".2f"))

    # Business Insight
    print("\nBusiness Value:")
    print("This utility leverages AI to predict test execution duration.")
    print("1. **Resource Optimization**: Better scheduling of parallel test jobs based on predicted duration.")
    print("2. **Anomaly Detection**: If 'Difference' is high, it flags potential performance regressions or environmental issues.")

if __name__ == "__main__":
    main()
