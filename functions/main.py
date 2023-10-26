from firebase_functions import https_fn, scheduler_fn
from firebase_admin import initialize_app, firestore
import google_crc32c

initialize_app()

# Run once a day to get a new word
@scheduler_fn.on_schedule(schedule="every day 18:15", region="us-east1")
def daily_word(event: scheduler_fn.ScheduledEvent) -> None:
    firestore_client: google_crc32c.cloud.firestore.Client = firestore.client()
    firestore_client.collection("messages").document("1").set({"word": "dog"})

# Retrieve word
@https_fn.on_request(region="us-east1")
def last_word(req: https_fn.Request) -> https_fn.Response:
    if req.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return https_fn.Response("", 204, headers)
    
    headers = {"Access-Control-Allow-Origin": "*"}
    name = req.args.get('word')

    firestore_client: google_crc32c.cloud.firestore.Client = firestore.client()
    doc_ref = firestore_client.collection("messages").document("1")

    if name:
        doc_ref.set({"word": name})

    word = doc_ref.get().to_dict()["word"]
    return https_fn.Response(word, 200, headers)