provider "google" {
  project = "wiiq-proj"
  zone    = "us-east1"
  region = "us-east1"
}

resource "google_storage_bucket" "func-bucket" {
  name     = "wiiq-cloud-functions"
  location = "us-east1"
}

# Upload all files to bucket
resource "google_storage_bucket_object" "functions_archive" {
  name   = "functions.zip"
  source = "../functions.zip"
  bucket = google_storage_bucket.func-bucket.id
}

resource "google_cloudfunctions_function" "function" {
  name        = "retrieve-daily-word"
  description = "retrieves word"

  runtime               = "python311"
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.func-bucket.name
  source_archive_object = google_storage_bucket_object.functions_archive.name
  timeout               = 60
  entry_point           = "last_word"
}

# IAM entry for a single user to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"

}