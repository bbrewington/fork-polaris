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
from inspect import getfullargspec
import json
import pprint
import re  # noqa: F401
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Optional
from polaris.catalog.models.add_partition_spec_update import AddPartitionSpecUpdate
from polaris.catalog.models.add_schema_update import AddSchemaUpdate
from polaris.catalog.models.add_snapshot_update import AddSnapshotUpdate
from polaris.catalog.models.add_sort_order_update import AddSortOrderUpdate
from polaris.catalog.models.assign_uuid_update import AssignUUIDUpdate
from polaris.catalog.models.remove_properties_update import RemovePropertiesUpdate
from polaris.catalog.models.remove_snapshot_ref_update import RemoveSnapshotRefUpdate
from polaris.catalog.models.remove_snapshots_update import RemoveSnapshotsUpdate
from polaris.catalog.models.remove_statistics_update import RemoveStatisticsUpdate
from polaris.catalog.models.set_current_schema_update import SetCurrentSchemaUpdate
from polaris.catalog.models.set_default_sort_order_update import SetDefaultSortOrderUpdate
from polaris.catalog.models.set_default_spec_update import SetDefaultSpecUpdate
from polaris.catalog.models.set_location_update import SetLocationUpdate
from polaris.catalog.models.set_properties_update import SetPropertiesUpdate
from polaris.catalog.models.set_snapshot_ref_update import SetSnapshotRefUpdate
from polaris.catalog.models.set_statistics_update import SetStatisticsUpdate
from polaris.catalog.models.upgrade_format_version_update import UpgradeFormatVersionUpdate
from typing import Union, Any, List, Set, TYPE_CHECKING, Optional, Dict
from typing_extensions import Literal, Self
from pydantic import Field

TABLEUPDATE_ANY_OF_SCHEMAS = ["AddPartitionSpecUpdate", "AddSchemaUpdate", "AddSnapshotUpdate", "AddSortOrderUpdate", "AssignUUIDUpdate", "RemovePropertiesUpdate", "RemoveSnapshotRefUpdate", "RemoveSnapshotsUpdate", "RemoveStatisticsUpdate", "SetCurrentSchemaUpdate", "SetDefaultSortOrderUpdate", "SetDefaultSpecUpdate", "SetLocationUpdate", "SetPropertiesUpdate", "SetSnapshotRefUpdate", "SetStatisticsUpdate", "UpgradeFormatVersionUpdate"]

