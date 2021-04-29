import operator
import math

from config import PLATO_NER_ALLOWED_TYPES


class StatsModel:
    def __init__(self, stats_id, value):
        self.stats_id = stats_id
        self.value = value

    @staticmethod
    def calculate_overall_ner_type_stats(ner_results_list):
        overall_ner_type_stats = {}

        for ner_allowed_type in PLATO_NER_ALLOWED_TYPES:
            overall_ner_type_stats[ner_allowed_type] = 0

        for ner_results in ner_results_list:
            for ner_results_key, ner_results_value in ner_results["ner_stats"]["ner_type_stats"].items():
                overall_ner_type_stats[ner_results_key] += ner_results_value

        return overall_ner_type_stats

    @staticmethod
    def calculate_overall_ner_count_stats(ner_results_list):
        overall_ner_count_stats = 0

        for ner_results in ner_results_list:
            overall_ner_count_stats += ner_results["ner_stats"]["ner_count"]

        return overall_ner_count_stats

    @staticmethod
    def calculate_overall_words_count_stats(entries_list):
        overall_words_count_stats = 0

        for entry in entries_list:
            overall_words_count_stats += entry["words_count"]

        return overall_words_count_stats

    @staticmethod
    def calculate_overall_ner_coverage_stats(overall_ner_count_stats, overall_word_count_stats):
        overall_ner_coverage = overall_ner_count_stats / overall_word_count_stats
        return round(overall_ner_coverage, 3)

    @staticmethod
    def calculate_overall_ner_occurrences_stats(ner_results_list):
        overall_ner_occurrences_stats = {}

        for ner_result in ner_results_list:
            for ner_occurrence_key, ner_occurrence_value in ner_result["ner_stats"]["ner_occurrences"].items():
                overall_ner_occurrences_stats[ner_occurrence_key] = (
                        overall_ner_occurrences_stats[ner_occurrence_key] + ner_occurrence_value) if (
                        ner_occurrence_key in overall_ner_occurrences_stats) else ner_occurrence_value

        overall_ner_occurrences_stats = dict(
            sorted(overall_ner_occurrences_stats.items(), key=operator.itemgetter(1), reverse=True))

        overall_ner_occurrence_count = 0
        ner_occurrence_split_step = 0
        overall_ner_occurrences_partial_stats = {}
        first_time_flag = True

        overflow_condition = (ner_occurrence_split_step + 1000) > len(overall_ner_occurrences_stats.keys())
        formatted_key = f"{ner_occurrence_split_step + 1}-{ner_occurrence_split_step + 1000}"
        formatted_overflow_key = f"{ner_occurrence_split_step + 1}-{len(overall_ner_occurrences_stats.keys())}"

        for key, value in overall_ner_occurrences_stats.items():
            if overall_ner_occurrence_count % 999 == 0:
                if not first_time_flag:
                    ner_occurrence_split_step += 1000
                    overall_ner_occurrence_count = 0

                overflow_condition = (ner_occurrence_split_step + 1000) > len(overall_ner_occurrences_stats.keys())
                formatted_key = f"{ner_occurrence_split_step + 1}-{ner_occurrence_split_step + 1000}"
                formatted_overflow_key = f"{ner_occurrence_split_step + 1}-{len(overall_ner_occurrences_stats.keys())}"

                if overflow_condition:
                    overall_ner_occurrences_partial_stats[formatted_overflow_key] = {}
                else:
                    overall_ner_occurrences_partial_stats[formatted_key] = {}

                first_time_flag = False

            if overflow_condition:
                overall_ner_occurrences_partial_stats[formatted_overflow_key][key] = value
            else:
                overall_ner_occurrences_partial_stats[formatted_key][key] = value

            overall_ner_occurrence_count += 1

        return overall_ner_occurrences_partial_stats
