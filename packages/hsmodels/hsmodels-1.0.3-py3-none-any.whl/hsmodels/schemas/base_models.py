from datetime import datetime
from typing import Any, Literal, Union

import typing_extensions
from pydantic import BaseModel, ConfigDict


class BaseMetadata(BaseModel):
    def model_dump(
        self,
        *,
        mode: Union[typing_extensions.Literal['json', 'python'], str] = 'python',
        include: 'IncEx' = None,
        exclude: 'IncEx' = None,
        context: Union[dict[str, Any], None] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        round_trip: bool = False,
        warnings: Union[bool, Literal['none', 'warn', 'error']] = False,
        serialize_as_any: bool = False,
        to_rdf: bool = False,
    ) -> dict[str, Any]:
        """
        Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

        Checks the config for a schema_config dictionary_field and converts a dictionary to a list of key/value pairs.
        This converts the dictionary to a format that can be described in a json schema (which can be found below in the
        schema_extra staticmethod.

        Override the default of exclude_none to True
        """
        d = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )
        if to_rdf and "additional_metadata" in d:
            additional_metadata = d["additional_metadata"]
            d["additional_metadata"] = [{"key": key, "value": value} for key, value in additional_metadata.items()]

        return d

    def model_dump_json(
        self,
        *,
        indent: Union[int, None] = None,
        include: 'IncEx' = None,
        exclude: 'IncEx' = None,
        context: Union[dict[str, Any], None] = None,
        by_alias: bool = False,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = True,
        round_trip: bool = False,
        warnings: Union[bool, Literal['none', 'warn', 'error']] = False,
        serialize_as_any: bool = False,
    ) -> str:
        """
        Generate a JSON representation of the model, `include` and `exclude` arguments as per `dict()`.

        `encoder` is an optional function to supply as `default` to json.dumps(), other arguments as per `json.dumps()`.

        Override the default of exclude_none to True
        """
        return super().model_dump_json(
            indent=indent,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            round_trip=round_trip,
            warnings=warnings,
            serialize_as_any=serialize_as_any,
        )

    model_config = ConfigDict(validate_assignment=True)


class BaseCoverage(BaseMetadata):
    def __str__(self):
        return "; ".join(
            [
                "=".join([key, val.isoformat() if isinstance(val, datetime) else str(val)])
                for key, val in self.__dict__.items()
                if key != "type" and val
            ]
        )
