import argparse
import sys
from os.path import exists
import pybars
import json

from edie.api import ApiClient
from edie.evaluator import Edie
from edie.vocabulary import Vocabulary
from edie.model import Dictionary
from metrics.entry import FormsPerEntryMetric, NumberOfSensesEvaluator, DefinitionOfSenseEvaluator, \
    SupportedFormatsEvaluator, AvgDefinitionLengthEvaluator
from metrics.metadata import PublisherEvaluator, LicenseEvaluator, MetadataQuantityEvaluator, RecencyEvaluator, \
    SizeOfDictionaryEvaluator
from rest import create_app


metadata_evaluators = [PublisherEvaluator(), LicenseEvaluator(), MetadataQuantityEvaluator(), RecencyEvaluator(),
                       SizeOfDictionaryEvaluator()]
entry_evaluators = [FormsPerEntryMetric(), NumberOfSensesEvaluator(), DefinitionOfSenseEvaluator(),
                    AvgDefinitionLengthEvaluator(), SupportedFormatsEvaluator()]


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
    argparser.add_argument("--html",
                            help="Write a human-readable HTML version of the output to this file")
    argparser.add_argument("-v",
                            help="Show verbose output")

    return argparser


if __name__ == "__main__":
    args = setup_argparser().parse_args()
    max_entries = int(args.max_entries) if args.max_entries else None

    if args.html and not exists("src/edie/edie.html"):
        print("Cannot find template for HTML output, please run from home folder")
        sys.exit(-1)

    endpoint = args.e if args.e else "http://localhost:8000/"
    api_instance = ApiClient(endpoint, args.api_key)
    edie = Edie(api_instance, metadata_metrics_evaluators=metadata_evaluators,
                entry_metrics_evaluators=entry_evaluators)
    if args.server:
        app = create_app()
        app.run()
    else:
        dictionaries, dictionary_report = edie.load_dictionaries(dictionaries=args.d if args.d else None)
        metadata_report = edie.evaluate_metadata(dictionaries)
        entry_report = edie.evaluate_entries(dictionaries, max_entries=max_entries)
        merged_report = edie.evaluation_report(dictionary_report, entry_report, metadata_report)
        report = edie.aggregated_evaluation(merged_report)

        if args.v:
            for dictionary in report['dictionaries']:
                print("Evaluation Result of Dictionary " + dictionary, end='\n')
                print("Metadata Evaluation: " + str(report['dictionaries'][dictionary]['metadata_report']), end='\n')
                print("Entry Evaluation: " + str(report['dictionaries'][dictionary]['entry_report']), end='\n')
                print('\n')

            print("=== AGGREGATION METRICS ===")
            print(report[Vocabulary.AGGREGATION_METRICS])
        else:
            print(json.dumps(report, indent=2))

        if args.html:
            def _percent(this, options, item):
                return "%.1f" % (item * 100)
            def _3dp(this, options, item):
                return "%.2f" % (item)
            compiler = pybars.Compiler()
            template = compiler.compile(open("src/edie/edie.html").read())

            with open(args.html, "w") as outp:
                outp.write(template(report, helpers={"percent":_percent,"num":_3dp}))
