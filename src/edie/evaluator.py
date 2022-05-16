import sys
import pandas as pd
import matplotlib.pyplot as plt
from xml.etree.ElementTree import ParseError
from pandas.plotting import parallel_coordinates
from requests import HTTPError
from requests.exceptions import JSONDecodeError

from edie.api import ApiClient
from edie.helper import validate_tei
from edie.model import Metadata, Dictionary, Entry, JsonEntry
from edie.vocabulary import SIZE_OF_DICTIONARY, AGGREGATION_METRICS, DICTIONARY_SIZE
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
        self.aggregate_evaluators: []

        self.report = {"endpoint": api_client.endpoint, "available": True, 
                "dictionaries": {},"errors":[]}
        self.entries_limit = 100

    def load_dictionaries(self, dictionaries: [str] = None, limit=-1):
        if dictionaries:
            dictionary_ids = dictionaries
        else:
            try:
                dictionary_ids = self.lexonomy_client.dictionaries()["dictionaries"]
            except HTTPError as error:
                self.report["available"] = False
                self._add_errors(self.report, [str(error)])
        if limit == -1:
            limit = len(dictionary_ids)
        sys.stderr.write(f'Evaluating {len(dictionary_ids):d} dictionaries\n')
        count = 0
        for dictionary_id in dictionary_ids:
            try:
                if count < limit:
                    sys.stderr.write(f"Loading Metadata of {dictionary_id} \n")
                    metadata = Metadata(self.lexonomy_client.about(dictionary_id))
                    dictionary = Dictionary(dictionary_id, metadata)
                    self.dictionaries.append(dictionary)
                count+=1
            except HTTPError as error:
                self._add_errors(self.report, [str(error)])
                self.report["available"] = False
                sys.stderr.write(f'Failed loading {dictionary_id} dictionary \n')

        return self.dictionaries

    def evaluate_metadata(self) -> None:
        for dictionary in self.dictionaries:
            self._prepare_report(dictionary)

            sys.stderr.write(f'Evaluating {dictionary}')

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

            entry_counter = max_entries if max_entries is not None else dictionary.metadata.entry_count
            self._loop_entries_endpoint(dictionary, entry_report, entry_counter)

            sys.stderr.write("\n")

            self._collect_entry_metrics(entry_report)
            self._add_entry_report(dictionary, entry_report)

    def entry_evaluation_report_as_dataframe(self):
        return pd.DataFrame.from_dict({i: self.report['dictionaries'][i]['entry_report']
                                       for i in self.report['dictionaries'].keys()},
                                      orient='index')

    def metadata_evaluation_report_as_dataframe(self):
        return pd.DataFrame.from_dict({i: self.report['dictionaries'][i]['metadata_report']
                                       for i in self.report['dictionaries'].keys()},
                                      orient='index')

    def entry_report(self, dictionary_id):
        return self.report['dictionaries'][dictionary_id]['entry_report']

    def visualize(self):
        dataframe = self.entry_evaluation_report_as_dataframe().drop('errors', axis=1)
        dataframe = dataframe.apply(lambda x: x / x.max(), axis=0)
        dataframe['dict_type'] = 0
        parallel_coordinates(dataframe, "dict_type", axvlines=True)
        plt.show()

    def aggregated_evaluation(self):
        df = self.metadata_evaluation_report_as_dataframe()

        self.report[AGGREGATION_METRICS] = {
            DICTIONARY_SIZE: {
                'min': df[SIZE_OF_DICTIONARY].min(),
                'max': df[SIZE_OF_DICTIONARY].max(),
                'mean': df[SIZE_OF_DICTIONARY].mean(),
                'median': df[SIZE_OF_DICTIONARY].median()
            }
        }

    def _loop_entries_endpoint(self, dictionary, entry_report, max_entries):
        entries_offset = 0
        while entries_offset <= max_entries:
            try:
                entries = self.lexonomy_client.list(dictionary.id, limit=self.entries_limit, offset=entries_offset)
            except HTTPError as error:
                self._add_errors(entry_report, [str(error)])
            except JSONDecodeError as error:
                self._add_errors(entry_report, [str(error)])
            if not entries:
                break
            entries_offset = self._handle_entries(dictionary, entries, entry_report, max_entries, entries_offset)
            sys.stderr.write(str(entries_offset) + '...')
            sys.stderr.flush()
            if len(entries) < self.entries_limit:
                break

    def _collect_entry_metrics(self, entry_report):
        for entry_metric in self.entry_metrics_evaluators:
            if entry_metric.result():
                sys.stderr.write(str(entry_metric))
                sys.stderr.write(str(entry_metric.result()))
                sys.stderr.write("\n")
                sys.stderr.flush()
                entry_report.update(entry_metric.result())
            entry_metric.reset()

    def _handle_entries(self, dictionary, entries, entry_report, max_entries, entries_offset):
        for entry in entries:
            entries_offset += 1
            print(entries_offset)
            if entries_offset > max_entries:
                break
            try:
                entry = Entry(entry)
                if entry.errors:
                    self._add_errors(entry_report, entry.errors)
                else:
                    self._entry_report(dictionary.id, entry_report, entry)

            except HTTPError:
                self._add_errors(entry_report, f'Failed to retrieve lemmas for dictionary {dictionary.id}')
            except ParseError as parse_error:
                self._add_errors(entry_report, [str(parse_error)])
            except JSONDecodeError as json_decode_error:
                self._add_errors(entry_report, [str(json_decode_error)])

        return entries_offset

    def evaluation_report(self):
        return self.report

    def _entry_report(self, dictionary_id: str, entry_report: dict, entry: Entry):
        retrieved_entry: JsonEntry = self._retrieve_entry(dictionary_id, entry)
        if retrieved_entry is not None:
            if retrieved_entry.errors:
                self._add_errors(entry_report, retrieved_entry.errors)
            self._run_entry_metrics_evaluators(retrieved_entry, entry)
        else: #TODO: handle None case
            pass

    def _retrieve_entry(self, dictionary_id, entry: Entry) -> JsonEntry:
        if "json" in entry.formats:
            try:
                return JsonEntry(self.lexonomy_client.json(dictionary_id, entry.id))
            except JSONDecodeError as jde:
                raise JSONDecodeError(f"Error parsing json response {entry.id}: {str(jde)}")

        elif "tei" in entry.formats:
            tei_entry = self.lexonomy_client.tei(dictionary_id, entry.id)
            try:
                tei_entry_element = validate_tei(tei_entry)
                return JsonEntry.from_tei_entry(tei_entry_element, entry.id)
            except ParseError as pe:
                raise ParseError(f"Error with entry {entry.id}: {str(pe)}")

    def _run_entry_metrics_evaluators(self, entry_details, entry_metadata):
        for entry_metric in self.entry_metrics_evaluators:
            entry_metric.accumulate(entry_details, entry_metadata)

    def _prepare_report(self, dictionary):
        if dictionary.id not in self.report['dictionaries']:
            self.report['dictionaries'][dictionary.id] = {'entry_report': {}, 'metadata_report': {}}

    def _add_entry_report(self, dictionary, entry_report):
        self.report['dictionaries'][dictionary.id]['entry_report'] = entry_report

    def _add_errors(self, entry_report, errors):
        if "errors" not in entry_report:
            entry_report["errors"] = []
        entry_report["errors"].extend(errors)
