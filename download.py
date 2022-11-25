import datetime
import logging
import pathlib
import requests

logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger(__name__)

DOWNLOAD_FOLDER = "data"

CTN_START_DATE = datetime.datetime.strptime("2022-03-11", "%Y-%m-%d")
CTN_END_DATE = datetime.datetime.strptime("2022-03-25", "%Y-%m-%d")


def _format_date(date: datetime.date) -> str:
    return date.strftime("%Y%m%d")


def _generate_url(date: datetime.date) -> str:
    date_str = _format_date(date)
    return f"https://www.chp.gov.hk/files/pdf/ctn_{date_str}.pdf"


def _generate_path(date: datetime.date) -> pathlib.Path:
    date_str = _format_date(date)
    return pathlib.Path(DOWNLOAD_FOLDER) / pathlib.Path(f"ctn_{date_str}.pdf")


def _download_file(url: str, dst_path: pathlib.Path):
    response = requests.get(url)

    if response.status_code != 200:
        logger.info("Skip downloading because of status code %s", response.status_code)
        return

    with open(dst_path, "wb") as file_handler:
        file_handler.write(response.content)


def download():
    current_date = CTN_START_DATE

    while current_date <= CTN_END_DATE:
        logger.info("Working on CTN date = %s", current_date)
        url = _generate_url(current_date)
        path = _generate_path(current_date)
        _download_file(url, path)
        current_date += datetime.timedelta(days=1)
        logger.info("Done working on CTN date = %s", current_date)


if __name__ == "__main__":
    download()
