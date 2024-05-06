from hdsr_fewspy.constants.choices import OutputChoices
from hdsr_fewspy.constants.custom_types import ResponseType
from hdsr_fewspy.converters.download import CsvDownloadDir
from hdsr_fewspy.converters.download import JsonDownloadDir
from hdsr_fewspy.converters.download import XmlDownloadDir
from pathlib import Path
from typing import List

import logging


logger = logging.getLogger(__name__)


class ResponseManager:
    """Relates an output_choice to the related Response Handler."""

    def __init__(self, output_choice: OutputChoices, request_class: str, output_dir: Path = None):
        self.output_choice = output_choice
        self.request_class = request_class  # e.g. gettimeseriesmulti
        self.output_dir = output_dir

    def _get_response_handler(self):
        OutputChoices.validate(output_choice=self.output_choice)
        if self.output_choice == OutputChoices.xml_file_in_download_dir:
            return XmlDownloadDir(request_class=self.request_class, output_dir=self.output_dir)
        elif self.output_choice == OutputChoices.json_file_in_download_dir:
            return JsonDownloadDir(request_class=self.request_class, output_dir=self.output_dir)
        elif self.output_choice == OutputChoices.csv_file_in_download_dir:
            return CsvDownloadDir(request_class=self.request_class, output_dir=self.output_dir)
        else:
            logger.debug(f"memory choice {self.output_choice} must be handled in GetRequest.run() itself")
            return None

    def run(self, responses: List[ResponseType], **kwargs):
        allowed_kwargs = {"file_name_values", "drop_missing_values", "flag_threshold", "only_value_and_flag"}
        kwargs_set = set(kwargs.keys())
        unexpected_kwargs = kwargs_set.difference(allowed_kwargs)
        assert not unexpected_kwargs, f"code error: found unexpected_kwargs {unexpected_kwargs}"

        response_handler = self._get_response_handler()
        return response_handler.run(responses=responses, **kwargs)
