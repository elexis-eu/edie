import argparse
import sys

from edie.evaluator import Edie
from metrics.base import FormsPerEntryMetric, NumberOfSensesEvaluator, DefinitionOfSenseEvaluator, \
    AvgDefinitionLengthEvaluator
import json
from edie.api import ApiClient
from edie.model import Metadata, Entry, JsonEntry, Dictionary
from edie.tei import convert_tei
from requests.exceptions import RequestException
import logging

logging.basicConfig(level=logging.DEBUG)

LIMIT = 100

metadata_evaluators = []

entry_evaluators = [FormsPerEntryMetric(), NumberOfSensesEvaluator(), DefinitionOfSenseEvaluator(),
                    AvgDefinitionLengthEvaluator()]


def list_dictionaries():
    return api_instance.dictionaries()["dictionaries"]


def entry_report(entry):
    if "json" in entry.formats:
        json_entry = JsonEntry(api_instance.json(dictionary, entry.id))
        if json_entry.errors:
            if "entryErrors" not in dict_report:
                dict_report["entryErrors"] = []
            dict_report["entryErrors"].extend(json_entry.errors)
        else:
            for entry_metric in entry_evaluators:
                entry_metric.accumulate(json_entry)
    elif "tei" in entry.formats:
        tei_entry = api_instance.tei(dictionary, entry.id)
        errors = []
        entries = convert_tei(tei_entry, errors, entry.id)
        if errors:
            if "entryErrors" not in dict_report:
                dict_report["entryErrors"] = []
            dict_report["entryErrors"].extend(errors)
        else:
            for entry in entries:
                for entry_metric in entry_evaluators:
                    entry_metric.accumulate(entry)
    else:
        print("TODO: non-JSON entries")


def setup_argparser() -> argparse.ArgumentParser:
    argparser = argparse.ArgumentParser("ELEXIS Dictionary Evaluation Tool (EDiE)")
    argparser.add_argument("--server", action="store_true",
                           help="Start in server mode")
    argparser.add_argument("-d", nargs="+",
                           help="Dictionaries to evaluate")
    argparser.add_argument("-e",
                           help="Endpoint to query")
    argparser.add_argument("-m", nargs="+",
                           help="List of metrics to evaluate")
    argparser.add_argument("--max-entries",
                           help="Maximum number of entries to evaluate")
    argparser.add_argument("--api-key",
                           help="The API KEY to use")

    return argparser


def analyze_metadata():
    metadata = Metadata(api_instance.about(dictionary))
    if metadata.errors:
        dict_report["metadataErrors"] = metadata.errors
    else:
        for metadata_metric in metadata_evaluators:
            dict_report.update(metadata_metric.apply(metadata))

    return metadata


def analyze():
    endpoint = args.e if args.e else "http://localhost:8000/"
    report = {"endpoint": endpoint, "available": True, "dictionaries": {}}
    api_instance = ApiClient(endpoint, args.api_key)
    edie = Edie(api_instance)

    edie.load_dictionaries(args.d)


if __name__ == "__main__":
    args = setup_argparser().parse_args()

    endpoint = args.e if args.e else "http://localhost:8000/"
    report = {"endpoint": endpoint, "available": True, "dictionaries": {}}
    api_instance = ApiClient(endpoint, args.api_key)
    edie = Edie(api_instance)

    dictionaries: [Dictionary] = edie.load_dictionaries(args.d)
    metadata_report = edie.evaluate_metadata()


def test_main():
    args = setup_argparser().parse_args()

    if args.max_entries:
        max_entries = int(args.max_entries)
    else:
        max_entries = float('inf')

    if args.server:
        print("TODO: implement server mode")
        sys.exit(-1)
    else:
        endpoint = args.e if args.e else "http://localhost:8000/"
        report = {"endpoint": endpoint, "available": True, "dictionaries": {}}
        api_instance = ApiClient(endpoint, args.api_key)

        dictionaries = args.d if args.d else list_dictionaries()

        try:
            sys.stderr.write("Evaluating %d dictionaries\n" % len(dictionaries))

            for dictionary in dictionaries:
                sys.stderr.write("Evaluating %s" % dictionary)

                for entry_metric in entry_evaluators:
                    entry_metric.reset()

                dict_report = {}
                report["dictionaries"][dictionary] = dict_report

                metadata = analyze_metadata()

                offset = 0
                # TODO: how do we know the # of max_entries?
                while offset <= max_entries:
                    entries = api_instance.list(dictionary, limit=LIMIT, offset=offset)
                    if not entries:
                        break

                    for entry in entries:
                        offset += 1
                        if offset > max_entries:
                            break
                        entry = Entry(entry)
                        if entry.errors:
                            if "entryErrors" not in dict_report:
                                dict_report["entryErrors"] = []
                            dict_report["entryErrors"].extend(entry.errors)
                        else:
                            entry_report(api_instance, dictionary, entry,
                                         dict_report)

                    sys.stderr.write(".")
                    sys.stderr.flush()

                    if len(entries) < LIMIT:
                        break

                sys.stderr.write("\n")
                for entry_metric in entry_evaluators:
                    if entry_metric.result():  # TODO
                        print(entry_metric, entry_metric.result())
                        dict_report.update(entry_metric.result())

        except RequestException as e:
            report["available"] = False

        print(json.dumps(report))
