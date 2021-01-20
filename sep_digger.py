from bs4 import BeautifulSoup
from part_id_enum import PartId


def get_text_part_of_entry(source, part_id):
    if not isinstance(part_id, PartId):
        raise TypeError('part_id must be an instance of PartId')

    soup = BeautifulSoup(source, 'html.parser')

    if part_id == PartId.TITLE:
        return soup.h1.get_text()

    return soup.find(id=part_id.value).get_text()
