# Custom HybridSecretManager for Cloud Composer

This repository contains a custom Secret Manager backend for Google Cloud Composer. The backend first checks the Airflow database for variables and connections. If a secret is not found in the Airflow database, it falls back to Google Cloud Secret Manager.

## Prerequisites

- Python 3.x installed on your machine.
- Access to a Google Cloud Project with permissions to use Google Cloud Secret Manager and Artifact Registry.
- Cloud Composer environment.

## Setup Instructions

Follow these steps to set up and deploy the `HybridSecretManager`.

```bash
# Step 1: Create a Python Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

# Step 2: Install Required Dependencies
pip install apache-airflow[gcp]
pip install setuptools

# Step 3: Configure Google Artifact Registry (replace pypi with your registry name)
gcloud config set artifacts/repository pypi
gcloud config set artifacts/location northamerica-northeast1

# Step 4: Prepare the Package
python setup.py sdist bdist_wheel

# Step 5: Upload the Package to Google Artifact Registry
# Replace `democentral` with your GCP project ID.
python3 -m twine upload --repository-url https://northamerica-northeast1-python.pkg.dev/democentral/pypi/ dist/*

# Step 6: Deploy the Package to Cloud Composer
# Add the package to your Cloud Composer environment via the Airflow web server or using the GCP Console.
# Ensure the environment variables or necessary configurations for the Secret Manager are set.

# Step 7: Update Airflow Configuration
# Update the `airflow.cfg` file or use environment variables to set the custom secret backend:
# [secrets]
# backend = your_project.HybridSecretManager
# backend_kwargs = {"key_path": "path/to/credentials.json"}

# Step 8: Test the Custom Secret Manager
# Deploy an Airflow DAG that retrieves secrets to validate the integration.

# Additional Notes:
# - Ensure the service account running Cloud Composer has the necessary permissions for Google Cloud Secret Manager.
# - Verify the fallback behavior by storing some secrets in Airflow and others in Google Cloud Secret Manager.
