import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os

# Load JSON data from multiple files
data = []
data_dir = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'train'))
for filename in os.listdir(data_dir):
    if filename.endswith('.json'):
        with open(os.path.join(data_dir, filename)) as f:
            data.append(json.load(f))

# Flatten the list of dictionaries
data = [item for sublist in data for item in sublist]

# Preprocess data
df = pd.json_normalize(data)
df['result'] = df['result'].apply(lambda x: 1 if x == 'Pass' else 0)

# Extract features and labels
features = df.drop(columns=['test_id', 'result', 'error_logs', 'stack_trace', 'changeset.commit_id', 'changeset.author', 'changeset.timestamp'])
labels = df['result']

# Convert categorical features to dummy variables
# Convert list columns to strings
for col in features.columns:
    if features[col].apply(lambda x: isinstance(x, list)).any():
        features[col] = features[col].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

features = pd.get_dummies(features)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Train a RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42, min_samples_leaf=1, max_features='sqrt')
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Identify and display flaky tests
flaky_tests = X_test[(y_test != y_pred)]
flaky_test_ids = df.loc[flaky_tests.index, 'test_id'].tolist()
print("Flaky tests:", flaky_test_ids)
