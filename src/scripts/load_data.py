import os
import numpy as np
import hopsworks
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


def setup_hopsworks():
    project = hopsworks.login(api_key_value=config("HOPSWORKS_KEY"))
    fs = project.get_feature_store()
    return fs

def to_hopsworks(data: pl.DataFrame) -> None:
    fs = setup_hopsworks()
    trans_fg = fs.get_or_create_feature_group(
        name="churn_training",
        version=1,
        description="Churn Training data",
        primary_key=['cc_num'],
        event_time='datetime',
        online_enabled=True,
)

def from_hopsworks() -> None:
    pass


if __name__ == "__main__":
    raw_data = from_supabase(config={})