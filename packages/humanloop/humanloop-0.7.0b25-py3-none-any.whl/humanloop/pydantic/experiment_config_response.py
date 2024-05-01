# coding: utf-8

"""
    Humanloop API

    The Humanloop API allows you to interact with Humanloop from your product or service.  You can do this through HTTP requests from any language or via our official Python or TypeScript SDK.  To install the official [Python SDK](https://pypi.org/project/humanloop/), run the following command:  ```bash pip install humanloop ```  To install the official [TypeScript SDK](https://www.npmjs.com/package/humanloop), run the following command:  ```bash npm i humanloop ```  ---  Guides and further details about key concepts can be found in [our docs](https://docs.humanloop.com/).

    The version of the OpenAPI document: 4.0.1
    Generated by: https://konfigthis.com
"""

from datetime import datetime, date
import typing
from enum import Enum
from typing_extensions import TypedDict, Literal, TYPE_CHECKING
from pydantic import BaseModel, Field, RootModel, ConfigDict

from humanloop.pydantic.config_response import ConfigResponse

class ExperimentConfigResponse(BaseModel):
    # Number of datapoints with feedback associated to the experiment.
    trials_count: int = Field(alias='trials_count')

    # Whether the model config is active in the experiment. Only active model configs can be sampled from the experiment.
    active: bool = Field(alias='active')

    # String ID of model config. Starts with `config_`.
    id: str = Field(alias='id')

    # Display name of model config. If this is not set by the user, a friendly name is generated.
    display_name: str = Field(alias='display_name')

    # Definition of the config used in the experiment.
    config: ConfigResponse = Field(alias='config')

    created_at: datetime = Field(alias='created_at')

    updated_at: datetime = Field(alias='updated_at')

    # The mean performance of the model config.
    mean: typing.Optional[typing.Union[int, float]] = Field(None, alias='mean')

    # The spread of performance of the model config.
    spread: typing.Optional[typing.Union[int, float]] = Field(None, alias='spread')

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True
    )
