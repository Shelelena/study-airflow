import vk_api
from datetime import datetime
import os
from pathlib import Path

os.chdir(Path(__file__).parent)
from config import DATA_PATH, VK_TOKEN, VK_RECEPIENT  # noqa: E402


def send_vk_report():
    assert VK_TOKEN and VK_RECEPIENT, 'vk params not set'

    report = _read_latest_report()
    vk = _init_vk()
    _send_report(vk, report)


def _read_latest_report() -> str:
    reports = DATA_PATH.glob('report*.txt')
    reports = sorted(reports)
    latest_report = reports[-1]
    with latest_report.open() as f:
        report_text = f.read()
    return report_text


def _init_vk():
    vk_session = vk_api.VkApi(token=VK_TOKEN)
    vk = vk_session.get_api()
    return vk


def _send_report(vk, report: str) -> None:
    random_id = int(datetime.timestamp(datetime.now()))
    vk.messages.send(
        user_id=VK_RECEPIENT,
        random_id=random_id,
        message=report
    )


if __name__ == '__main__':
    send_vk_report()
