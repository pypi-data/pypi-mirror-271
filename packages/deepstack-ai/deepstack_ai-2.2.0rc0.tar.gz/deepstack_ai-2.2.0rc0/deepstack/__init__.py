import deepstack.logging
from deepstack.core.component import component
from deepstack.core.errors import ComponentError, DeserializationError
from deepstack.core.pipeline import Pipeline, PredefinedPipeline
from deepstack.core.serialization import default_from_dict, default_to_dict
from deepstack.dataclasses import Answer, Document, ExtractedAnswer, GeneratedAnswer

# Initialize the logging configuration
# This is a no-op unless `structlog` is installed
deepstack.logging.configure_logging()

__all__ = [
    "component",
    "default_from_dict",
    "default_to_dict",
    "DeserializationError",
    "ComponentError",
    "Pipeline",
    "PredefinedPipeline",
    "Document",
    "Answer",
    "GeneratedAnswer",
    "ExtractedAnswer",
]
