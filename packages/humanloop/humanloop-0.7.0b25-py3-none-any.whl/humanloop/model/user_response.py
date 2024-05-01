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


class UserResponse(
    schemas.DictSchema
):
    """
    This class is auto generated by Konfig (https://konfigthis.com)
    """


    class MetaOapg:
        required = {
            "email_address",
            "verified",
            "id",
        }
        
        class properties:
            id = schemas.StrSchema
            email_address = schemas.StrSchema
            verified = schemas.BoolSchema
            full_name = schemas.StrSchema
            __annotations__ = {
                "id": id,
                "email_address": email_address,
                "verified": verified,
                "full_name": full_name,
            }
    
    email_address: MetaOapg.properties.email_address
    verified: MetaOapg.properties.verified
    id: MetaOapg.properties.id
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["email_address"]) -> MetaOapg.properties.email_address: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["verified"]) -> MetaOapg.properties.verified: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["full_name"]) -> MetaOapg.properties.full_name: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "email_address", "verified", "full_name", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["email_address"]) -> MetaOapg.properties.email_address: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["verified"]) -> MetaOapg.properties.verified: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["full_name"]) -> typing.Union[MetaOapg.properties.full_name, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "email_address", "verified", "full_name", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *args: typing.Union[dict, frozendict.frozendict, ],
        email_address: typing.Union[MetaOapg.properties.email_address, str, ],
        verified: typing.Union[MetaOapg.properties.verified, bool, ],
        id: typing.Union[MetaOapg.properties.id, str, ],
        full_name: typing.Union[MetaOapg.properties.full_name, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'UserResponse':
        return super().__new__(
            cls,
            *args,
            email_address=email_address,
            verified=verified,
            id=id,
            full_name=full_name,
            _configuration=_configuration,
            **kwargs,
        )
