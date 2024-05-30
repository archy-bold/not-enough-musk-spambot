import json
from google.cloud import storage
from google.oauth2 import service_account

client: storage.Client = None

def get_gcs_client(creds: str) -> storage.Client:
    global client
    if client is None:
        info = json.loads(creds)
        storage_credentials = service_account.Credentials.from_service_account_info(info)
        client = storage.Client(credentials=storage_credentials)
    return client

def download_db_file_from_gcs(gcs_bucket: str, gcs_key: str, dir: str, db_name: str) -> None:
    if gcs_bucket is not None and gcs_key is not None:
        gcs_client = get_gcs_client(gcs_key)
        gcs_client.bucket(gcs_bucket).get_blob(db_name).download_to_filename(dir + '/' + db_name)
        print("Downloaded gs://" + gcs_bucket + "/" + db_name + " from GCS")

def upload_db_file_to_gcs(gcs_bucket: str, gcs_key: str, dir: str, db_name: str) -> None:
    if gcs_bucket is not None and gcs_key is not None:
        gcs_client = get_gcs_client(gcs_key)
        gcs_client.bucket(gcs_bucket).blob(db_name).upload_from_filename(dir + '/' + db_name)
        print("Uploaded " + db_name + " to GCS gs://" + gcs_bucket)
