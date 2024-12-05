from setuptools import setup, find_packages

setup(
    name="hybrid-secret-manager",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "apache-airflow",
        "google-cloud-secret-manager",
    ],
    description="Custom Airflow secrets backend for Google Secret Manager",
    author="Your Name",
    author_email="your.email@example.com",
)
