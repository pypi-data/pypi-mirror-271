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

from humanloop.type.feedback_class import FeedbackClass
from humanloop.type.feedback_label_request import FeedbackLabelRequest

RequiredFeedbackTypeRequest = TypedDict("RequiredFeedbackTypeRequest", {
    # The type of feedback to update.
    "type": str,
    })

OptionalFeedbackTypeRequest = TypedDict("OptionalFeedbackTypeRequest", {
    # The feedback values to be available. This field should only be populated when updating a 'select' or 'multi_select' feedback class.
    "values": typing.List[FeedbackLabelRequest],

    # The data type associated to this feedback type; whether it is a 'text'/'select'/'multi_select'. This is optional when updating the default feedback types (i.e. when `type` is 'rating', 'action' or 'issue').
    "class": FeedbackClass,
    }, total=False)

class FeedbackTypeRequest(RequiredFeedbackTypeRequest, OptionalFeedbackTypeRequest):
    pass
