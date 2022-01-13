import argparse
import sys

from edie.evaluator import Edie
from metrics.base import FormsPerEntryMetric, NumberOfSensesEvaluator, DefinitionOfSenseEvaluator, \
    AvgDefinitionLengthEvaluator
import json
from edie.api import ApiClient
from edie.model import Dictionary
import logging

logging.basicConfig(level=logging.DEBUG)

LIMIT = 100

metadata_evaluators = []

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
        edie = Edie(api_instance)

        dictionaries: [Dictionary] = edie.load_dictionaries(args.d)
        metadata_report = edie.evaluate_metadata()
        entry_report = edie.evaluate_entries(10)
        logging.info(json.dumps(edie.evaluation_report()))