from config import PLATO_NER_ALLOWED_TYPES


class StatsModel:
    def __init__(self, stats_id, stats):
        self.stats_id = stats_id
        self.stats = stats

    @staticmethod
    def calculate_overall_ner_stats(ner_results_list):
        overall_ner_stats_for_preamble = {}
        overall_ner_stats_for_main_text = {}

        for ner_allowed_type in PLATO_NER_ALLOWED_TYPES:
            overall_ner_stats_for_preamble[ner_allowed_type] = 0
            overall_ner_stats_for_main_text[ner_allowed_type] = 0

        for ner_results in ner_results_list:
            for ner_results_for_preamble_key, ner_results_for_preamble_value in \
                    ner_results["ner_stats"]["preamble"].items():
                overall_ner_stats_for_preamble[ner_results_for_preamble_key] += ner_results_for_preamble_value

            for ner_results_for_main_text_key, ner_results_for_main_text_value in \
                    ner_results["ner_stats"]["main_text"].items():
                overall_ner_stats_for_main_text[ner_results_for_main_text_key] += ner_results_for_main_text_value

        return {
            "preamble": overall_ner_stats_for_preamble,
            "main_text": overall_ner_stats_for_main_text
        }
