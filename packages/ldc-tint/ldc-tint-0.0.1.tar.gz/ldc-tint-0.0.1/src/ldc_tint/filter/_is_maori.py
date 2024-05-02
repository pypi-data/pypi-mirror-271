import argparse
import re
from typing import List, Union

from wai.logging import LOGGING_WARNING
from ldc.core import DOMAIN_PRETRAIN, DOMAIN_PAIRS, DOMAIN_CLASSIFICATION
from ldc.core import LOCATION_ANY, LOCATION_INSTRUCTION, LOCATION_INPUT, LOCATION_OUTPUT, LOCATION_CONTENT, \
    LOCATION_TEXT, LOCATIONS, locations_match, add_location_argument
from ldc.api import Filter, FILTER_ACTIONS, FILTER_ACTION_KEEP, FILTER_ACTION_DISCARD
from ldc.api.pretrain import PretrainData
from ldc.api.supervised.classification import ClassificationData
from ldc.api.supervised.pairs import PairData
from reo_toolkit import is_maori


class IsMaori(Filter):
    """
    Detects whether text is Māori or not, either in strict or weak mode.
    """

    def __init__(self, min_maori: float = 0.0, strict: bool = False, action: str = FILTER_ACTION_KEEP,
                 location: Union[str, List[str]] = LOCATION_ANY,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the filter.

        :param min_maori: the minimum required ratio of Māori words (0-1)
        :type min_maori: float
        :param strict: whether to use a strict evaluation
        :type strict: bool
        :param action: the action to apply to the data records
        :type action: str
        :param location: which part of the data to check
        :type location: str or list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)

        if action not in FILTER_ACTIONS:
            raise Exception("Invalid action: %s" % action)

        if location not in LOCATIONS:
            raise Exception("Invalid location: %s" % location)

        self.min_maori = min_maori
        self.strict = strict
        self.location = location
        self.action = action

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "is-maori"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Determines whether text is Māori or not (weak or strict mode), using the supplied threshold. The filter action then determines what to do with the record."

    def domains(self) -> List[str]:
        """
        Returns the domains of the filter.

        :return: the domains
        :rtype: list
        """
        return [DOMAIN_PRETRAIN, DOMAIN_PAIRS, DOMAIN_CLASSIFICATION]

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [PretrainData, PairData, ClassificationData]

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [PretrainData, PairData, ClassificationData]

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-m", "--min_maori", type=float, default=0.0, help="The minimum required ratio (0-1) of Māori words in the text.")
        parser.add_argument("-s", "--strict", action="store_true", help="Whether to use strict mode rather than weak one.")
        add_location_argument(parser, "Which data to check")
        parser.add_argument("-a", "--action", choices=FILTER_ACTIONS, default=FILTER_ACTION_KEEP, help="How to react when the thresholds are met")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.min_maori = ns.min_maori
        self.strict = ns.strict
        self.location = ns.location
        self.action = ns.action

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()

        if isinstance(self.location, str):
            self.location = [self.location]

    def _evaluate(self, content: str) -> float:
        """
        Evaluates the text.

        :param content: the text to evaluate
        :type content: str
        :return: the determined ratio of maori words
        :rtype: float
        """
        if content is None:
            return 0.0

        # evaluate all words
        text = content.strip()
        splitter = re.compile(r'[\s\n\-]+')
        if splitter.search(text):
            evals = []
            # Split the text and evaluate each piece
            for split in splitter.split(text):
                if len(split) > 0:
                    evals.append(is_maori(split, strict=self.strict))
        else:
            evals = [is_maori(content, strict=self.strict)]

        if len(evals) > 0:
            ratio = evals.count(True) / len(evals)
        else:
            ratio = 0.0
        return ratio

    def _do_process(self, data):
        """
        Processes the data record.

        :param data: the record to process
        :return: the potentially updated record or None if to drop
        """
        result = data

        ratios = dict()
        if isinstance(data, PretrainData):
            if locations_match(self.location, LOCATION_CONTENT):
                ratios[LOCATION_CONTENT] = self._evaluate(data.content)
        elif isinstance(data, ClassificationData):
            if locations_match(self.location, LOCATION_TEXT):
                ratios[LOCATION_TEXT] = self._evaluate(data.text)
        elif isinstance(data, PairData):
            if locations_match(self.location, LOCATION_INSTRUCTION):
                ratios[LOCATION_INSTRUCTION] = self._evaluate(data.instruction)
            if locations_match(self.location, LOCATION_INPUT):
                ratios[LOCATION_INPUT] = self._evaluate(data.input)
            if locations_match(self.location, LOCATION_OUTPUT):
                ratios[LOCATION_OUTPUT] = self._evaluate(data.output)
        else:
            raise Exception("Unhandled type of data: %s" % str(type(data)))

        for key in ratios:
            ratio = ratios[key]
            if ratio >= self.min_maori:
                if self.action == FILTER_ACTION_DISCARD:
                    result = None
            else:
                if self.action == FILTER_ACTION_KEEP:
                    result = None
            if result is None:
                break

        self.logger().info("ratios=%s, forward=%s" % (str(ratios), (result is not None)))

        return result
