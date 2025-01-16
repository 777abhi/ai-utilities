import json
import random
import uuid
from datetime import datetime, timedelta
import os

def generate_random_data():
    data = []
    test_names = ["001_Login Test", "002_Signup Test", "003_Profile Update Test", "004_Password Reset Test", "005_Logout Test"]
    # test_names = ["002_Signup Test"]

    for test_name in test_names:
        test_data = {
            "test_id": test_name,
            #"result": random.choice(["Pass", "Fail"]),
            "result": random.choice(["Pass"]),
            "execution_time": str(timedelta(seconds=random.randint(1, 3600))),
            "error_logs": "Error log example" if random.choice([True, False]) else "",
            "stack_trace": "Stack trace example" if random.choice([True, False]) else "",
            "environment": {
                "os": random.choice(["Windows", "Linux", "macOS"]),
                "python_version": random.choice(["3.6", "3.7", "3.8", "3.9"]),
                "dependencies": ["dependency1", "dependency2"]
            },
            "configuration": {
                "config1": "value1",
                "config2": "value2"
            },
            "changeset": {
                "commit_id": str(uuid.uuid4()),
                "author": "Author Name",
                "timestamp": str(datetime.now() - timedelta(days=random.randint(0, 30)))
            }
        }
        data.append(test_data)
    return data

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    data = generate_random_data()
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'train')
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = os.path.join(output_dir, f'training_data_{timestamp}.json')

    save_to_json(data, output_file)
    print("Generated random test results entries and saved to : ", output_file)