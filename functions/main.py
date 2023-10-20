from firebase_functions import https_fn
from firebase_admin import initialize_app, firestore
import google_crc32c

initialize_app()

@https_fn.on_request()
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