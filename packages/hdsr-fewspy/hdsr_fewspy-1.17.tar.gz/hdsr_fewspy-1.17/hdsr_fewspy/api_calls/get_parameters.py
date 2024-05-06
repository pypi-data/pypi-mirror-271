from hdsr_fewspy.api_calls.base import GetRequest
from hdsr_fewspy.constants.choices import ApiParameters
from hdsr_fewspy.constants.choices import OutputChoices
from hdsr_fewspy.constants.custom_types import ResponseType
from hdsr_fewspy.converters.utils import camel_to_snake_case
from typing import List
from typing import Union

import logging
import pandas as pd


logger = logging.getLogger(__name__)

COLUMNS = [
    "id",
    "name",
    "parameter_type",
    "unit",
    "display_unit",
    "uses_datum",
    "parameter_group",
]


class GetParameters(GetRequest):
    def __init__(self, *args, **kwargs):
        # show_attributes does not make a difference in response (both for Pi_JSON and PI_XML)
        super().__init__(*args, **kwargs)

    @property
    def url_post_fix(self) -> str:
        return "parameters"

    @property
    def allowed_request_args(self) -> List[str]:
        return [
            ApiParameters.filter_id,
            ApiParameters.document_format,
            ApiParameters.document_version,
        ]

    @property
    def required_request_args(self) -> List[str]:
        return [
            ApiParameters.filter_id,
            ApiParameters.document_format,
            ApiParameters.document_version,
        ]

    @property
    def allowed_output_choices(self) -> List[OutputChoices]:
        return [
            OutputChoices.json_response_in_memory,
            OutputChoices.xml_response_in_memory,
            OutputChoices.pandas_dataframe_in_memory,
        ]

    def run(self) -> Union[ResponseType, pd.DataFrame]:
        response = self.retry_backoff_session.get(
            url=self.url, params=self.filtered_fews_parameters, verify=self.pi_settings.ssl_verify
        )
        if self.output_choice in {OutputChoices.json_response_in_memory, OutputChoices.xml_response_in_memory}:
            return response

        assert self.output_choice == OutputChoices.pandas_dataframe_in_memory, "code error GetParameters"
        # parse the response to dataframe
        df = pd.DataFrame(columns=COLUMNS)
        if response.status_code == 200:
            if "timeSeriesParameters" in response.json().keys():
                df = pd.DataFrame(response.json()["timeSeriesParameters"])
                df.columns = [camel_to_snake_case(i) for i in df.columns]
                df["uses_datum"] = df["uses_datum"] == "true"
        else:
            logger.error(f"FEWS Server responds {response.text}")
        df.set_index("id", inplace=True)

        return df
