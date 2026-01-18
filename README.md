# Flaky Test Predictor

This project aims to predict and identify "flaky" tests in a software test suite using machine learning. Flaky tests are tests that exhibit inconsistent results (pass/fail) despite no changes in the code, often due to timing issues, concurrency problems, or environmental factors.

## How It Works

The project consists of two main components:

1.  **Data Generation (`src/utils/data-prep-training.py`)**:
    -   This script generates synthetic test execution data to simulate a real-world testing environment.
    -   It creates JSON files containing test results, execution times, error logs, stack traces, and environment details.
    -   The data is saved in `src/data/train/` for training the model.

2.  **Model Training & Prediction (`src/models/train_and_predict_model.py`)**:
    -   This script loads the generated training data.
    -   It preprocesses the data by flattening the JSON structure, converting lists to strings, and creating dummy variables for categorical features.
    -   A **Random Forest Classifier** is trained on the data to predict the test result (Pass/Fail).
    -   The model is evaluated on a test set.
    -   **Flaky Identification**: Tests where the model's prediction differs from the actual result in the test set are flagged as "flaky". This approach assumes that if a test's outcome is hard to predict based on its features, it might be unstable or flaky.

## Getting Started

### Prerequisites

-   Python 3.x
-   pip

### Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Usage

1.  **Generate Training Data**:
    Run the data preparation script to generate synthetic test data.

    ```bash
    python src/utils/data-prep-training.py
    ```
    This will create JSON files in the `src/data/train/` directory.

2.  **Train Model and Predict**:
    Run the model training script.

    ```bash
    python src/models/train_and_predict_model.py
    ```
    This will train the Random Forest model, output the classification report, and list the IDs of identified flaky tests.

## Project Structure

-   `src/data/`: Contains the training data (JSON files).
-   `src/models/`: Contains the machine learning model script (`train_and_predict_model.py`).
-   `src/utils/`: Contains utility scripts like the data generator (`data-prep-training.py`).

## Future Improvements

Here are some suggested incremental features and improvements for the project:

-   **Enhanced Feature Engineering**:
    -   Use **Natural Language Processing (NLP)** techniques (e.g., TF-IDF, Word2Vec, BERT) to extract meaningful features from `error_logs` and `stack_trace` instead of dropping them.
    -   Extract features from `changeset` information to correlate code changes with flakiness.
-   **Advanced Modeling**:
    -   Experiment with other algorithms like **Gradient Boosting (XGBoost, LightGBM)** or **Neural Networks** to improve prediction accuracy.
    -   Perform **Hyperparameter Tuning** (e.g., using GridSearchCV) to optimize the Random Forest model.
-   **Real-world Data Integration**:
    -   Modify the data loader to ingest real test results from CI/CD tools (e.g., Jenkins, GitHub Actions) instead of using synthetic data.
-   **Better Flaky Definition**:
    -   Implement a more robust definition of flakiness by analyzing historical data for the *same* commit to check for result toggling, rather than relying solely on misclassification.
-   **Visualization & Reporting**:
    -   Generate confusion matrices, feature importance plots, and trend analysis graphs to visualize the model's performance and flaky test trends.
-   **API / CLI**:
    -   Expose the model via a REST API (using Flask or FastAPI) or improve the CLI to accept arguments for input files, model parameters, and output paths.

---

# Business Outcomes

## Improved Software Quality

By identifying and addressing flaky tests, the project helps in improving the overall quality of the software. Flaky tests can cause intermittent failures that are difficult to diagnose and fix. By predicting and addressing these tests, the project helps in reducing the number of false positives and false negatives in the test suite.

## Faster Delivery Pipeline

By reducing the number of flaky tests, the project helps in speeding up the software delivery pipeline. Flaky tests can cause delays in the pipeline as developers spend time diagnosing and fixing intermittent failures. By addressing these tests, the project helps in reducing the time spent on debugging and fixing issues, leading to faster delivery of software.

## Increased Developer Productivity

By automating the identification and addressing of flaky tests, the project helps in increasing developer productivity. Developers can focus on writing new features and fixing real issues instead of spending time on diagnosing and fixing flaky tests. This leads to increased productivity and faster delivery of software.

# Potential Use Cases

## Continuous Integration (CI) Pipelines

The project can be integrated into CI pipelines to automatically identify and address flaky tests. This helps in ensuring that the CI pipeline runs smoothly without intermittent failures caused by flaky tests.

## Test Suite Maintenance

The project can be used to maintain the test suite by identifying and addressing flaky tests. This helps in keeping the test suite clean and reliable, leading to more accurate test results.

## Pre-release Testing

The project can be used in pre-release testing to identify and address flaky tests before releasing the software. This helps in ensuring that the software is of high quality and free from intermittent failures caused by flaky tests.
