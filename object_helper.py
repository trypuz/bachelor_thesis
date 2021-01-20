def sum_dictionaries(accumulator, element):
    for key, value in element.items():
        accumulator[key] = accumulator.get(key, 0) + value
    return accumulator


def sort_stats_from_largest(stats_dict):
    return dict(sorted(stats_dict.items(), key=lambda item: item[1], reverse=True))
