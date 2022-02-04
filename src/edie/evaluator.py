import sys
from xml.etree.ElementTree import ParseError

from requests import HTTPError

from edie.api import ApiClient
from edie.helper import validate_tei
from edie.model import Metadata, Dictionary, Entry, JsonEntry
from metrics.base import MetadataMetric, EntryMetric



class Edie(object):
    def __init__(self, api_client, metadata_metrics_evaluators: [MetadataMetric] = None,
                 entry_metrics_evaluators: [EntryMetric] = None):
        self.lexonomy_client: ApiClient = api_client
        self.dictionaries: [Dictionary] = []
        self.metadata_metrics_evaluators: [
            MetadataMetric] = metadata_metrics_evaluators if metadata_metrics_evaluators is not None else []
        self.entry_metrics_evaluators: [
            EntryMetric] = entry_metrics_evaluators if entry_metrics_evaluators is not None else []

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
        sys.stderr.write("Evaluating %d dictionaries\n" % len(dictionary_ids))
        for dictionary_id in dictionary_ids:
            sys.stderr.write("Evaluating %s" % dictionary_id)
            metadata = Metadata(self.lexonomy_client.about(dictionary_id))
            dictionary = Dictionary(dictionary_id, metadata)
            self.dictionaries.append(dictionary)
        return self.dictionaries

    def evaluate_metadata(self) -> None:
        for dictionary in self.dictionaries:
            self._prepare_report(dictionary)

            sys.stderr.write("Evaluating %s" % dictionary)

            metadata_report = {}
            metadata = dictionary.metadata
            if dictionary.metadata.errors:
                metadata_report['errors'] = dictionary.metadata.errors

            for metadata_evaluator in self.metadata_metrics_evaluators:
                metadata_evaluator.analyze(metadata)
                metadata_report.update(metadata_evaluator.result())

            self.report['dictionaries'][dictionary.id]['metadata_report'] = metadata_report

    def evaluate_entries(self, max_entries=None) -> None:
        for dictionary in self.dictionaries:
            self._prepare_report(dictionary)
            entry_report = {}
            offset = 0
            limit = 100
            # TODO: how do we know the # of max_entries?
            max_entries = max_entries if max_entries is not None else dictionary.metadata.entryCount
            while offset <= max_entries:
                try:
                    entries = self.lexonomy_client.list(dictionary.id, limit=limit, offset=offset)

                    if not entries:
                        break
                    for entry in entries:
                        offset += 1
                        if offset > max_entries:
                            break
                        entry = Entry(entry)
                        if entry.errors:
                            self._add_errors(entry_report, entry.errors)
                        else:
                            self._entry_report(dictionary.id, entry_report, entry)

                    sys.stderr.write(".")
                    sys.stderr.flush()
                    if len(entries) < limit:
                        break

                except HTTPError as he:
                    self._add_errors(entry_report, f'Failed to retrieve lemmas for dictionary {dictionary.id}')
                except ParseError as pe:
                    self._add_errors(entry_report, str(pe))


            sys.stderr.write("\n")

            for entry_metric in self.entry_metrics_evaluators:
                if entry_metric.result():
                    print(entry_metric, entry_metric.result())
                    entry_report.update(entry_metric.result())
            self._add_entry_report(dictionary, entry_report)

    def evaluation_report(self):
        return self.report

    def entry_report(self, dictionary_id):
        return self.report['dictionaries'][dictionary_id]['entry_report']


    def _entry_report(self, dictionary_id: str, entry_report: dict, entry: Entry):
        retrieved_entry: JsonEntry = self._retrieve_entry(dictionary_id, entry)
        if retrieved_entry is not None:
            if retrieved_entry.errors:
                self._add_errors(entry_report, retrieved_entry.errors)
            self._run_entry_metrics_evaluators(retrieved_entry)

    def _retrieve_entry(self, dictionary_id, entry: Entry) -> JsonEntry:
        if "json" in entry.formats:
            return JsonEntry(self.lexonomy_client.json(dictionary_id, entry.id))
        elif "tei" in entry.formats:
            tei_entry = self.lexonomy_client.tei(dictionary_id, entry.id)
            try:
                tei_entry_element = validate_tei(tei_entry)
                return JsonEntry.from_tei_entry(tei_entry_element, entry.id)
            except ParseError as pe:
                raise ParseError("Error with entry %s: %s" % (entry.id, str(pe)))

    def _run_entry_metrics_evaluators(self, entry):
        for entry_metric in self.entry_metrics_evaluators:
            entry_metric.accumulate(entry)

    def _prepare_report(self, dictionary):
        if dictionary.id not in self.report['dictionaries']:
            self.report['dictionaries'][dictionary.id] = {'entry_report':{}, 'metadata_report': {}}

    def _add_entry_report(self, dictionary, entry_report):
        self.report['dictionaries'][dictionary.id]['entry_report'] = entry_report

    def _add_errors(self, entry_report, errors):
        if "errors" not in entry_report:
            entry_report["errors"] = []
        entry_report["errors"].extend(errors)

