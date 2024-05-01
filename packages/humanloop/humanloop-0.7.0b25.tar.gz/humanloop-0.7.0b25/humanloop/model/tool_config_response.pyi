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


class ToolConfigResponse(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        required = {
            "name",
            "id",
            "type",
            "status",
        }
        
        class properties:
            id = schemas.StrSchema
            
            
            class type(
                schemas.EnumBase,
                schemas.StrSchema
            ):
                
                @schemas.classproperty
                def TOOL(cls):
                    return cls("tool")
            status = schemas.StrSchema
            name = schemas.StrSchema
            description = schemas.StrSchema
            parameters = schemas.DictSchema
            other = schemas.DictSchema
        
            @staticmethod
            def created_by() -> typing.Type['UserResponse']:
                return UserResponse
        
            @staticmethod
            def source() -> typing.Type['ToolSource']:
                return ToolSource
            source_code = schemas.StrSchema
            setup_schema = schemas.DictSchema
            signature = schemas.StrSchema
            is_preset = schemas.BoolSchema
            preset_name = schemas.StrSchema
            __annotations__ = {
                "id": id,
                "type": type,
                "status": status,
                "name": name,
                "description": description,
                "parameters": parameters,
                "other": other,
                "created_by": created_by,
                "source": source,
                "source_code": source_code,
                "setup_schema": setup_schema,
                "signature": signature,
                "is_preset": is_preset,
                "preset_name": preset_name,
            }
    
    name: MetaOapg.properties.name
    id: MetaOapg.properties.id
    type: MetaOapg.properties.type
    status: MetaOapg.properties.status
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["description"]) -> MetaOapg.properties.description: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["parameters"]) -> MetaOapg.properties.parameters: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["other"]) -> MetaOapg.properties.other: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["created_by"]) -> 'UserResponse': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["source"]) -> 'ToolSource': ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["source_code"]) -> MetaOapg.properties.source_code: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["setup_schema"]) -> MetaOapg.properties.setup_schema: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["signature"]) -> MetaOapg.properties.signature: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["is_preset"]) -> MetaOapg.properties.is_preset: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["preset_name"]) -> MetaOapg.properties.preset_name: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "type", "status", "name", "description", "parameters", "other", "created_by", "source", "source_code", "setup_schema", "signature", "is_preset", "preset_name", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["status"]) -> MetaOapg.properties.status: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["description"]) -> typing.Union[MetaOapg.properties.description, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["parameters"]) -> typing.Union[MetaOapg.properties.parameters, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["other"]) -> typing.Union[MetaOapg.properties.other, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["created_by"]) -> typing.Union['UserResponse', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["source"]) -> typing.Union['ToolSource', schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["source_code"]) -> typing.Union[MetaOapg.properties.source_code, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["setup_schema"]) -> typing.Union[MetaOapg.properties.setup_schema, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["signature"]) -> typing.Union[MetaOapg.properties.signature, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["is_preset"]) -> typing.Union[MetaOapg.properties.is_preset, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["preset_name"]) -> typing.Union[MetaOapg.properties.preset_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "type", "status", "name", "description", "parameters", "other", "created_by", "source", "source_code", "setup_schema", "signature", "is_preset", "preset_name", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        id: typing.Union[MetaOapg.properties.id, str, ],
        type: typing.Union[MetaOapg.properties.type, str, ],
        status: typing.Union[MetaOapg.properties.status, str, ],
        description: typing.Union[MetaOapg.properties.description, str, schemas.Unset] = schemas.unset,
        parameters: typing.Union[MetaOapg.properties.parameters, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        other: typing.Union[MetaOapg.properties.other, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        created_by: typing.Union['UserResponse', schemas.Unset] = schemas.unset,
        source: typing.Union['ToolSource', schemas.Unset] = schemas.unset,
        source_code: typing.Union[MetaOapg.properties.source_code, str, schemas.Unset] = schemas.unset,
        setup_schema: typing.Union[MetaOapg.properties.setup_schema, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        signature: typing.Union[MetaOapg.properties.signature, str, schemas.Unset] = schemas.unset,
        is_preset: typing.Union[MetaOapg.properties.is_preset, bool, schemas.Unset] = schemas.unset,
        preset_name: typing.Union[MetaOapg.properties.preset_name, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'ToolConfigResponse':
        return super().__new__(
            cls,
            *args,
            name=name,
            id=id,
            type=type,
            status=status,
            description=description,
            parameters=parameters,
            other=other,
            created_by=created_by,
            source=source,
            source_code=source_code,
            setup_schema=setup_schema,
            signature=signature,
            is_preset=is_preset,
            preset_name=preset_name,
            _configuration=_configuration,
            **kwargs,
        )

from humanloop.model.tool_source import ToolSource
from humanloop.model.user_response import UserResponse
