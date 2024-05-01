# coding: utf-8

"""
    E2B API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Any, ClassVar, Dict, List, Optional
from pydantic import BaseModel, StrictInt, StrictStr
from pydantic import Field

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class RunningSandboxes(BaseModel):
    """
    RunningSandboxes
    """  # noqa: E501

    template_id: StrictStr = Field(
        description="Identifier of the template from which is the sandbox created",
        alias="templateID",
    )
    alias: Optional[StrictStr] = Field(
        default=None, description="Alias of the template"
    )
    sandbox_id: StrictStr = Field(
        description="Identifier of the sandbox", alias="sandboxID"
    )
    client_id: StrictStr = Field(
        description="Identifier of the client", alias="clientID"
    )
    started_at: datetime = Field(
        description="Time when the sandbox was started", alias="startedAt"
    )
    cpu_count: StrictInt = Field(
        description="CPU cores for the sandbox", alias="cpuCount"
    )
    memory_mb: StrictInt = Field(
        description="Memory limit for the sandbox in MB", alias="memoryMB"
    )
    metadata: Optional[Dict[str, StrictStr]] = None
    additional_properties: Dict[str, Any] = {}
    __properties: ClassVar[List[str]] = [
        "templateID",
        "alias",
        "sandboxID",
        "clientID",
        "startedAt",
        "cpuCount",
        "memoryMB",
        "metadata",
    ]

    model_config = {"populate_by_name": True, "validate_assignment": True}

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of RunningSandboxes from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * Fields in `self.additional_properties` are added to the output dict.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={
                "additional_properties",
            },
            exclude_none=True,
        )
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of RunningSandboxes from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "templateID": obj.get("templateID"),
                "alias": obj.get("alias"),
                "sandboxID": obj.get("sandboxID"),
                "clientID": obj.get("clientID"),
                "startedAt": obj.get("startedAt"),
                "cpuCount": obj.get("cpuCount"),
                "memoryMB": obj.get("memoryMB"),
                "metadata": obj.get("metadata"),
            }
        )
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
