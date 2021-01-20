import csv
import json


def write_to_csv(filename, data):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['WORD', 'NER_TYPE', 'START_WORD_OFFSET', 'END_WORD_OFFSET', 'START_CHAR_OFFSET',
                         'END_CHAR_OFFSET', 'CONTEXT'])
        writer.writerows(data)


def write_to_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
