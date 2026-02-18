from google.cloud import storage
from .base import FileStorage
from app.config import settings

client = storage.Client(project=settings.GCP_PROJECT)

class GCSStorage(FileStorage):

    async def save(self, file, filename: str) -> str:
        bucket = client.bucket(settings.GCS_BUCKET)
        blob = bucket.blob(filename)

        blob.upload_from_file(file, rewind=True)
        blob.make_public()

        return blob.public_url
