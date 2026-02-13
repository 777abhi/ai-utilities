# Flaky Test Predictor

This project aims to predict and identify "flaky" tests in a software test suite using machine learning. Flaky tests are tests that exhibit inconsistent results (pass/fail) despite no changes in the code, often due to timing issues, concurrency problems, or environmental factors.

## Current Features & How It Works

The project consists of several key components that form its core feature set:

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

3.  **Test Duration Prediction (`src/models/predict_test_duration.py`)**:
    -   This utility leverages a **Random Forest Regressor** to predict the execution time of tests based on environmental factors (OS, Python version) and test identifiers.
    -   It helps in identifying tests that are taking longer than expected (potential regressions) and aids in scheduling.

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

3.  **Predict Test Duration**:
    Run the duration prediction script.

    ```bash
    python src/models/predict_test_duration.py
    ```
    This will train a regression model to predict test execution times and display a comparison of actual vs. predicted durations.

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

## Roadmap: Next 20 Incremental Features

Here is a prioritized list of 20 incremental features that can add significant value to the project:

### Data & Input Enhancements
1.  **Configurable Data Generation**: Add CLI arguments to `data-prep-training.py` to control the number of samples, failure rates, and specific test scenarios.
2.  **Real Data Ingestion**: Create an adapter to ingest real test results from standard formats like JUnit XML (`.xml`) or Cucumber JSON (`.json`) instead of synthetic data.
3.  **Time-Series Data Support**: Enhanced data generation to simulate test history over time (e.g., detecting consecutive failures).
4.  **Enriched Environment Features**: Add more granular environment metrics (e.g., CPU load, memory usage) to the data model.
5.  **Data Validation Schema**: Implement strict schema validation (using Pydantic or Marshmallow) for input JSON data to ensure consistency.

### Model & Analytics Improvements
6.  **Flakiness Probability Score**: Update the classifier to output a probability score (0-100%) for flakiness, rather than a binary Pass/Fail prediction.
7.  **Feature Importance Visualization**: Generate a report or plot showing which factors (OS, Time, Changeset) contribute most to test flakiness.
8.  **Model Serialization**: Save trained models to disk (`.pkl` or `.joblib`) to allow for inference without retraining every time.
9.  **XGBoost Integration**: Add an option to switch between Random Forest and XGBoost for potentially better accuracy on structured data.
10. **Test Duration Outlier Detection**: Implement a statistical method (e.g., Z-score) to automatically flag duration outliers even if the test passes.
11. **Historical Trend Analysis**: A script to track and visualize the flakiness rate of specific tests over the last N builds.
12. **Hyperparameter Tuning Script**: A dedicated script to run Grid Search or Random Search to find the optimal model parameters.

### Operational & DevOps
13. **Interactive CLI**: A command-line interface (using `typer` or `click`) for querying the model (e.g., `predict --test-id 123`).
14. **REST API Service**: A simple Flask or FastAPI application to serve predictions via HTTP endpoints.
15. **Docker Containerization**: Add a `Dockerfile` and `docker-compose.yml` to containerize the training and prediction environment.
16. **HTML Report Generation**: Generate a self-contained HTML dashboard summarizing flaky tests and duration stats.
17. **Slack/Email Notifications**: A utility to send alerts to a Slack channel or email when high-confidence flaky tests are detected.
18. **Pre-commit Hook**: A git hook script that warns developers if they are modifying tests known to be flaky.

### Code Quality & Infrastructure
19. **Unit Test Suite**: Add a proper unit test suite (`pytest`) for the data generator and model training functions.
20. **Configuration Management**: Move hardcoded values (like test names, base times) into a central `config.yaml` file for easier management.

---

# Business Outcomes

## Improved Software Quality

By identifying and addressing flaky tests, the project helps in improving the overall quality of the software. Flaky tests can cause intermittent failures that are difficult to diagnose and fix. By predicting and addressing these tests, the project helps in reducing the number of false positives and false negatives in the test suite.

## Faster Delivery Pipeline

By reducing the number of flaky tests, the project helps in speeding up the software delivery pipeline. Flaky tests can cause delays in the pipeline as developers spend time diagnosing and fixing intermittent failures. By addressing these tests, the project helps in reducing the time spent on debugging and fixing issues, leading to faster delivery of software.

## Increased Developer Productivity

By automating the identification and addressing of flaky tests, the project helps in increasing developer productivity. Developers can focus on writing new features and fixing real issues instead of spending time on diagnosing and fixing flaky tests. This leads to increased productivity and faster delivery of software.

## Optimized Resource Allocation

The **Test Duration Predictor** allows for better scheduling of test execution. By knowing the expected duration of tests, CI/CD pipelines can be optimized to run parallel jobs more efficiently, reducing idle time and cloud infrastructure costs.

## Proactive Anomaly Detection

By comparing predicted execution times with actual runtimes, the system can flag performance regressions or infrastructure issues (e.g., a test taking 3x longer than usual) even if the test passes. This enables proactive maintenance before these issues cause timeout failures.

# Potential Use Cases

## Continuous Integration (CI) Pipelines

The project can be integrated into CI pipelines to automatically identify and address flaky tests. This helps in ensuring that the CI pipeline runs smoothly without intermittent failures caused by flaky tests.

## Test Suite Maintenance

The project can be used to maintain the test suite by identifying and addressing flaky tests. This helps in keeping the test suite clean and reliable, leading to more accurate test results.

## Pre-release Testing

The project can be used in pre-release testing to identify and address flaky tests before releasing the software. This helps in ensuring that the software is of high quality and free from intermittent failures caused by flaky tests.
