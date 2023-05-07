from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import os

endpoint = os.environ.get('JUNI_VISION_ENDPOINT')
key = os.environ.get('JUNI_VISION_KEY')

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

def see_receipt(url): 
    poller = document_analysis_client.begin_analyze_document_from_url("prebuilt-receipt", url)
    receipts = poller.result()

    if len(receipts.documents) != 1:
        return None
    
    result = ''
    receipt = receipts.documents[0]

    merchant_name = receipt.fields.get("MerchantName")
    if merchant_name:
        result += 'MERCHANT_NAME: ' + merchant_name.value + '\n'

    transaction_date = receipt.fields.get("TransactionDate")
    if transaction_date:
        result += 'TRANSACTION_DATE: ' + transaction_date.value.strftime("%Y-%m-%d") + '\n'

    transaction_time = receipt.fields.get("TransactionTime")
    if transaction_date:
        result += 'TRANSACTION_TIME: ' + transaction_time.value.strftime("%H:%M:%S") + '\n'

    total = receipt.fields.get("Total")
    if total:
        result += 'TOTAL: ' + str(total.value) + '\n'

    result += '---ITEMS---\n'

    if receipt.fields.get("Items"):
        for _, raw_item in enumerate(receipt.fields.get("Items").value):
            item = ''
            
            item_description = raw_item.value.get("Description")
            if item_description:
                item += 'DESCRIPTION: ' + item_description.value + ';'

            item_quantity = raw_item.value.get("Quantity")
            if item_quantity:
                item += 'QUANTITY: ' + str(item_quantity.value) + ';'

            item_price = raw_item.value.get("Price")
            if item_price:
                item += 'PRICE: ' + str(item_price.value) + ';'

            item_total_price = raw_item.value.get("TotalPrice")
            if item_total_price:
                item += 'TOTAL: ' + str(item_total_price.value) + ';'

            result += item + '\n'

    return result