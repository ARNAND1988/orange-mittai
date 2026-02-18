import os
import uuid
import logging
from urllib.parse import urlparse
from fastapi import UploadFile

from app.config import (
    STORAGE_BACKEND,
    LOCAL_UPLOAD_DIR,
    BUCKET_NAME,
    CDN_BASE_URL,
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# Entry points (USED BY ROUTES / SERVICES)
# --------------------------------------------------

def upload_product_image(file: UploadFile) -> str:
    """
    Upload product image using configured storage backend
    """
    if STORAGE_BACKEND == "gcs":
        return _gcs_upload(file)

    return _local_upload(file)


def delete_product_image(image_url: str):
    """
    Delete product image from configured storage backend
    """
    if not image_url:
        return

    try:
        if STORAGE_BACKEND == "gcs":
            _delete_gcs_image(image_url)
        else:
            _delete_local_image(image_url)
    except Exception as e:
        logger.warning("Failed to delete image %s: %s", image_url, e)

# --------------------------------------------------
# LOCAL STORAGE (Raspberry Pi / Dev)
# --------------------------------------------------

def _local_upload(file: UploadFile) -> str:
    os.makedirs(LOCAL_UPLOAD_DIR, exist_ok=True)

    ext = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(LOCAL_UPLOAD_DIR, filename)

    logger.info("Local upload: %s", file_path)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    # served via StaticFiles
    return f"{CDN_BASE_URL}/products/{filename}"


def _delete_local_image(image_url: str):
    parsed = urlparse(image_url)
    filename = os.path.basename(parsed.path)

    file_path = os.path.join(LOCAL_UPLOAD_DIR, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        logger.info("Deleted local image: %s", file_path)

# --------------------------------------------------
# GCS STORAGE (GCP)
# --------------------------------------------------

def _gcs_upload(file: UploadFile) -> str:
    from google.cloud import storage  # lazy import

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    ext = file.filename.split(".")[-1]
    object_path = f"products/{uuid.uuid4()}.{ext}"

    blob = bucket.blob(object_path)
    blob.cache_control = "public, max-age=31536000, immutable"

    blob.upload_from_file(
        file.file,
        content_type=file.content_type,
        rewind=True,
    )

    return f"{CDN_BASE_URL}/{object_path}"


def _delete_gcs_image(image_url: str):
    from google.cloud import storage  # lazy import

    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    object_path = image_url.replace(f"{CDN_BASE_URL}/", "")
    blob = bucket.blob(object_path)

    if blob.exists():
        blob.delete()
        logger.info("Deleted GCS image: %s", object_path)
