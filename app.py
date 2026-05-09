from flask import Flask, render_template

from azure.data.tables import EntityProperty, TableClient, UpdateMode
from azure.identity import DefaultAzureCredential

TABLE_ENDPOINT = "https://cloudcounter.table.core.windows.net"
TABLE_NAME = "counter"
TABLE_PARTITION_KEY = "Global"
TABLE_ROW_KEY = "Counter"
TABLE_COUNT_KEY = "Count"

app = Flask(__name__)

credential = DefaultAzureCredential()

table_client = TableClient(endpoint=TABLE_ENDPOINT, table_name=TABLE_NAME, credential=credential)

@app.route("/")
def index():
    counter = table_client.get_entity(partition_key=TABLE_PARTITION_KEY, row_key=TABLE_ROW_KEY)
    count_property = counter[TABLE_COUNT_KEY]
    count = count_property.value + 1
    counter[TABLE_COUNT_KEY] = EntityProperty(value=count, edm_type=count_property.edm_type)
    table_client.update_entity(mode=UpdateMode.REPLACE, entity=counter)

    return render_template("index.html", count=count)
