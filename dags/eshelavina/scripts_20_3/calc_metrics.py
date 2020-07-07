import pandas as pd
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
from config import DATA_PATH  # noqa: E402


def calc_dayly_metrics() -> None:
    data = _read_data()
    metrics = _calc_clicks_and_views(data)
    metrics['ctr'] = _calc_ctr(metrics)
    metrics['cost'] = _calc_cost(data)
    _save_metrics(metrics)


def _read_data():
    return pd.read_csv(
        DATA_PATH / 'raw_data.csv',
        parse_dates=['date', 'time']
    )


def _calc_clicks_and_views(data: pd.DataFrame) -> pd.DataFrame:
    clicks_and_views = (
        data
        .pivot_table(
            index=['ad_id', 'date'],
            columns='event',
            values='time',
            aggfunc='count',
            fill_value=0)
        .rename(columns=lambda col: col + 's')
    )
    if 'clicks' not in clicks_and_views:
        clicks_and_views['clicks'] = 0
    if 'views' not in clicks_and_views:
        clicks_and_views['views'] = 0

    return clicks_and_views


def _calc_ctr(metrics: pd.DataFrame) -> pd.Series:
    ctr = (
        (metrics.clicks / metrics.views)
        .mul(100)
        .round(4)
    )
    return ctr


def _calc_cost(data: pd.DataFrame) -> pd.Series:
    paid_events = data.query(
        "(event == 'view' and ad_cost_type == 'CPM')"
        "or (event == 'click' and ad_cost_type == 'CPC')"
    )
    paid_events['cost_coefficient'] = (
        paid_events
        .ad_cost_type
        .map({
            'CPM': 0.001,
            'CPC': 1,
        })
    )
    paid_events['cost'] = (
        paid_events.ad_cost
        * paid_events.cost_coefficient
    )
    dayly_costs = (
        paid_events
        .groupby(['ad_id', 'date'])
        .cost
        .sum()
        .round(2)
    )
    return dayly_costs


def _save_metrics(metrics: pd.DataFrame) -> None:
    metrics.to_csv(DATA_PATH / 'metrics.csv')


if __name__ == '__main__':
    calc_dayly_metrics()
