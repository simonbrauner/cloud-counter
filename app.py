from datetime import datetime, timedelta, timezone

from flask import Flask, redirect, render_template

from azure.data.tables import EntityProperty, TableClient, UpdateMode
from azure.storage.blob import BlobSasPermissions, BlobServiceClient, generate_blob_sas
from azure.identity import DefaultAzureCredential

TABLE_ENDPOINT = "https://cloudcounter.table.core.windows.net"
TABLE_NAME = "counter"
TABLE_PARTITION_KEY = "Global"
TABLE_ROW_KEY = "Counter"
TABLE_COUNT_KEY = "Count"

STORAGE_ACCOUNT_NAME = "cloudcounter"
BLOB_ENDPOINT = f"https://{STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
CONTAINER_NAME = "cloudcounter"
BLOB_NAME = "style.css"

app = Flask(__name__, static_folder=None)

credential = DefaultAzureCredential()

table_client = TableClient(endpoint=TABLE_ENDPOINT, table_name=TABLE_NAME, credential=credential)

blob_client = BlobServiceClient(account_url=BLOB_ENDPOINT, credential=credential)

@app.route("/")
def index():
    counter = table_client.get_entity(partition_key=TABLE_PARTITION_KEY, row_key=TABLE_ROW_KEY)
    count_property = counter[TABLE_COUNT_KEY]
    count = count_property.value + 1
    counter[TABLE_COUNT_KEY] = EntityProperty(value=count, edm_type=count_property.edm_type)
    table_client.update_entity(mode=UpdateMode.REPLACE, entity=counter)

    return render_template("index.html", count=count)

@app.route('/static/<path:filename>')
def static(filename):
    now = datetime.now(timezone.utc) - timedelta(minutes=5)
    expiry = datetime.now(timezone.utc) + timedelta(hours=1)

    user_delegation_key = blob_client.get_user_delegation_key(
        key_start_time=now,
        key_expiry_time=expiry
    )

    sas_token = generate_blob_sas(
        account_name=STORAGE_ACCOUNT_NAME,
        container_name=CONTAINER_NAME,
        blob_name=filename,
        user_delegation_key=user_delegation_key,
        permission=BlobSasPermissions(read=True),
        expiry=expiry
    )

    return redirect(f"{BLOB_ENDPOINT}/{CONTAINER_NAME}/{filename}?{sas_token}")
