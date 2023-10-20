from firebase_functions import https_fn
from firebase_admin import initialize_app

initialize_app()

@https_fn.on_request()
def on_request_example(req: https_fn.Request) -> https_fn.Response:
    if req.method == "OPTIONS":
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }
        return https_fn.Response("", 204, headers)
    
    headers = {"Access-Control-Allow-Origin": "*"}
    name = req.args.get('name')
    if not name:
        name = 'World'

    return https_fn.Response("Hello " + name + "!", 200, headers)