from app.config import settings
from app.storage.local import LocalStorage
from app.storage.gcs import GCSStorage

def get_storage():
    if settings.STORAGE_BACKEND == "gcs":
        return GCSStorage()
    return LocalStorage()
