from typing import Optional
from airflow.providers.google.cloud.secrets.secret_manager import CloudSecretManagerBackend
from airflow.secrets.metastore import MetastoreBackend
import logging

class HybridSecretManager(CloudSecretManagerBackend):
    """
    Custom Secret Manager backend that checks Airflow DB for variables and connections first.
    Falls back to Google Cloud Secret Manager if not found.
    """
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.metastore_backend = MetastoreBackend()

    def get_variable(self, key: str) -> Optional[str]:
        # Check Airflow DB for the variable first
        logging.info(f"Checking variable '{key}' from Airflow DB")
        var = self.metastore_backend.get_variable(key)
        if var is not None:
            return var

        # Fallback to GCP Secret Manager
        logging.info(f"Checking variable '{key}' from GCP Secret Manager")
        return super().get_variable(key)


    
    def get_conn_value(self, conn_id: str) -> str | None:
        # Check Airflow DB for the conn first
        logging.info(f"Checking conn '{conn_id}' from Airflow DB")
        conn = self.metastore_backend.get_connection(conn_id)
        if conn is not None:
            return conn.as_json() 

        # Fallback to GCP Secret Manager
        logging.info(f"Checking conn '{conn_id}' from GCP Secret Manager")
        return super().get_conn_value(conn_id)