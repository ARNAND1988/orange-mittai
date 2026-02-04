# services/gcs.py
import os
import uuid
from fastapi import UploadFile
import logging
from urllib.parse import urlparse


logger = logging.getLogger(__name__)
APP_ENV = os.getenv("APP_ENV", "local")

# Only import GCS in cloud
if APP_ENV == "cloud":
    from google.cloud import storage

BUCKET_NAME = "orange-mittai-store"
CDN_BASE_URL = os.getenv("CDN_BASE_URL", "http://localhost:8000")

# Local mock storage directory
LOCAL_PRODUCTS_DIR = "/tmp/products"


def upload_product_image(file: UploadFile) -> str:
    """
    Uploads image to GCS in cloud
    Saves image locally in local env
    """

    if APP_ENV == "local":
        return mock_upload(file)

    return gcs_upload(file)


# =========================
# MOCK UPLOAD (LOCAL ONLY)
# =========================
def mock_upload(file: UploadFile) -> str:
    """
    Saves image to local filesystem and returns local URL
    """

    os.makedirs(LOCAL_PRODUCTS_DIR, exist_ok=True)
    logger.info("Mock upload started")
    logger.debug("Filename: %s", file.filename)
    ext = file.filename.split(".")[-1]
    filename = f"mock-{uuid.uuid4()}.{ext}"
    file_path = os.path.join(LOCAL_PRODUCTS_DIR, filename)

    # Save file locally
    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # Return URL that FastAPI can serve
    return f"{CDN_BASE_URL}/products/{filename}"


# =========================
# REAL GCS UPLOAD (CLOUD)
# =========================
def gcs_upload(file: UploadFile) -> str:
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    ext = file.filename.split(".")[-1]
    object_path = f"products/{uuid.uuid4()}.{ext}"

    blob = bucket.blob(object_path)
    blob.cache_control = "public, max-age=31536000, immutable"

    blob.upload_from_file(
        file.file,
        content_type=file.content_type
    )

    return f"{CDN_BASE_URL}/{object_path}"

def delete_product_image(image_url: str):
    """
    Deletes product image from local storage or GCS
    """
    if not image_url:
        return

    try:
        if APP_ENV == "local":
            delete_local_image(image_url)
        else:
            delete_gcs_image(image_url)
    except Exception as e:
        logger.warning("Failed to delete image %s: %s", image_url, e)

def delete_local_image(image_url: str):
    """
    Deletes locally stored image based on URL
    """
    parsed = urlparse(image_url)
    filename = os.path.basename(parsed.path)

    file_path = os.path.join(LOCAL_PRODUCTS_DIR, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Deleted local image: %s", file_path)

def delete_gcs_image(image_url: str):
    """
    Deletes image from GCS using its CDN URL
    """
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    # CDN_BASE_URL/products/uuid.jpg → products/uuid.jpg
    object_path = image_url.replace(f"{CDN_BASE_URL}/", "")

    blob = bucket.blob(object_path)

    if blob.exists():
        blob.delete()
        logger.info("Deleted GCS image: %s", object_path)
