from supabase import create_client
from app.core.config import settings

supabase = create_client(settings.supabase_url, settings.supabase_key)

def upload_file(file_bytes: bytes, storage_path: str) -> None:
    supabase.storage.from_(settings.supabase_bucket).upload(
        storage_path,
        file_bytes,
        file_options={"upsert":"true"}
    )

def download_file(storage_path: str) -> bytes:
    return supabase.storage.from_(settings.supabase_bucket).download(storage_path)

def delete_file(storage_path: str) -> None:
    supabase.storage.from_(settings.supabase_bucket).remove([storage_path])