#
# Copyright (c) 2024 Snowflake Computing Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# coding: utf-8

"""
    Apache Iceberg REST Catalog API

    Defines the specification for the first version of the REST Catalog API. Implementations should ideally support both Iceberg table specs v1 and v2, with priority given to v2.

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from polaris.catalog.models.model_schema import ModelSchema
from polaris.catalog.models.view_history_entry import ViewHistoryEntry
from polaris.catalog.models.view_version import ViewVersion
from typing import Optional, Set
from typing_extensions import Self

class ViewMetadata(BaseModel):
    """
    ViewMetadata
    """ # noqa: E501
    view_uuid: StrictStr = Field(alias="view-uuid")
    format_version: Annotated[int, Field(le=1, strict=True, ge=1)] = Field(alias="format-version")
    location: StrictStr
    current_version_id: StrictInt = Field(alias="current-version-id")
    versions: List[ViewVersion]
    version_log: List[ViewHistoryEntry] = Field(alias="version-log")
    schemas: List[ModelSchema]
    properties: Optional[Dict[str, StrictStr]] = None
    __properties: ClassVar[List[str]] = ["view-uuid", "format-version", "location", "current-version-id", "versions", "version-log", "schemas", "properties"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of ViewMetadata from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in versions (list)
        _items = []
        if self.versions:
            for _item in self.versions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['versions'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in version_log (list)
        _items = []
        if self.version_log:
            for _item in self.version_log:
                if _item:
                    _items.append(_item.to_dict())
            _dict['version-log'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in schemas (list)
        _items = []
        if self.schemas:
            for _item in self.schemas:
                if _item:
                    _items.append(_item.to_dict())
            _dict['schemas'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ViewMetadata from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "view-uuid": obj.get("view-uuid"),
            "format-version": obj.get("format-version"),
            "location": obj.get("location"),
            "current-version-id": obj.get("current-version-id"),
            "versions": [ViewVersion.from_dict(_item) for _item in obj["versions"]] if obj.get("versions") is not None else None,
            "version-log": [ViewHistoryEntry.from_dict(_item) for _item in obj["version-log"]] if obj.get("version-log") is not None else None,
            "schemas": [ModelSchema.from_dict(_item) for _item in obj["schemas"]] if obj.get("schemas") is not None else None,
            "properties": obj.get("properties")
        })
        return _obj


