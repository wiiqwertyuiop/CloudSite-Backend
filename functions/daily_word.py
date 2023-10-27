from firebase_functions import scheduler_fn
from firebase_admin import initialize_app, firestore
import google_crc32c
from random_word import RandomWords

initialize_app()

# Run once a day to get a new word
@scheduler_fn.on_schedule(schedule="every day 04:00", region="us-east1")
def daily_word(event: scheduler_fn.ScheduledEvent) -> None:
    r = RandomWords()
    firestore_client: google_crc32c.cloud.firestore.Client = firestore.client()
    firestore_client.collection("messages").document("1").set({"word": r.get_random_word()})
