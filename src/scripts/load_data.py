import os
import polars as pl
from decouple import config
from supabase import create_client, Client


def create_engine() -> Client:
    url: str = config("SUPABASE_URL")
    key: str = config("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase


def from_supabase(config: dict) -> pl.DataFrame:
    supabase: Client = create_engine()
    count: int = supabase.table("raw_data").select('*', count="exact").execute().count
    print(f"Length of data: {count}")
    data_chunks: list = []
    start: int = 0
    chunk_size: int = 1000
    while True:
        chunk: list = supabase.table("raw_data").select("*").range(start, start + chunk_size - 1).execute().data
        if not chunk:
            break
        data_chunks.extend(chunk)
        if len(chunk) < chunk_size:
            break
        start += chunk_size
    raw_data = pl.DataFrame(data_chunks)
    return raw_data

def to_hopsworks() -> None:
    pass

def from_hopsworks() -> None:
    pass


if __name__ == "__main__":
    raw_data = from_supabase(config={})