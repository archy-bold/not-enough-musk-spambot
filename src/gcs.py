import json
from google.cloud import storage
from google.oauth2 import service_account

def get_gcs_client(creds: str) -> storage.Client:
    info = json.loads(creds)
    storage_credentials = service_account.Credentials.from_service_account_info(info)
    return storage.Client(credentials=storage_credentials)