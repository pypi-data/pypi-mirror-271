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

from humanloop.pydantic.dashboard_configuration_model_config_ids import DashboardConfigurationModelConfigIds
from humanloop.pydantic.time_unit import TimeUnit

class DashboardConfiguration(BaseModel):
    time_unit: TimeUnit = Field(alias='time_unit')

    time_range_days: int = Field(alias='time_range_days')

    model_config_ids_: DashboardConfigurationModelConfigIds = Field(alias='model_config_ids')

    model_config = ConfigDict(
        protected_namespaces=(),
        arbitrary_types_allowed=True
    )
