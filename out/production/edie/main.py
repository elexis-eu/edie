import argparse
import sys

from edie.evaluator import Edie
from metrics.base import FormsPerEntryMetric, NumberOfSensesEvaluator, DefinitionOfSenseEvaluator, \
    AvgDefinitionLengthEvaluator, PublisherEvaluator, LicenseEvaluator, MetadataQuantityEvaluator, RecencyEvaluator
import json
from edie.api import ApiClient
from edie.model import Dictionary

metadata_evaluators = [PublisherEvaluator(), LicenseEvaluator(), MetadataQuantityEvaluator(), RecencyEvaluator()]
entry_evaluators = [FormsPerEntryMetric(), NumberOfSensesEvaluator(), DefinitionOfSenseEvaluator(),
                    AvgDefinitionLengthEvaluator()]


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


if __name__ == "__main__":
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
        edie = Edie(api_instance, metadata_metrics_evaluators=metadata_evaluators,
                    entry_metrics_evaluators=entry_evaluators)

        dictionaries: [Dictionary] = edie.load_dictionaries(args.d)
        edie.evaluate_metadata()
        edie.evaluate_entries(10)
        report = edie.evaluation_report()

        for dictionary in report['dictionaries']:
            print("Evaluation Result of Dictionary " + dictionary, end='\n')
            print("Metadata Evaluation: " + str(report['dictionaries'][dictionary]['metadata_report']), end='\n')
            print("Entry Evaluation: " + str(report['dictionaries'][dictionary]['entry_report']), end='\n')
            print('\n')
