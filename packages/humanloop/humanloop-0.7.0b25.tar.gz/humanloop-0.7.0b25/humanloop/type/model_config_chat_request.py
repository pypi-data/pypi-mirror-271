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

from humanloop.type.chat_message_with_tool_call import ChatMessageWithToolCall
from humanloop.type.model_config_chat_request_tools import ModelConfigChatRequestTools
from humanloop.type.model_endpoints import ModelEndpoints
from humanloop.type.model_providers import ModelProviders
from humanloop.type.response_format import ResponseFormat

class RequiredModelConfigChatRequest(TypedDict):
    # The model instance used. E.g. text-davinci-002.
    model: str

class OptionalModelConfigChatRequest(TypedDict, total=False):
    # A description of the model config.
    description: str

    # A friendly display name for the model config. If not provided, a name will be generated.
    name: str

    # The company providing the underlying model service.
    provider: ModelProviders

    # The maximum number of tokens to generate. Provide max_tokens=-1 to dynamically calculate the maximum number of tokens to generate given the length of the prompt
    max_tokens: int

    # What sampling temperature to use when making a generation. Higher values means the model will be more creative.
    temperature: typing.Union[int, float]

    # An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass.
    top_p: typing.Union[int, float]

    # The string (or list of strings) after which the model will stop generating. The returned text will not contain the stop sequence.
    stop: typing.Union[str, typing.List[str]]

    # Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the generation so far.
    presence_penalty: typing.Union[int, float]

    # Number between -2.0 and 2.0. Positive values penalize new tokens based on how frequently they appear in the generation so far.
    frequency_penalty: typing.Union[int, float]

    # Other parameter values to be passed to the provider call.
    other: typing.Dict[str, typing.Union[bool, date, datetime, dict, float, int, list, str, None]]

    # If specified, model will make a best effort to sample deterministically, but it is not guaranteed.
    seed: int

    # The format of the response. Only type json_object is currently supported for chat.
    response_format: ResponseFormat

    # The provider model endpoint used.
    endpoint: ModelEndpoints

    # Messages prepended to the list of messages sent to the provider. These messages that will take your specified inputs to form your final request to the provider model. Input variables within the template should be specified with syntax: {{INPUT_NAME}}.
    chat_template: typing.List[ChatMessageWithToolCall]

    tools: ModelConfigChatRequestTools

class ModelConfigChatRequest(RequiredModelConfigChatRequest, OptionalModelConfigChatRequest):
    pass
