# coding: utf-8

"""
    Humanloop API

    The Humanloop API allows you to interact with Humanloop from your product or service.  You can do this through HTTP requests from any language or via our official Python or TypeScript SDK.  To install the official [Python SDK](https://pypi.org/project/humanloop/), run the following command:  ```bash pip install humanloop ```  To install the official [TypeScript SDK](https://www.npmjs.com/package/humanloop), run the following command:  ```bash npm i humanloop ```  ---  Guides and further details about key concepts can be found in [our docs](https://docs.humanloop.com/).

    The version of the OpenAPI document: 4.0.1
    Generated by: https://konfigthis.com
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from humanloop import schemas  # noqa: F401


class ChatResponse(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Overwrite GenerateResponse for chat.
    """


    class MetaOapg:
        required = {
            "data",
            "provider_responses",
        }
        
        class properties:
            
            
            class data(
                schemas.ListSchema
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['ChatDataResponse']:
                        return ChatDataResponse
            
                def __new__(
                    cls,
                    arg: typing.Union[typing.Tuple['ChatDataResponse'], typing.List['ChatDataResponse']],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'data':
                    return super().__new__(
                        cls,
                        arg,
                        _configuration=_configuration,
                    )
            
                def __getitem__(self, i: int) -> 'ChatDataResponse':
                    return super().__getitem__(i)
        
            @staticmethod
            def provider_responses() -> typing.Type['ChatResponseProviderResponses']:
                return ChatResponseProviderResponses
            project_id = schemas.StrSchema
            num_samples = schemas.IntSchema
            logprobs = schemas.IntSchema
            suffix = schemas.StrSchema
            user = schemas.StrSchema
        
            @staticmethod
            def usage() -> typing.Type['Usage']:
                return Usage
            metadata = schemas.DictSchema
            provider_request = schemas.DictSchema
            session_id = schemas.StrSchema
            
            
            class tool_choice(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    
                    
                    class any_of_0(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                        
                        @schemas.classproperty
                        def NONE(cls):
                            return cls("none")
                    
                    
                    class any_of_1(
                        schemas.EnumBase,
                        schemas.StrSchema
                    ):
                        
                        @schemas.classproperty
                        def AUTO(cls):
                            return cls("auto")
                    
                    @classmethod
                    @functools.lru_cache()
                    def any_of(cls):
                        # we need this here to make our import statements work
                        # we must store _composed_schemas in here so the code is only run
                        # when we invoke this method. If we kept this at the class
                        # level we would get an error because the class level
                        # code would be run when this module is imported, and these composed
                        # classes don't exist yet because their module has not finished
                        # loading
                        return [
                            cls.any_of_0,
                            cls.any_of_1,
                            ToolChoice,
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'tool_choice':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            __annotations__ = {
                "data": data,
                "provider_responses": provider_responses,
                "project_id": project_id,
                "num_samples": num_samples,
                "logprobs": logprobs,
                "suffix": suffix,
                "user": user,
                "usage": usage,
                "metadata": metadata,
                "provider_request": provider_request,
                "session_id": session_id,
                "tool_choice": tool_choice,
            }
    
    data: MetaOapg.properties.data
    provider_responses: 'ChatResponseProviderResponses'
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["data"]) -> MetaOapg.properties.data: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider_responses"]) -> 'ChatResponseProviderResponses': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["project_id"]) -> MetaOapg.properties.project_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["num_samples"]) -> MetaOapg.properties.num_samples: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["logprobs"]) -> MetaOapg.properties.logprobs: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["suffix"]) -> MetaOapg.properties.suffix: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["user"]) -> MetaOapg.properties.user: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["usage"]) -> 'Usage': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider_request"]) -> MetaOapg.properties.provider_request: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["session_id"]) -> MetaOapg.properties.session_id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["tool_choice"]) -> MetaOapg.properties.tool_choice: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["data", "provider_responses", "project_id", "num_samples", "logprobs", "suffix", "user", "usage", "metadata", "provider_request", "session_id", "tool_choice", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["data"]) -> MetaOapg.properties.data: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider_responses"]) -> 'ChatResponseProviderResponses': ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["project_id"]) -> typing.Union[MetaOapg.properties.project_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["num_samples"]) -> typing.Union[MetaOapg.properties.num_samples, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["logprobs"]) -> typing.Union[MetaOapg.properties.logprobs, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["suffix"]) -> typing.Union[MetaOapg.properties.suffix, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["user"]) -> typing.Union[MetaOapg.properties.user, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["usage"]) -> typing.Union['Usage', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider_request"]) -> typing.Union[MetaOapg.properties.provider_request, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["session_id"]) -> typing.Union[MetaOapg.properties.session_id, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["tool_choice"]) -> typing.Union[MetaOapg.properties.tool_choice, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["data", "provider_responses", "project_id", "num_samples", "logprobs", "suffix", "user", "usage", "metadata", "provider_request", "session_id", "tool_choice", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        data: typing.Union[MetaOapg.properties.data, list, tuple, ],
        provider_responses: 'ChatResponseProviderResponses',
        project_id: typing.Union[MetaOapg.properties.project_id, str, schemas.Unset] = schemas.unset,
        num_samples: typing.Union[MetaOapg.properties.num_samples, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        logprobs: typing.Union[MetaOapg.properties.logprobs, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        suffix: typing.Union[MetaOapg.properties.suffix, str, schemas.Unset] = schemas.unset,
        user: typing.Union[MetaOapg.properties.user, str, schemas.Unset] = schemas.unset,
        usage: typing.Union['Usage', schemas.Unset] = schemas.unset,
        metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        provider_request: typing.Union[MetaOapg.properties.provider_request, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        session_id: typing.Union[MetaOapg.properties.session_id, str, schemas.Unset] = schemas.unset,
        tool_choice: typing.Union[MetaOapg.properties.tool_choice, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ChatResponse':
        return super().__new__(
            cls,
            *args,
            data=data,
            provider_responses=provider_responses,
            project_id=project_id,
            num_samples=num_samples,
            logprobs=logprobs,
            suffix=suffix,
            user=user,
            usage=usage,
            metadata=metadata,
            provider_request=provider_request,
            session_id=session_id,
            tool_choice=tool_choice,
            _configuration=_configuration,
            **kwargs,
        )

from humanloop.model.chat_data_response import ChatDataResponse
from humanloop.model.chat_response_provider_responses import ChatResponseProviderResponses
from humanloop.model.tool_choice import ToolChoice
from humanloop.model.usage import Usage
