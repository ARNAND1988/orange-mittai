from abc import ABC, abstractmethod
from typing import BinaryIO

class FileStorage(ABC):
    @abstractmethod
    async def save(self, file: BinaryIO, filename: str) -> str:
        pass
