import pandas as pd
from datetime import datetime
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
from config import DATA_PATH, AD_ID  # noqa: E402


PATTERN = '''
Отчет по объявлению {highlighting}{ad_id}{highlighting} за {date}:
{cost_emoji} Траты: {cost:.2f} рублей ({cost_margin:+.0%})
{views_emoji} Показы: {views:.0f} ({views_margin:+.0%})
{clicks_emoji} Клики: {clicks:.0f} ({clicks_margin:+.0%})
{ctr_emoji} CTR: {ctr:.2f} ({ctr_margin:+.0%})
'''

EMOJI_UP = '&#10133;'
EMOJI_DOWN = '&#10134;'
EMOJI_HIGHLIGHTING = '&#10069;'


def create_report():
    metrics = _read_metrics()
    last_date = _get_last_date(metrics)
    metrics = _extract_date_and_ad(metrics, last_date, AD_ID)
    report = _format_report(metrics, last_date, AD_ID)
    _save_report(report, last_date)


def _read_metrics() -> pd.DataFrame:
    return pd.read_csv(
        DATA_PATH / 'metrics.csv',
        index_col=['ad_id', 'value_type', 'date'],
        parse_dates=['date'],
    )


def _get_last_date(metrics: pd.DataFrame) -> datetime:
    return metrics.index.get_level_values('date').max()


def _extract_date_and_ad(
    metrics: pd.DataFrame,
    date: datetime,
    ad_id: int,
) -> pd.DataFrame:
    return metrics.xs(key=(ad_id, date), level=('ad_id', 'date'))


def _format_report(
    metrics: pd.DataFrame,
    date: datetime,
    ad_id: int,
) -> str:
    args = {
        'ad_id': ad_id,
        'date': date.strftime('%-d %b'),
        'highlighting': EMOJI_HIGHLIGHTING,
    }
    for metric in metrics.columns:

        metric_margin = metric + '_margin'
        metric_emoji = metric + '_emoji'

        args[metric] = metrics.loc['absolute', metric]
        args[metric_margin] = metrics.loc['relative', metric]
        args[metric_emoji] = _get_emoji(
            metrics.loc['relative', metric])

    return PATTERN.format(**args)


def _save_report(report: str, date: datetime) -> None:
    file_name = 'report_' + date.strftime('%Y_%m_%d') + '.txt'
    file_path = DATA_PATH / file_name
    with file_path.open('w') as f:
        f.write(report)


def _get_emoji(value: float) -> str:
    if value > 0:
        return EMOJI_UP
    if value < 0:
        return EMOJI_DOWN
    return ''


if __name__ == '__main__':
    create_report()
