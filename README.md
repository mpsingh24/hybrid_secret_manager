# Custom HybridSecretManager for Cloud Composer

This repository contains a custom Secret Manager backend for Google Cloud Composer. It reverses the default Airflow order of first checking external Secret Manager and then Airflow DB for secrets. The backend first checks the Airflow database for variables and connections. If a secret is not found in the Airflow database, it falls back to Google Cloud Secret Manager.

```
Note: I am using a project name democentral and Artifact Registry named pypi. Please remember to update these with your project name and Artifact Registry name as you go through the steps.
```

## Prerequisites

- Python 3.x installed on your machine.
- Access to a Google Cloud Project with permissions to use Google Cloud Secret Manager and Artifact Registry.
- Cloud Composer environment.

## Setup Instructions

Follow these steps to set up and deploy the `HybridSecretManager`.


### Step 1: Create a Python Virtual Environment
```
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install Required Dependencies
```
pip install apache-airflow[gcp]
pip install wheel
pip install twine
pip install setuptools
pip install keyrings.google-artifactregistry-auth
```

### Step 3: Create Google Artifact Registry for Python Packages
#### Replace "pypi" with the name of your desired registry.
```
gcloud artifacts repositories create pypi \
    --repository-format=python \
    --location=northamerica-northeast1 \
    --description="Python package repository"
```

### Step 4: Configure Google Artifact Registry
#### Replace "pypi" with your registry name.
```
gcloud config set artifacts/repository pypi
gcloud config set artifacts/location northamerica-northeast1
```

### Step 5: Review the pip.conf file
####  Update `pip.conf` with your Python Package Repository and configure your composer environment to install from it. When using Artifact Registry repository, /simple/ should be appended to the repository URL
####  Upload this `pip.conf` file to the `/config/pip/` folder in your composer environment's bucket.

### Step 6: Prepare the Package
####  Ensure your `setup.py` file is correctly configured for your project.
```
python setup.py sdist bdist_wheel
```

### Step 7: Upload the Package to Google Artifact Registry
#### Replace "democentral" with your GCP project ID.
```
python3 -m twine upload --repository-url [https://northamerica-northeast1-python.pkg.dev/democentral/pypi/](https://northamerica-northeast1-python.pkg.dev/democentral/pypi/) dist/*
```

### Step 8: Deploy the Package to Cloud Composer
#### Add the package to your Cloud Composer environment via PYPI Packages tab.
#### Provide the following:
```
Package name: `hybrid-secret-manager`
Version: `==0.0.1`
```

### Step 9: Update Airflow Configuration
#### Use airflow configuration overrides to set the custom secret backend:
```
[secrets]
backend = hybrid_secret_manager.HybridSecretManager
backend_kwargs = {"project_id": "democentral", "connections_prefix":"airflow-connections", "variables_prefix":"airflow-variables", "sep":"-"}
```

### Step 10: Test the Custom Secret Manager
#### Deploy an Airflow DAG that retrieves secrets to validate the integration.