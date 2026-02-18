import os
import aiofiles
from .base import FileStorage

UPLOAD_DIR = "uploads"

class LocalStorage(FileStorage):

    async def save(self, file, filename: str) -> str:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        path = os.path.join(UPLOAD_DIR, filename)

        async with aiofiles.open(path, "wb") as out:
            await out.write(await file.read())

        return f"/uploads/{filename}"
