import pandas as pd
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
from config import DATA_PATH  # noqa: E402


def add_relative_metrics() -> None:
    absolute_metrics = _read_metrics()
    relative_metrics = _calc_relatives(absolute_metrics)
    metrics = _concat(absolute_metrics, relative_metrics)
    _save_metrics(metrics)


def _read_metrics() -> pd.DataFrame:
    return pd.read_csv(
        DATA_PATH / 'metrics.csv',
        index_col=['ad_id', 'date'],
        parse_dates=['date'],
    )


def _calc_relatives(absolute_metrics: pd.DataFrame) -> pd.DataFrame:
    relative_metrics = (
        absolute_metrics
        .rolling(2)
        .agg(lambda x: x[1] / x[0] - 1)
        .fillna(0)
        .round(4)
    )
    return relative_metrics


def _concat(
    absolute_metrics: pd.DataFrame,
    relative_metrics: pd.DataFrame,
) -> pd.DataFrame:

    absolute_metrics['value_type'] = 'absolute'
    relative_metrics['value_type'] = 'relative'

    united_metrics = (
        pd.concat([
            absolute_metrics,
            relative_metrics,
        ])
        .set_index('value_type', append=True)
        .reorder_levels(['ad_id', 'value_type', 'date'])
    )
    return united_metrics


def _save_metrics(metrics: pd.DataFrame) -> None:
    metrics.to_csv(DATA_PATH / 'metrics.csv')


if __name__ == '__main__':
    add_relative_metrics()
