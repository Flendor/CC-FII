import logging

import azure.functions as func
from pymongo import MongoClient
from azure.storage.blob import BlockBlobService


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    mongo_uri = ""
    client = MongoClient(mongo_uri)
    db = client['']
    user_collection = db['']
    photos_collection = db['']

    blob_service = BlockBlobService(account_name="", account_key="")

    username = req.params.get('username')
    if not username:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            username = req_body.get('username')

    if username:
        try:
            user_collection.delete_one({"username": username})
            all_blobs = blob_service.list_blobs("photos")
            for blob in all_blobs:
                if blob.name.startswith(username):
                    blob_service.delete_blob("photos", blob.name)
            photos_collection.delete_many({"user": username})
        except Exception as e:
            print(e)
        return func.HttpResponse(
            f"Hello, {username}. Your account has been deleted successfully.", 
            status_code=200
        )
    else:
        return func.HttpResponse(
             "A problem occured while retrieving your username!", 
             status_code=400
        )
