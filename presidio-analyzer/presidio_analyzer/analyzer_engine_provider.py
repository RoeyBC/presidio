import yaml
import os
import logging
from pathlib import Path
from typing import Optional, Union, List, Tuple, Dict, Any

from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, EntityRecognizer, PatternRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider, NlpEngine
from presidio_analyzer.recognizer_registry import RecognizerRegistry
from presidio_analyzer.recognizer_registry_provider import RecognizerRegistryProvider

logger = logging.getLogger("presidio-analyzer")


class AnalyzerEngineProvider:
    """
    Utility function for loading Presidio Analyzer.

    Use this class to load presidio analyzer engine from a yaml file
    """

    def __init__(self, conf_file: Optional[Union[Path, str]] = None):
        self.configuration = {}
        if not conf_file or not os.path.exists(conf_file):
            logger.warning(
                "configuration file is missing. Using default configuration for analyzer engine"
            )
            return
        
        self.configuration = yaml.safe_load(open(conf_file))
        return


    def create_engine(self) -> AnalyzerEngine:
        """
        loads Presidio Analyzer from yaml configuration file.

        :return: analyzer engine initialized with yaml configuration
        """

        nlp_engine = self._load_nlp_engine()
        registry = self._load_recognizer_registry()
        supported_languages = "en"
        default_score_threshold = 0
        if "analyzer_engine" not in self.configuration:
            logger.warning(
                "configuration file is missing 'analyzer_engine'. Using default configuration for analyzer engine"
                )
        else:
            supported_languages = self.configuration.get("supported_languages", "en")
            default_score_threshold = self.configuration.get("default_score_threshold", 0)

        analyzer = AnalyzerEngine(
            nlp_engine=nlp_engine, 
            registry=registry,
            supported_languages=supported_languages,
            default_score_threshold=default_score_threshold
        )

        return analyzer

    def _load_recognizer_registry(self) -> RecognizerRegistry:
        if "recognizer_registry" not in self.configuration:
            logger.warning(
                "configuration file is missing 'recognizer_registry'. Using default configuration for recognizer registry"
            )
            return None
        registry_configuration = self.configuration["recognizer_registry"]
        provider = RecognizerRegistryProvider(registry_configuration=registry_configuration)
        return provider.create_engine_recognizer_registry()
    
    def _load_nlp_engine(self) -> NlpEngine:
        if "nlp_configuration" not in self.configuration:
            logger.warning(
                "configuration file is missing 'nlp_configuration'. Using default configuration for nlp engine"
            )
            return None
        nlp_configuration = self.configuration["nlp_configuration"]
        provider = NlpEngineProvider(nlp_configuration=nlp_configuration)
        return provider.create_engine()