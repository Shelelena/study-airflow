import pandas as pd
import os
from pathlib import Path

# this is required because airflow runs scripts in temporary directory
os.chdir(Path(__file__).parent)
from config import DATA_PATH  # noqa: E402


URL = (
    'https://docs.google.com/spreadsheets/d/e/2PACX-1vR-ti6Su94955DZ4'
    'Tky8EbwifpgZf_dTjpBdiVH0Ukhsq94jZdqoHuUytZsFZKfwpXEUCKRFteJRc9P'
    '/pub?gid=889004448&single=true&output=csv'
)


def load_data():
    data = _load_data_from_url()
    _create_directory()
    _save_data(data)


def _load_data_from_url() -> pd.DataFrame:
    return pd.read_csv(URL)


def _create_directory() -> None:
    if not DATA_PATH.exists():
        DATA_PATH.mkdir(parents=True)


def _save_data(data: pd.DataFrame) -> None:
    data.to_csv(
        DATA_PATH / 'raw_data.csv',
        index=False,
    )


if __name__ == '__main__':
    load_data()
