import argparse
import csv
import json
import sys
from collections import OrderedDict
from typing import List, Dict

from wai.logging import LOGGING_WARNING

from idc.api import ImageClassificationData, ObjectDetectionData, ImageSegmentationData, StreamWriter, \
    make_list, LABEL_KEY

OUTPUT_FORMAT_TEXT = "text"
OUTPUT_FORMAT_CSV = "csv"
OUTPUT_FORMAT_JSON = "json"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_TEXT,
    OUTPUT_FORMAT_CSV,
    OUTPUT_FORMAT_JSON,
]


class LabelDistributionWriter(StreamWriter):
    """
    Collects the labels and outputs their distribution.
    """

    def __init__(self, output_file: str = None, output_format: str = OUTPUT_FORMAT_TEXT,
                 label_key: str = LABEL_KEY, percentages: bool = False,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param output_file: the output file to save the label distribution to
        :type output_file: str
        :param output_format: the format for the output file
        :type output_format: str
        :param label_key: the key in the object detection metadata that contains the label
        :type label_key: str
        :param percentages: whether to output percentages or absolute counts
        :type percentages: bool
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.output_format = output_format
        self.label_key = label_key
        self.percentages = percentages
        self._labels = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "label-dist"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Collects the labels and outputs their distribution."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output_file", type=str, help="The file to write the statistics to; uses stdout if omitted.", required=False, default=None)
        parser.add_argument("-f", "--output_format", type=str, help="The format to use for the output, available formats: %s" % ", ".join(OUTPUT_FORMATS), required=False, default=OUTPUT_FORMAT_TEXT)
        parser.add_argument("-k", "--label_key", type=str, help="The key in the (object detection) meta-data that contains the label.", required=False, default=LABEL_KEY)
        parser.add_argument("-p", "--percentages", action="store_true", help="Whether to output percentages instead of counts.", required=False)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_file = ns.output_file
        self.output_format = ns.output_format
        self.label_key = ns.label_key
        self.percentages = ns.percentages

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData, ObjectDetectionData, ImageSegmentationData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.output_format is None:
            raise Exception("No output format defined!")
        if (self.label_key is None) or (self.label_key == ""):
            self.label_key = LABEL_KEY
        if self.percentages is None:
            self.percentages = False
        self._labels = dict()

    def add_label(self, label: str):
        """
        Increments the count for the label.
        """
        if label not in self._labels:
            self._labels[label] = 0

        self._labels[label] = self._labels[label] + 1

    def output_text(self, dist: Dict, keys: List, use_stdout: bool):
        """
        Outputs the label distribution in simple textual format.

        :param dist: the distribution dictionary
        :type dist: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            for k in keys:
                if self.percentages:
                    print("%s: %f" % (k, dist[k]))
                else:
                    print("%s: %d" % (k, dist[k]))
        else:
            with open(self.output_file, "w") as f:
                for k in keys:
                    if self.percentages:
                        f.write("%s: %f" % (k, dist[k]))
                    else:
                        f.write("%s: %d" % (k, dist[k]))
                    f.write("\n")

    def output_csv(self, dist: Dict, keys: List, use_stdout: bool):
        """
        Outputs the label distribution in CSV format.

        :param dist: the distribution dictionary
        :type dist: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            writer = csv.writer(sys.stdout)
            f = None
        else:
            f = open(self.output_file, "w")
            writer = csv.writer(f)

        writer.writerow(["Label", "Percent" if self.percentages else "Count"])
        for k in keys:
            writer.writerow([k, dist[k]])

        if f is not None:
            f.close()

    def output_json(self, dist: Dict, use_stdout: bool):
        """
        Outputs the label distribution in json format.

        :param dist: the distribution dictionary
        :type dist: dict
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        if use_stdout:
            print(json.dumps(dist, indent=2))
        else:
            with open(self.output_file, "w") as f:
                json.dump(dist, f, indent=2)

    def output_label_distribution(self):
        """
        Outputs the distribution.
        """
        keys = list(self._labels.keys())
        keys.sort()
        dist = OrderedDict()
        for k in keys:
            dist[k] = self._labels[k]

        if self.percentages:
            total = 0
            for k in dist:
                total += dist[k]
            for k in dist:
                dist[k] = dist[k] / total * 100.0

        use_stdout = (self.output_file is None) or (len(self.output_file) == 0)

        if self.output_format == OUTPUT_FORMAT_TEXT:
            self.output_text(dist, keys, use_stdout)
        elif self.output_format == OUTPUT_FORMAT_CSV:
            self.output_csv(dist, keys, use_stdout)
        elif self.output_format == OUTPUT_FORMAT_JSON:
            self.output_json(dist, use_stdout)
        else:
            raise Exception("Unhandled output format: %s" % self.output_format)

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            if isinstance(item, ImageClassificationData):
                self.add_label(item.annotation.label)
            elif isinstance(item, ObjectDetectionData):
                for obj in item.annotation:
                    if self.label_key in obj.metadata:
                        self.add_label(obj.metadata[self.label_key])
            elif isinstance(item, ImageSegmentationData):
                for label in item.annotation.layers:
                    self.add_label(label)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.output_label_distribution()
