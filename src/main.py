import argparse
import sys
from metrics.base import FormsPerEntryMetric
import json
from elexis_client.api import ApiClient
from elexis_client.model import Metadata, Entry, JsonEntry
from requests.exceptions import RequestException

LIMIT = 100

metadata_metrics = []

entry_metrics = [FormsPerEntryMetric()]

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

    args = argparser.parse_args()
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

            for dictionary in dictionaries:
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
                while True:
                    entries = api_instance.list(dictionary, limit=LIMIT, offset=offset)
                    if not entries:
                        break

                    for entry in entries:
                        entry = Entry(entry)
                        if entry.errors:
                            if "entryErrors" not in dict_report:
                                dict_report["entryErrors"] = []
                            dict_report["entryErrors"].extend(entry.errors)
                        else:
                            entry_report(api_instance, dictionary, entry, 
                                    dict_report)

                    offset += LIMIT
                for entry_metric in entry_metrics:
                    dict_report.update(entry_metric.result())
                
        except RequestException as e:
            report["available"] = False

        print(json.dumps(report))
