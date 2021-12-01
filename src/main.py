import argparse
import sys
from metrics.base import FormsPerEntryMetric, NumberOfSensesEvaluator
import json
from edie.api import ApiClient
from edie.model import Metadata, Entry, JsonEntry
from requests.exceptions import RequestException

LIMIT = 100

metadata_metrics = []

entry_metrics = [FormsPerEntryMetric(), NumberOfSensesEvaluator()]


def list_dictionaries(api_instance):
    return api_instance.dictionaries()["dictionaries"]


def entry_report(api_instance, dictionary, entry, dict_report):
    if "json" in entry.formats:
        json_entry = JsonEntry(api_instance.json(dictionary, entry.id))
        if json_entry.errors:
            if "entryErrors" not in dict_report:
                dict_report["entryErrors"] = []
            dict_report["entryErrors"].extend(json_entry.errors)
        else:
            for entry_metric in entry_metrics:
                entry_metric.accumulate(json_entry)
    else:
        print("TODO: non-JSON entries")


if __name__ == "__main__":
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

    args = argparser.parse_args()
    if args.max_entries:
        max_entries = int(args.max_entries)
    else:
        max_entries = float('inf')

    if args.server:
        print("TODO: implement server mode")
        sys.exit(-1)
    else:
        endpoint = args.e if args.e else "http://localhost:8000/"
        report = {"endpoint": endpoint}

        api_instance = ApiClient(endpoint)
        try:
            dictionary_list = list_dictionaries(api_instance)
            report["available"] = True
            dictionaries = args.d if args.d else dictionary_list
            report["dictionaries"] = {}

            sys.stderr.write("Evaluating %d dictionaries\n" % len(dictionaries))

            for dictionary in dictionaries:
                sys.stderr.write("Evaluating %s" % dictionary)

                for entry_metric in entry_metrics:
                    entry_metric.reset()

                dict_report = {}
                report["dictionaries"][dictionary] = dict_report

                metadata = Metadata(api_instance.about(dictionary))

                if metadata.errors:
                    dict_report["metadataErrors"] = metadata.errors
                else:
                    for metadata_metric in metadata_metrics:
                        dict_report.update(metadata_metric.apply(metadata))

                offset = 0
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
                for entry_metric in entry_metrics:
                    dict_report.update(entry_metric.result())

        except RequestException as e:
            report["available"] = False

        print(json.dumps(report))
