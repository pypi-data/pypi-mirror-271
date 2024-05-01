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


class ModelConfigCompletionRequest(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)

    Completion model config request
    """


    class MetaOapg:
        required = {
            "model",
            "prompt_template",
        }
        
        class properties:
            model = schemas.StrSchema
            prompt_template = schemas.StrSchema
            description = schemas.StrSchema
            name = schemas.StrSchema
        
            @staticmethod
            def provider() -> typing.Type['ModelProviders']:
                return ModelProviders
            max_tokens = schemas.IntSchema
            temperature = schemas.NumberSchema
            top_p = schemas.NumberSchema
            
            
            class stop(
                schemas.ComposedSchema,
            ):
            
            
                class MetaOapg:
                    any_of_0 = schemas.StrSchema
                    
                    
                    class any_of_1(
                        schemas.ListSchema
                    ):
                    
                    
                        class MetaOapg:
                            items = schemas.StrSchema
                    
                        def __new__(
                            cls,
                            arg: typing.Union[typing.Tuple[typing.Union[MetaOapg.items, str, ]], typing.List[typing.Union[MetaOapg.items, str, ]]],
                            _configuration: typing.Optional[schemas.Configuration] = None,
                        ) -> 'any_of_1':
                            return super().__new__(
                                cls,
                                arg,
                                _configuration=_configuration,
                            )
                    
                        def __getitem__(self, i: int) -> MetaOapg.items:
                            return super().__getitem__(i)
                    
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
                        ]
            
            
                def __new__(
                    cls,
                    *args: typing.Union[dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'stop':
                    return super().__new__(
                        cls,
                        *args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            presence_penalty = schemas.NumberSchema
            frequency_penalty = schemas.NumberSchema
            other = schemas.DictSchema
            seed = schemas.IntSchema
        
            @staticmethod
            def response_format() -> typing.Type['ResponseFormat']:
                return ResponseFormat
        
            @staticmethod
            def endpoint() -> typing.Type['ModelEndpoints']:
                return ModelEndpoints
            __annotations__ = {
                "model": model,
                "prompt_template": prompt_template,
                "description": description,
                "name": name,
                "provider": provider,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "stop": stop,
                "presence_penalty": presence_penalty,
                "frequency_penalty": frequency_penalty,
                "other": other,
                "seed": seed,
                "response_format": response_format,
                "endpoint": endpoint,
            }
    
    model: MetaOapg.properties.model
    prompt_template: MetaOapg.properties.prompt_template
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["model"]) -> MetaOapg.properties.model: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["prompt_template"]) -> MetaOapg.properties.prompt_template: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["provider"]) -> 'ModelProviders': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["max_tokens"]) -> MetaOapg.properties.max_tokens: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["temperature"]) -> MetaOapg.properties.temperature: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["top_p"]) -> MetaOapg.properties.top_p: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["stop"]) -> MetaOapg.properties.stop: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["presence_penalty"]) -> MetaOapg.properties.presence_penalty: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["frequency_penalty"]) -> MetaOapg.properties.frequency_penalty: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["other"]) -> MetaOapg.properties.other: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["seed"]) -> MetaOapg.properties.seed: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["response_format"]) -> 'ResponseFormat': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["endpoint"]) -> 'ModelEndpoints': ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["model", "prompt_template", "description", "name", "provider", "max_tokens", "temperature", "top_p", "stop", "presence_penalty", "frequency_penalty", "other", "seed", "response_format", "endpoint", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["model"]) -> MetaOapg.properties.model: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["prompt_template"]) -> MetaOapg.properties.prompt_template: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> typing.Union[MetaOapg.properties.name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["provider"]) -> typing.Union['ModelProviders', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["max_tokens"]) -> typing.Union[MetaOapg.properties.max_tokens, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["temperature"]) -> typing.Union[MetaOapg.properties.temperature, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["top_p"]) -> typing.Union[MetaOapg.properties.top_p, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["stop"]) -> typing.Union[MetaOapg.properties.stop, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["presence_penalty"]) -> typing.Union[MetaOapg.properties.presence_penalty, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["frequency_penalty"]) -> typing.Union[MetaOapg.properties.frequency_penalty, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["other"]) -> typing.Union[MetaOapg.properties.other, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["seed"]) -> typing.Union[MetaOapg.properties.seed, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["response_format"]) -> typing.Union['ResponseFormat', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["endpoint"]) -> typing.Union['ModelEndpoints', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["model", "prompt_template", "description", "name", "provider", "max_tokens", "temperature", "top_p", "stop", "presence_penalty", "frequency_penalty", "other", "seed", "response_format", "endpoint", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        model: typing.Union[MetaOapg.properties.model, str, ],
        prompt_template: typing.Union[MetaOapg.properties.prompt_template, str, ],
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        name: typing.Union[MetaOapg.properties.name, str, schemas.Unset] = schemas.unset,
        provider: typing.Union['ModelProviders', schemas.Unset] = schemas.unset,
        max_tokens: typing.Union[MetaOapg.properties.max_tokens, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        temperature: typing.Union[MetaOapg.properties.temperature, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        top_p: typing.Union[MetaOapg.properties.top_p, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        stop: typing.Union[MetaOapg.properties.stop, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, schemas.Unset] = schemas.unset,
        presence_penalty: typing.Union[MetaOapg.properties.presence_penalty, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        frequency_penalty: typing.Union[MetaOapg.properties.frequency_penalty, decimal.Decimal, int, float, schemas.Unset] = schemas.unset,
        other: typing.Union[MetaOapg.properties.other, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        seed: typing.Union[MetaOapg.properties.seed, decimal.Decimal, int, schemas.Unset] = schemas.unset,
        response_format: typing.Union['ResponseFormat', schemas.Unset] = schemas.unset,
        endpoint: typing.Union['ModelEndpoints', schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ModelConfigCompletionRequest':
        return super().__new__(
            cls,
            *args,
            model=model,
            prompt_template=prompt_template,
            description=description,
            name=name,
            provider=provider,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=stop,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            other=other,
            seed=seed,
            response_format=response_format,
            endpoint=endpoint,
            _configuration=_configuration,
            **kwargs,
        )

from humanloop.model.model_endpoints import ModelEndpoints
from humanloop.model.model_providers import ModelProviders
from humanloop.model.response_format import ResponseFormat
