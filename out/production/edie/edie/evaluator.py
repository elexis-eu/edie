from edie.api import ApiClient
from edie.model import Metadata, Dictionary, Entry, JsonEntry
from edie.tei import convert_tei
from metrics.base import MetadataMetric, EntryMetric

import logging


class Edie(object):
    def __init__(self, api_client, metadata_metrics_evaluators: [MetadataMetric] = None,
                 entry_metrics_evaluators: [EntryMetric] = None):
        self.lexonomy_client: ApiClient = api_client
        self.dictionaries: [Dictionary] = []
        self.metadata_metrics_evaluators: [
            MetadataMetric] = metadata_metrics_evaluators if metadata_metrics_evaluators is not None else []
        self.entry_metrics_evaluators: [EntryMetric] = entry_metrics_evaluators if entry_metrics_evaluators is not None else []
        self.metadata_report = {}
        self.report = {"endpoint": api_client.endpoint, "available": True, "dictionaries": {}}

    def load_dictionaries(self, dictionaries: [str] = None):
        correct_dictionaries = [
            "elexis-dsl-kalkar",
            "elexis-dsl-moth",
            "elexis-dsl-ods",
            "elexis-oeaw-jakob",
            "elexis-oeaw-schranka",
            "elexis-tcdh-bmz"
        ]
        dictionary_ids = dictionaries if dictionaries is not None else correct_dictionaries
        for dictionary_id in dictionary_ids:
            logging.info("Loading Metadata for %s" % dictionary_id)
            metadata = Metadata(self.lexonomy_client.about(dictionary_id))
            dictionary = Dictionary(dictionary_id, metadata)
            self.dictionaries.append(dictionary)
        return self.dictionaries

    def evaluate_metadata(self):
        for dictionary in self.dictionaries:
            metadata_report = {}
            metadata = dictionary.metadata
            if dictionary.metadata.errors:
                metadata_report['metadataErrors'] = metadata.errors

            for metadata_evaluator in self.metadata_metrics_evaluators:
                metadata_evaluator.analyze(metadata)
                metadata_report.update(metadata_evaluator.result())

            self.metadata_report[dictionary.id] = metadata_report

        return self.metadata_report

    def evaluate_entries(self):
        for dictionary in self.dictionaries:
            entry_report = {}
            offset = 0
            limit = 100
            # TODO: how do we know the # of max_entries?
            max_entries = dictionary.metadata.entryCount
            while offset <= max_entries:
                entries = self.lexonomy_client.list(dictionary, limit=limit, offset=offset)

                if not entries:
                    break
                for entry in entries:
                    offset += 1
                    if offset > max_entries:
                        break
                    entry = Entry(entry)
                    if entry.errors:
                        if "entryErrors" not in entry_report:
                            entry_report["entryErrors"] = []
                        entry_report["entryErrors"].extend(entry.errors)
                    else:
                        self._entry_report(self.lexonomy_client, dictionary, entry,
                                     entry_report)

                logging.info(".")

                if len(entries) < LIMIT:
                    break

            logging.info("\n")
            for entry_metric in entry_evaluators:
                if entry_metric.result():  # TODO
                    print(entry_metric, entry_metric.result())
                    dict_report.update(entry_metric.result())

    def _entry_report(self, dictionary_id: str, entry: Entry, entry_report: dict):
        if "json" in entry.formats:
            json_entry = JsonEntry(self.lexonomy_client.json(dictionary_id, entry.id))
            if json_entry.errors:
                if "entryErrors" not in entry_report:
                    entry_report["entryErrors"] = []
                entry_report["entryErrors"].extend(json_entry.errors)
            else:
                for entry_metric in self.entry_metrics_evaluators:
                    entry_metric.accumulate(json_entry)
        elif "tei" in entry.formats:
            tei_entry = self.lexonomy_client.tei(dictionary_id, entry.id)
            errors = []
            entries = convert_tei(tei_entry, errors, entry.id)
            if errors:
                if "entryErrors" not in entry_report:
                    entry_report["entryErrors"] = []
                entry_report["entryErrors"].extend(errors)
            else:
                for entry in entries:
                    for entry_metric in self.entry_metrics_evaluators:
                        entry_metric.accumulate(entry)
        else:
            print("TODO: non-JSON entries")


    def _r
        un_entry_metrics_evaluators(self, entry):
        for entry_metric in self.entry_metrics_evaluators:
            entry_metric.accumulate(entry)

