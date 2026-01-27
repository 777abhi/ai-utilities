import json
import random
import uuid
from datetime import datetime, timedelta
import os

def generate_random_data():
    data = []
    test_names = ["001_Login Test", "002_Signup Test", "003_Profile Update Test", "004_Password Reset Test", "005_Logout Test"]
    # test_names = ["002_Signup Test"]

    base_times = {
        "001_Login Test": 120,
        "002_Signup Test": 300,
        "003_Profile Update Test": 200,
        "004_Password Reset Test": 150,
        "005_Logout Test": 50
    }

    # Generate more data for better training
    for _ in range(50):
        for test_name in test_names:
            os_name = random.choice(["Windows", "Linux", "macOS"])

            # Calculate execution time with some patterns:
            # 1. Base time depends on test name
            # 2. OS multiplier (Windows slower)
            # 3. Random noise
            base_time = base_times.get(test_name, 100)
            os_multiplier = {"Windows": 1.5, "macOS": 1.2, "Linux": 1.0}.get(os_name, 1.0)
            noise = random.uniform(0.9, 1.1)
            duration_seconds = int(base_time * os_multiplier * noise)

            test_data = {
                "test_id": test_name,
                #"result": random.choice(["Pass", "Fail"]),
                "result": random.choice(["Pass"]),
                "execution_time": str(timedelta(seconds=duration_seconds)),
                "error_logs": "Error log example" if random.choice([True, False]) else "",
                "stack_trace": "Stack trace example" if random.choice([True, False]) else "",
                "environment": {
                    "os": os_name,
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