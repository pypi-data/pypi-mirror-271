# TODO: This class is mostly held together via bad TDD. It was copied over from
# the classnotation loader and ported whenever a test failed. As a result none
# of the overarching logic is thought out. While this file does not need to be
# rebuilt from the ground up, the tests obviously pass, each branch should be
# revisited with an eye to "what is this actually doing" at some point in
# the future.
# TODO: The errors are almost certainly wrong and will confuse regular users
from types import NoneType
from typing import Any, TypeVar, get_origin, get_args, Union, Optional, Literal, Tuple
from .json_types import JSONData, JSONObject
from dataclasses import fields, is_dataclass
import enum
import json


T = TypeVar('T')


class DataclassDumper():

    def dumps(
        self,
        data: T,
        # allow_whole_float_as_int: bool = True,
        # strict: bool = False
    ) -> str:
        # self.allow_whole_float_as_int = allow_whole_float_as_int
        # self.strict = strict
        return json.dumps(self._dump_data(data, _stack=()))


    def _dump_data(
        self,
        data: T,
        _stack: Tuple[str, ...],
    ) -> JSONData:

        return_data: JSONObject = {}

        if not is_dataclass(data):
            raise TypeError("Expected a dataclass")

        for field in fields(data):
            return_data[field.name] = self.dump_field(getattr(data, field.name), field.type, _stack=(*_stack, field.name))

        return return_data

        # if not is_dataclass(data_class):
        #     raise TypeError("Expected a dataclass type as `data_class`")

        # field_type_lookup = {field.name: resolve_field_type(field.type, data_class) for field in fields(data_class)}
        # field_renaming = {field.metadata["json"]: field.name for field in fields(data_class) if "json" in field.metadata}
        # validated_data = {}

        # for json_key, value in data.items():

        #     if not isinstance(json_key, str):
        #         raise TypeError("Expected only string keys when loading dict into dataclass but found `{}` of type {} at {}".format(json_key, type(json_key), ".".join(_stack)))

        #     field_name = json_key
        #     if json_key in field_renaming:
        #         field_name = field_renaming[json_key]

        #     if field_name in field_type_lookup:
        #         field_type = field_type_lookup[field_name]

        #         validated_data[field_name] = self.validate_field(value, field_type, _stack=(*_stack, json_key))

        #     else:
        #         error_message = "Warning: Field '{json_key}' found in json at {stack} but it not present in the dataclass {dataclass}.".format(
        #             json_key=json_key,
        #             stack=".".join(_stack),
        #             dataclass=data_class,
        #         )
        #         if not self.strict:
        #             logging.warning(error_message)
        #         else:
        #             raise ValueError(error_message)

        # try:
        #     return data_class(**validated_data)
        # except TypeError as e:
        #     print("Error found at", ".".join(_stack)) # TODO: this should be incorporated into the message somehow
        #     raise e


    def dump_field(
        self,
        value: Any,
        field_type: type,
        _stack: Tuple[str, ...],
    ) -> JSONData:

        field_origin = get_origin(field_type)

        # List[]
        if field_origin == list:
            if isinstance(value, list):
                retval = [
                    self.dump_field(
                        element,
                        get_args(field_type)[0],
                        _stack=(*_stack, "[{}]".format(i))
                    ) for i, element in enumerate(value)
                ]
                return retval

        # Dict[]
        elif field_origin == dict:
            if isinstance(value, dict):
                retval = {
                    str(k):
                    self.dump_field(v, get_args(field_type)[1], _stack=(*_stack, "[{}]".format(k.__repr__())))
                    for k, v in value.items()
                }
                return retval

        # Set[]
        elif field_origin == set:
            if isinstance(value, list) or isinstance(value, set) or isinstance(value, tuple):
                retval = [
                    self.dump_field(element, get_args(field_type)[0], _stack=(*_stack, "[{}]".format(i)))
                    for i, element in enumerate(value)
                ]
                return sorted(retval, key=lambda x: repr(x)) # TODO: We should have a flag on "Should sort set"

        # Tuple[]
        elif (field_origin == tuple):
            if isinstance(value, tuple):
                args = get_args(field_type)

                # Variable Length Tuples
                if len(args) == 2 and args[1] == Ellipsis:
                    retval = [
                        self.dump_field(element, get_args(field_type)[0], _stack=(*_stack, "[{}]".format(i)))
                        for i, element in enumerate(value)
                    ]
                    return retval

                # Fixed Length Tuples
                else:
                    if len(args) != len(value):
                        raise TypeError("Different Number of elements found for tuple then expected found {} ({}), expected {}".format(len(value), value, len(args)))

                    retval = [
                        self.dump_field(value[i], args[i], _stack=(*_stack, "[{}]".format(i)))
                        for i in range(len(value))
                    ]
                    return retval

        # Union[] and Optional[]
        elif field_origin == Union:
            last_error: Optional[TypeError] = None
            for arg in get_args(field_type):
                last_error = None
                try:
                    return self.dump_field(value, arg, _stack=_stack)
                except TypeError as e:
                    last_error = e

            if last_error is not None:
                raise last_error

        # Literal[]
        elif field_origin == Literal:
            arg_value = get_args(field_type)[0]
            if type(value) is bytes and type(arg_value) is bytes:
                return value.decode("utf-8")

            if value != arg_value:
                raise TypeError("Expected a literal '{}' but got '{}".format(get_args(field_type)[0], value))

            return value


        elif field_origin is None:
            # Special case of None Type
            if (field_type is None or field_type == NoneType) and value is None:
                return value

            elif field_type is str and type(value) is str:
                return value

            elif field_type is bytes and type(value) is bytes:
                return value.decode("utf-8")

            elif field_type is int and type(value) is int:
                return value

            elif field_type is float and type(value) is float:
                return value

            elif field_type is bool and type(value) is bool:
                return value

            elif is_dataclass(field_type) and is_dataclass(value):
                return self._dump_data(value, _stack=_stack) # Stack might be wrong here

            elif issubclass(field_type, enum.Enum) and issubclass(type(value), enum.Enum):
                # Return the value of the enum
                return value.value

            # If we get here, nothing above parsed properly
            raise TypeError("Unhandled scalar type `{found_type}` at `{stack}`. Expected `{target_type}`.".format(
                found_type=type(value),
                stack=".".join(_stack),
                target_type=field_type)
            )

        else:
            raise TypeError(
                "Error: Field '{data_key} in dataclass has an unexpected origin type of {data_origin}. This might be a bug in dataclass loader, please report it.".format(
                    data_key=".".join(_stack),
                    data_origin=field_origin
                )
            )

        raise TypeError(
            "Error: Field '{data_key}' is {data_type} but dataclass expected {dataclass_type}".format(
                data_key=".".join(_stack),
                data_type=type(value),
                dataclass_type=field_type,
            )
        )


def dump_data(data: T) -> JSONData:
    pass

def dumps(data: T) -> str:
    loader = DataclassDumper()
    return loader.dumps(data)