class TableUpdate(BaseModel):
    """
    TableUpdate
    """

    # data type: AssignUUIDUpdate
    anyof_schema_1_validator: Optional[AssignUUIDUpdate] = None
    # data type: UpgradeFormatVersionUpdate
    anyof_schema_2_validator: Optional[UpgradeFormatVersionUpdate] = None
    # data type: AddSchemaUpdate
    anyof_schema_3_validator: Optional[AddSchemaUpdate] = None
    # data type: SetCurrentSchemaUpdate
    anyof_schema_4_validator: Optional[SetCurrentSchemaUpdate] = None
    # data type: AddPartitionSpecUpdate
    anyof_schema_5_validator: Optional[AddPartitionSpecUpdate] = None
    # data type: SetDefaultSpecUpdate
    anyof_schema_6_validator: Optional[SetDefaultSpecUpdate] = None
    # data type: AddSortOrderUpdate
    anyof_schema_7_validator: Optional[AddSortOrderUpdate] = None
    # data type: SetDefaultSortOrderUpdate
    anyof_schema_8_validator: Optional[SetDefaultSortOrderUpdate] = None
    # data type: AddSnapshotUpdate
    anyof_schema_9_validator: Optional[AddSnapshotUpdate] = None
    # data type: SetSnapshotRefUpdate
    anyof_schema_10_validator: Optional[SetSnapshotRefUpdate] = None
    # data type: RemoveSnapshotsUpdate
    anyof_schema_11_validator: Optional[RemoveSnapshotsUpdate] = None
    # data type: RemoveSnapshotRefUpdate
    anyof_schema_12_validator: Optional[RemoveSnapshotRefUpdate] = None
    # data type: SetLocationUpdate
    anyof_schema_13_validator: Optional[SetLocationUpdate] = None
    # data type: SetPropertiesUpdate
    anyof_schema_14_validator: Optional[SetPropertiesUpdate] = None
    # data type: RemovePropertiesUpdate
    anyof_schema_15_validator: Optional[RemovePropertiesUpdate] = None
    # data type: SetStatisticsUpdate
    anyof_schema_16_validator: Optional[SetStatisticsUpdate] = None
    # data type: RemoveStatisticsUpdate
    anyof_schema_17_validator: Optional[RemoveStatisticsUpdate] = None
    if TYPE_CHECKING:
        actual_instance: Optional[Union[AddPartitionSpecUpdate, AddSchemaUpdate, AddSnapshotUpdate, AddSortOrderUpdate, AssignUUIDUpdate, RemovePropertiesUpdate, RemoveSnapshotRefUpdate, RemoveSnapshotsUpdate, RemoveStatisticsUpdate, SetCurrentSchemaUpdate, SetDefaultSortOrderUpdate, SetDefaultSpecUpdate, SetLocationUpdate, SetPropertiesUpdate, SetSnapshotRefUpdate, SetStatisticsUpdate, UpgradeFormatVersionUpdate]] = None
    else:
        actual_instance: Any = None
    any_of_schemas: Set[str] = { "AddPartitionSpecUpdate", "AddSchemaUpdate", "AddSnapshotUpdate", "AddSortOrderUpdate", "AssignUUIDUpdate", "RemovePropertiesUpdate", "RemoveSnapshotRefUpdate", "RemoveSnapshotsUpdate", "RemoveStatisticsUpdate", "SetCurrentSchemaUpdate", "SetDefaultSortOrderUpdate", "SetDefaultSpecUpdate", "SetLocationUpdate", "SetPropertiesUpdate", "SetSnapshotRefUpdate", "SetStatisticsUpdate", "UpgradeFormatVersionUpdate" }

    model_config = {
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    discriminator_value_class_map: Dict[str, str] = {
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_anyof(cls, v):
        instance = TableUpdate.model_construct()
        error_messages = []
        # validate data type: AssignUUIDUpdate
        if not isinstance(v, AssignUUIDUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AssignUUIDUpdate`")
        else:
            return v

        # validate data type: UpgradeFormatVersionUpdate
        if not isinstance(v, UpgradeFormatVersionUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `UpgradeFormatVersionUpdate`")
        else:
            return v

        # validate data type: AddSchemaUpdate
        if not isinstance(v, AddSchemaUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AddSchemaUpdate`")
        else:
            return v

        # validate data type: SetCurrentSchemaUpdate
        if not isinstance(v, SetCurrentSchemaUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SetCurrentSchemaUpdate`")
        else:
            return v

        # validate data type: AddPartitionSpecUpdate
        if not isinstance(v, AddPartitionSpecUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AddPartitionSpecUpdate`")
        else:
            return v

        # validate data type: SetDefaultSpecUpdate
        if not isinstance(v, SetDefaultSpecUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SetDefaultSpecUpdate`")
        else:
            return v

        # validate data type: AddSortOrderUpdate
        if not isinstance(v, AddSortOrderUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AddSortOrderUpdate`")
        else:
            return v

        # validate data type: SetDefaultSortOrderUpdate
        if not isinstance(v, SetDefaultSortOrderUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SetDefaultSortOrderUpdate`")
        else:
            return v

        # validate data type: AddSnapshotUpdate
        if not isinstance(v, AddSnapshotUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AddSnapshotUpdate`")
        else:
            return v

        # validate data type: SetSnapshotRefUpdate
        if not isinstance(v, SetSnapshotRefUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SetSnapshotRefUpdate`")
        else:
            return v

        # validate data type: RemoveSnapshotsUpdate
        if not isinstance(v, RemoveSnapshotsUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `RemoveSnapshotsUpdate`")
        else:
            return v

        # validate data type: RemoveSnapshotRefUpdate
        if not isinstance(v, RemoveSnapshotRefUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `RemoveSnapshotRefUpdate`")
        else:
            return v

        # validate data type: SetLocationUpdate
        if not isinstance(v, SetLocationUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SetLocationUpdate`")
        else:
            return v

        # validate data type: SetPropertiesUpdate
        if not isinstance(v, SetPropertiesUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SetPropertiesUpdate`")
        else:
            return v

        # validate data type: RemovePropertiesUpdate
        if not isinstance(v, RemovePropertiesUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `RemovePropertiesUpdate`")
        else:
            return v

        # validate data type: SetStatisticsUpdate
        if not isinstance(v, SetStatisticsUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SetStatisticsUpdate`")
        else:
            return v

        # validate data type: RemoveStatisticsUpdate
        if not isinstance(v, RemoveStatisticsUpdate):
            error_messages.append(f"Error! Input type `{type(v)}` is not `RemoveStatisticsUpdate`")
        else:
            return v

        if error_messages:
            # no match
            raise ValueError("No match found when setting the actual_instance in TableUpdate with anyOf schemas: AddPartitionSpecUpdate, AddSchemaUpdate, AddSnapshotUpdate, AddSortOrderUpdate, AssignUUIDUpdate, RemovePropertiesUpdate, RemoveSnapshotRefUpdate, RemoveSnapshotsUpdate, RemoveStatisticsUpdate, SetCurrentSchemaUpdate, SetDefaultSortOrderUpdate, SetDefaultSpecUpdate, SetLocationUpdate, SetPropertiesUpdate, SetSnapshotRefUpdate, SetStatisticsUpdate, UpgradeFormatVersionUpdate. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        # anyof_schema_1_validator: Optional[AssignUUIDUpdate] = None
        try:
            instance.actual_instance = AssignUUIDUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_2_validator: Optional[UpgradeFormatVersionUpdate] = None
        try:
            instance.actual_instance = UpgradeFormatVersionUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_3_validator: Optional[AddSchemaUpdate] = None
        try:
            instance.actual_instance = AddSchemaUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_4_validator: Optional[SetCurrentSchemaUpdate] = None
        try:
            instance.actual_instance = SetCurrentSchemaUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_5_validator: Optional[AddPartitionSpecUpdate] = None
        try:
            instance.actual_instance = AddPartitionSpecUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_6_validator: Optional[SetDefaultSpecUpdate] = None
        try:
            instance.actual_instance = SetDefaultSpecUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_7_validator: Optional[AddSortOrderUpdate] = None
        try:
            instance.actual_instance = AddSortOrderUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_8_validator: Optional[SetDefaultSortOrderUpdate] = None
        try:
            instance.actual_instance = SetDefaultSortOrderUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_9_validator: Optional[AddSnapshotUpdate] = None
        try:
            instance.actual_instance = AddSnapshotUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_10_validator: Optional[SetSnapshotRefUpdate] = None
        try:
            instance.actual_instance = SetSnapshotRefUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_11_validator: Optional[RemoveSnapshotsUpdate] = None
        try:
            instance.actual_instance = RemoveSnapshotsUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_12_validator: Optional[RemoveSnapshotRefUpdate] = None
        try:
            instance.actual_instance = RemoveSnapshotRefUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_13_validator: Optional[SetLocationUpdate] = None
        try:
            instance.actual_instance = SetLocationUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_14_validator: Optional[SetPropertiesUpdate] = None
        try:
            instance.actual_instance = SetPropertiesUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_15_validator: Optional[RemovePropertiesUpdate] = None
        try:
            instance.actual_instance = RemovePropertiesUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_16_validator: Optional[SetStatisticsUpdate] = None
        try:
            instance.actual_instance = SetStatisticsUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_17_validator: Optional[RemoveStatisticsUpdate] = None
        try:
            instance.actual_instance = RemoveStatisticsUpdate.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))

        if error_messages:
            # no match
            raise ValueError("No match found when deserializing the JSON string into TableUpdate with anyOf schemas: AddPartitionSpecUpdate, AddSchemaUpdate, AddSnapshotUpdate, AddSortOrderUpdate, AssignUUIDUpdate, RemovePropertiesUpdate, RemoveSnapshotRefUpdate, RemoveSnapshotsUpdate, RemoveStatisticsUpdate, SetCurrentSchemaUpdate, SetDefaultSortOrderUpdate, SetDefaultSpecUpdate, SetLocationUpdate, SetPropertiesUpdate, SetSnapshotRefUpdate, SetStatisticsUpdate, UpgradeFormatVersionUpdate. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], AddPartitionSpecUpdate, AddSchemaUpdate, AddSnapshotUpdate, AddSortOrderUpdate, AssignUUIDUpdate, RemovePropertiesUpdate, RemoveSnapshotRefUpdate, RemoveSnapshotsUpdate, RemoveStatisticsUpdate, SetCurrentSchemaUpdate, SetDefaultSortOrderUpdate, SetDefaultSpecUpdate, SetLocationUpdate, SetPropertiesUpdate, SetSnapshotRefUpdate, SetStatisticsUpdate, UpgradeFormatVersionUpdate]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


