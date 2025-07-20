import logging
import azure.functions as func
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableServiceClient, UpdateMode
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Page hit function triggered.')

    account_name = "ofirgaash"
    account_key = os.environ["TABLE_ACCOUNT_KEY"]  # המפתח מתוך הגדרות הפונקציה

    credential = AzureNamedKeyCredential(account_name, account_key)
    table_service = TableServiceClient(
        endpoint=f"https://{account_name}.table.core.windows.net",
        credential=credential
    )
    table_name = "PageHits"
    partition_key = "HitCounter"
    row_key = "MainPage"

    try:
        table = table_service.get_table_client(table_name)
        try:
            entity = table.get_entity(partition_key, row_key)
            entity["Count"] += 1
        except:
            entity = {"PartitionKey": partition_key, "RowKey": row_key, "Count": 1}

        table.upsert_entity(entity, mode=UpdateMode.REPLACE)
        return func.HttpResponse(str(entity["Count"]), status_code=200)
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse("Internal Server Error", status_code=500)
