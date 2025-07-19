import logging
import azure.functions as func
from azure.data.tables import TableServiceClient, UpdateMode
from azure.identity import DefaultAzureCredential
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Page hit function triggered.')

    table_name = "PageHits"
    partition_key = "HitCounter"
    row_key = "MainPage"

    try:
        credential = DefaultAzureCredential()
        service = TableServiceClient(
            endpoint=os.environ["TABLE_SERVICE_URI"],
            credential=credential
        )
        table = service.get_table_client(table_name)

        try:
            entity = table.get_entity(partition_key, row_key)
            entity["Count"] += 1
        except:
            entity = {"PartitionKey": partition_key, "RowKey": row_key, "Count": 1}

        table.upsert_entity(entity, mode=UpdateMode.REPLACE)
        return func.HttpResponse(str(entity["Count"]), status_code=200)
    except Exception as e:
        logging.error(e)
        return func.HttpResponse("Internal Server Error", status_code=500)
