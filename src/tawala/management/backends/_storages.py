"""Custom storage backends."""

from django.core.files.base import ContentFile, File
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from vercel.blob import BlobClient  # pyright: ignore[reportMissingTypeStubs]

from ..settings import BLOB_READ_WRITE_TOKEN

__all__: list[str] = ["VercelBlobStorageBackend"]


@deconstructible
class VercelBlobStorageBackend(Storage):
    """Storage backend for Vercel Blob."""

    def __init__(self) -> None:
        """Set up Vercel Blob client."""
        self.client: BlobClient = BlobClient(BLOB_READ_WRITE_TOKEN)

    def _save(self, name: str, content: File) -> str:
        """Upload file to Vercel Blob."""
        file_content: bytes = content.read()
        result = self.client.put(
            name,
            file_content,
            access="public",
            add_random_suffix=True,  # This ensures unique filenames
            content_type=getattr(content, "content_type", None),
        )
        return result.pathname

    def _open(self, name: str, mode: str = "rb") -> ContentFile:
        """Download file from Vercel Blob."""
        listing = self.client.list_objects(prefix=name, limit=1)
        if not listing.blobs:
            raise FileNotFoundError(f"File {name} not found.")
        result = self.client.get(listing.blobs[0].url)
        return ContentFile(result.content, name=name)

    def delete(self, name: str) -> None:
        """Delete file from Vercel Blob."""
        listing = self.client.list_objects(prefix=name, limit=1)
        if listing.blobs:
            self.client.delete([listing.blobs[0].url])

    def exists(self, name: str) -> bool:
        """Check if file exists in Vercel Blob."""
        listing = self.client.list_objects(prefix=name, limit=1)
        return len(listing.blobs) > 0

    def url(self, name: str) -> str:
        """Return public URL for the file."""
        listing = self.client.list_objects(prefix=name, limit=1)
        if not listing.blobs:
            raise ValueError(f"File {name} not found in Vercel Blob storage")
        return listing.blobs[0].url

    def size(self, name: str) -> int:
        """Return file size."""
        listing = self.client.list_objects(prefix=name, limit=1)
        if not listing.blobs:
            return 0
        return listing.blobs[0].size

    def get_valid_name(self, name: str) -> str:
        """Return a valid filename for storage."""
        return name

    def get_available_name(self, name: str, max_length: int | None = None) -> str:
        """Return an available filename (Vercel Blob handles uniqueness with add_random_suffix)."""
        return name
