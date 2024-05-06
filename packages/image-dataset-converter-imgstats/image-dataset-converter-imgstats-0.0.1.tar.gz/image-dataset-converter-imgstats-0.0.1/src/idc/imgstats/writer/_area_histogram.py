import argparse
import csv
import json
import numpy as np
import sys
import termplotlib as tpl
from collections import OrderedDict
from typing import List, Dict

from wai.logging import LOGGING_WARNING

from idc.api import ObjectDetectionData, ImageSegmentationData, StreamWriter, \
    make_list, LABEL_KEY

OUTPUT_FORMAT_TEXT = "text"
OUTPUT_FORMAT_CSV = "csv"
OUTPUT_FORMAT_JSON = "json"
OUTPUT_FORMATS = [
    OUTPUT_FORMAT_TEXT,
    OUTPUT_FORMAT_CSV,
    OUTPUT_FORMAT_JSON,
]


class AreaHistogramWriter(StreamWriter):
    """
    Collects the labels and outputs their distribution.
    """

    def __init__(self, output_file: str = None, output_format: str = OUTPUT_FORMAT_TEXT,
                 label_key: str = LABEL_KEY, num_bins: int = None, force_bbox: bool = False,
                 normalized: bool = False, all_label: str = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param output_file: the file to write the histogram to; uses stdout if omitted
        :type output_file: str
        :param output_format: the format for the output file
        :type output_format: str
        :param label_key: the key in the object detection metadata that contains the label
        :type label_key: str
        :param num_bins: the number of bins to use for the histogram
        :type num_bins: int
        :param force_bbox: whether to use the bounding box even if a polygon is present (object detection domain only)
        :type force_bbox: bool
        :param normalized: whether to use normalized areas (using the image size as base)
        :type normalized: bool
        :param all_label: the label to use for all the labels combined
        :type all_label: str
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.output_file = output_file
        self.output_format = output_format
        self.label_key = label_key
        self.num_bins = num_bins
        self.force_bbox = force_bbox
        self.normalized = normalized
        self.all_label = all_label
        self._data = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "area-histogram"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Generates histograms of the area (normalized or absolute) occupied by the annotations."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output_file", type=str, help="The file to write the statistics to; uses stdout if omitted.", required=False, default=None)
        parser.add_argument("-f", "--output_format", type=str, help="The format to use for the output, available modes: %s" % ", ".join(OUTPUT_FORMATS), required=False, default=OUTPUT_FORMAT_TEXT)
        parser.add_argument("-k", "--label_key", type=str, help="The key in the (object detection) meta-data that contains the label.", required=False, default=LABEL_KEY)
        parser.add_argument("-B", "--num_bins", type=int, help="The number of bins to use for the histogram.", required=False, default=20)
        parser.add_argument("-b", "--force_bbox", action="store_true", help="Whether to use the bounding box even if a polygon is present (object detection domain only)", required=False)
        parser.add_argument("-n", "--normalized", action="store_true", help="Whether to use normalized areas (using the image size as base)", required=False)
        parser.add_argument("-a", "--all_label", metavar="LABEL", type=str, help="The label to use for all the labels combined.", required=False, default="ALL")
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
        self.num_bins = ns.num_bins
        self.force_bbox = ns.force_bbox
        self.normalized = ns.normalized
        self.all_label = ns.all_label

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData, ImageSegmentationData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.output_format is None:
            raise Exception("No output format defined!")
        if (self.label_key is None) or (self.label_key == ""):
            self.label_key = LABEL_KEY
        if self.num_bins is None:
            self.num_bins = 20
        if self.force_bbox is None:
            self.force_bbox = False
        if self.normalized is None:
            self.normalized = False
        if self.all_label is None:
            self.all_label = "ALL"
        self._data = dict()

    def append_value(self, label: str, value):
        """
        Appends a value to the label.
        """
        if "" not in self._data:
            self._data[""] = []
        if label not in self._data:
            self._data[label] = []

        if value <= 0:
            self.logger().warning("Invalid area (%s): %f" % (label, value))

        if label != "":
            self._data[""].append(value)
        self._data[label].append(value)

    def create_all_label(self, labels: List[str]) -> str:
        """
        Creates a unique label for "all".

        :param labels: the labels used in the dataset
        :type labels: list
        :return: the generated all label
        :rtype: str
        """
        result = self.all_label
        label_set = set(labels)
        while result in label_set:
            result = "_" + result + "_"
        return result

    def output_text(self, histograms: Dict, keys: List[str], use_stdout: bool):
        """
        Outputs the label distribution in simple textual format.

        :param histograms: the distribution dictionary (counts, bin_edges tuple)
        :type histograms: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        plots = ""
        for k in keys:
            if k == "":
                label = self.create_all_label(keys)
            else:
                label = k
            plots += label + ":\n\n"
            counts, bin_edges = histograms[k]
            fig = tpl.figure()
            fig.hist(counts, bin_edges, orientation="horizontal", force_ascii=False)
            plots += fig.get_string() + "\n\n"

        if use_stdout:
            print(plots)
        else:
            with open(self.output_file, "w") as fp:
                fp.write(plots)

    def output_csv(self, histograms: Dict, keys: List[str], use_stdout: bool):
        """
        Outputs the label distribution in CSV format.

        :param histograms: the distribution dictionary (counts, bin_edges tuple)
        :type histograms: dict
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

        writer.writerow(["label", "bin", "from", "to", "count"])
        for k in keys:
            if k == "":
                label = self.create_all_label(keys)
            else:
                label = k
            counts, bin_edges = histograms[k]
            for i in range(len(counts)):
                writer.writerow([label, i, bin_edges[i], bin_edges[i+1], counts[i]])

        if f is not None:
            f.close()

    def output_json(self, histograms: Dict, keys: List[str], use_stdout: bool):
        """
        Outputs the label distribution in json format.

        :param histograms: the distribution dictionary (counts, bin_edges tuple)
        :type histograms: dict
        :param keys: they sorted keys
        :type keys: list
        :param use_stdout: whether to use stdout or the file
        :type use_stdout: bool
        """
        data = []
        for k in keys:
            if k == "":
                label = self.create_all_label(keys)
            else:
                label = k
            counts, bin_edges = histograms[k]
            label_data = OrderedDict()
            label_data["label"] = label
            label_data["bins"] = []
            for i in range(len(counts)):
                bin = OrderedDict()
                bin["bin"] = i
                bin["from"] = float(bin_edges[i])
                bin["to"] = float(bin_edges[i+1])
                bin["count"] = int(counts[i])
                label_data["bins"].append(bin)
            data.append(label_data)

        if use_stdout:
            print(json.dumps(data, indent=2))
        else:
            with open(self.output_file, "w") as f:
                json.dump(data, f, indent=2)

    def output_histograms(self):
        """
        Computes and outputs the histograms.
        """
        histograms = dict()
        keys = []
        for k in self._data:
            if k != "":
                keys.append(k)
            counts, bin_edges = np.histogram(self._data[k], bins=self.num_bins)
            histograms[k] = (counts, bin_edges)

        use_stdout = (self.output_file is None) or (len(self.output_file) == 0)

        keys.sort()
        keys.insert(0, "")

        if self.output_format == "text":
            self.output_text(histograms, keys, use_stdout)
        elif self.output_format == "csv":
            self.output_csv(histograms, keys, use_stdout)
        elif self.output_format == "json":
            self.output_json(histograms, keys, use_stdout)
        else:
            raise Exception("Unhandled output format: %s" % self.output_format)

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            img_area = item.image_width * item.image_height
            if isinstance(item, ObjectDetectionData):
                for obj in item.get_absolute():
                    label = ""
                    if self.label_key in obj.metadata:
                        label = obj.metadata[self.label_key]
                    if not self.force_bbox and obj.has_polygon():
                        area = obj.get_polygon().area()
                    else:
                        area = obj.get_rectangle().area()
                    if self.normalized:
                        self.append_value(label, area / img_area)
                    else:
                        self.append_value(label, area)
            elif isinstance(item, ImageSegmentationData):
                for label in item.annotation.layers:
                    area = np.count_nonzero(item.annotation.layers[label])
                    if self.normalized:
                        self.append_value(label, area / img_area)
                    else:
                        self.append_value(label, area)

    def finalize(self):
        """
        Finishes the processing, e.g., for closing files or databases.
        """
        super().finalize()
        self.output_histograms()
