import collections
import csv
import io
import logging
import os
import re

import PyPDF2

DATA_FOLDER = "data"

logging.basicConfig()
logging.root.setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def _read_pdf(file_handler: io.TextIOWrapper) -> PyPDF2.PdfFileReader:
    reader = PyPDF2.PdfFileReader(file_handler)
    return reader


def _get_text_from_pdf_reader(reader: PyPDF2.PdfFileReader) -> str:
    return "\n".join(page.extractText() for page in reader.pages)


def _get_list_of_addresses(unstructured_text: str) -> list[str]:
    split_by_new_line = unstructured_text.split("\n")
    unstructured_adddresses = [
        line
        for line in split_by_new_line
        if re.match("^[0-9]+\.\s*\D*[\u4e00-\u9fff]+", line)
    ]

    final_addresses = []

    for address in unstructured_adddresses:
        print(address)
        (
            _,
            *address_with_space_list,
        ) = address.strip().split(". ")
        address_with_space = ". ".join(address_with_space_list)
        address_splitted_by_space = address_with_space.split(" ")
        normalized_address = "".join(
            partial_address
            for partial_address in address_splitted_by_space
            if partial_address
        )

        final_addresses.append(normalized_address)

    return final_addresses


def write_result_in_csv(counter: collections.Counter):
    csv_dict_list = [
        {"address": address, "count": count} for address, count in counter.items()
    ]

    with open("result.csv", "w") as file_handler:
        writer = csv.DictWriter(file_handler, fieldnames=csv_dict_list[0].keys())
        writer.writeheader()

        for csv_dict in csv_dict_list:
            writer.writerow(csv_dict)


def main():
    pdf_file_path_list = [f"{DATA_FOLDER}/{file}" for file in os.listdir(DATA_FOLDER)]
    pdf_file_path_list.sort()
    counter = collections.Counter()

    for pdf_file_path in pdf_file_path_list:
        logger.info("Working on file %s", pdf_file_path)
        with open(pdf_file_path, "rb") as pdf_file_handler:
            reader = _read_pdf(pdf_file_handler)
            unstructured_text = _get_text_from_pdf_reader(reader)
            address = _get_list_of_addresses(unstructured_text)
            counter += collections.Counter(address)

    write_result_in_csv(counter)


if __name__ == "__main__":
    main()
