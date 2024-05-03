from typing import Dict, Any, Type, TypeVar, List, get_origin, get_args, Union, Optional, Literal, Tuple
from dataclasses import fields, is_dataclass
import logging
import enum
import importlib
import json
from .json_types import JSONData, JSONObject

T = TypeVar('T')


class DataclassLoader:
    allow_whole_float_as_int: bool
    strict: bool

    ############################################################################
    # loads
    #
    # Helper function wrapper to load a JSON string directly into a dataclass.
    ############################################################################
    def loads(
        self,
        data_class: Type[T],
        data: str,
        allow_whole_float_as_int: bool = True,
        strict: bool = True,
    ) -> T:
        return self.load_data(
            data_class=data_class,
            data=json.loads(data),
            allow_whole_float_as_int=allow_whole_float_as_int,
            strict=strict,
        )

    ############################################################################
    # load
    #
    # Load pre-parsed json data into a dataclass
    ############################################################################
    def load_data(
        self,
        data_class: Type[T],
        data: JSONObject,
        allow_whole_float_as_int: bool = True,
        strict: bool = True
    ) -> T:
        self.allow_whole_float_as_int = allow_whole_float_as_int
        self.strict = strict
        return self._load_data(data_class, data, _stack=())

    ############################################################################
    # _load_data
    #
    # An internal function call to load arbitrary data objects
    ############################################################################
    def _load_data(
        self,
        data_class: Type[T],
        data: JSONObject,
        _stack: Tuple[str, ...],

    ) -> T:
        if not is_dataclass(data_class):
            raise TypeError("Expected a dataclass type as `data_class`")

        field_type_lookup = {field.name: resolve_field_type(field.type, data_class) for field in fields(data_class)}
        field_renaming = {field.metadata["json"]: field.name for field in fields(data_class) if "json" in field.metadata}
        validated_data = {}

        for json_key, value in data.items():

            if not isinstance(json_key, str):
                raise TypeError("Expected only string keys when loading dict into dataclass but found `{}` of type {} at {}".format(json_key, type(json_key), ".".join(_stack)))

            field_name = json_key
            if json_key in field_renaming:
                field_name = field_renaming[json_key]

            if field_name in field_type_lookup:
                field_type = field_type_lookup[field_name]

                validated_data[field_name] = self.validate_field(value, field_type, _stack=(*_stack, json_key))

            else:
                error_message = "Warning: Field '{json_key}' found in json at {stack} but it not present in the dataclass {dataclass}.".format(
                    json_key=json_key,
                    stack=".".join(_stack),
                    dataclass=data_class,
                )
                if not self.strict:
                    logging.warning(error_message)
                else:
                    raise ValueError(error_message)

        try:
            return data_class(**validated_data)
        except TypeError as e:
            print("Error found at", ".".join(_stack)) # TODO: this should be incorporated into the message somehow
            raise e

    ################################################################################
    #
    ################################################################################
    def validate_field(
        self,
        value: Any,
        field_type: Type[T],
        _stack: Tuple[str, ...],
    ) -> T:
        field_origin = get_origin(field_type)

        # List[]
        if field_origin == list:
            if isinstance(value, list):
                retval = [
                    self.validate_field(
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
                    self.validate_field(k, get_args(field_type)[0], _stack=(*_stack, str(k))):
                    self.validate_field(v, get_args(field_type)[1], _stack=(*_stack, "[{}]".format(k.__repr__())))
                    for k, v in value.items()
                }
                return retval

        # Set[]
        elif field_origin == set:
            if isinstance(value, list) or isinstance(value, set) or isinstance(value, tuple):
                retval = set([
                    self.validate_field(element, get_args(field_type)[0], _stack=(*_stack, "[{}]".format(i)))
                    for i, element in enumerate(value)
                ])
                return retval

        # Tuple[]
        elif (get_origin(field_type) == tuple):
            if isinstance(value, list) or isinstance(value, tuple):

                args = get_args(field_type)
                # Variable Length Tuples
                if len(args) == 2 and args[1] == Ellipsis:
                    retval = tuple(
                        self.validate_field(element, get_args(field_type)[0], _stack=(*_stack, "[{}]".format(i)))
                        for i, element in enumerate(value)
                    )
                    return retval

                # Fixed Length Tuples
                else:
                    if len(args) != len(value):
                        raise TypeError("Different Number of elements found for tuple then expected found {} ({}), expected {}".format(len(value), value, len(args)))

                    retval = tuple(
                        self.validate_field(value[i], args[i], _stack=(*_stack, "[{}]".format(i)))
                        for i in range(len(value))
                    )
                    return retval

        # Union[] and Optional[]
        elif field_origin == Union:
            all_errors: List[TypeError] = []
            for arg in get_args(field_type):
                try:
                    return self.validate_field(value, arg, _stack=_stack)
                except TypeError as e:
                    all_errors.append(e)

            if len(all_errors) > 0:
                # Build an error message that contains the errors from parsing each of the possible types in the union
                combined_message = "Expected one of union type `{}` at `{}`\n".format(field_type, ".".join(_stack))
                for i, error in enumerate(all_errors):
                    prefix: str = "  {}: ".format(i)
                    for line in error.args[0].split("\n"):
                        combined_message += prefix + line + "\n"
                        prefix = " " * len(prefix)

                raise TypeError(combined_message)

        # Literal[]
        elif field_origin == Literal:
            arg_value = get_args(field_type)[0]
            if type(value) is str and type(arg_value) is bytes:
                value = value.encode("utf-8")

            if value != arg_value:
                raise TypeError("Expected a literal '{}' but got '{}".format(get_args(field_type)[0], value))
            return value

        elif field_origin is None:
            # Special case of None Type
            if field_type is None and value is None:
                return value

            # Special case to call out that bool is historically an instance of int
            # and we want to be sure a bool is not trying to be assigned to an int.
            # TODO: we might want to make a custom isinstance function instead.
            elif type(value) is bool and field_type in (int, float):
                pass

            # General case of scalar types
            elif isinstance(value, field_type):
                return value

            # Enums
            elif issubclass(field_type, enum.Enum):
                for element in field_type:
                    if element.value == value:
                        return field_type(value)
                raise TypeError("Invalid Enum value for {}: {}".format(field_type, value))

            # Sub Dataclass
            elif isinstance(value, dict) and is_dataclass(field_type):
                retval = self._load_data(field_type, value, _stack=_stack)
                return retval

            # Special handling for floats as integers (as JSON numbers are parsed as floats)
            elif self.allow_whole_float_as_int and field_type is int and isinstance(value, float) and value.is_integer():
                return int(value)

            # Special handling for ints as floats, which can have integers implicitly assinged to them in general
            elif field_type is float and isinstance(value, int):
                return float(value)

            # Special handling for strings as bytes
            elif field_type is bytes and isinstance(value, str):
                return value.encode("utf-8")

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


################################################################################
# resolve_field_type
#
# This function takes a type annotation and resolves it into an actual type if
# it is defined as a string. This is necessary because many functions will be
# expecting a real type value and not a string representation of the type. One
# function is the commonly used `isinstance()`.
################################################################################
def resolve_field_type(
    field_type: Any,
    defined_in_object: Optional[Any] = None
) -> Type:
    # Handle stringy types
    if isinstance(field_type, str):
        if defined_in_object is None:
            raise TypeError("Stringy Type found but no object path can be used to decode the type")

        module_name = defined_in_object.__module__
        module = importlib.import_module(module_name)

        # Iterate through the full type grabbing the next subtype in the list
        found_type: Any = module
        for element in field_type.split("."):
            found_type = getattr(found_type, element)

        # Sanity Check
        if not isinstance(found_type, type):
            raise TypeError("Cannot find the specified type {}".format(field_type))

        return found_type

    # Handle most types
    elif isinstance(field_type, type):
        return field_type

    # Special case for the "None" type
    elif field_type is None:
        return field_type

    # Handle typing generic types, for example List[int]
    elif get_origin(field_type) is not None:
        return field_type

    else:
        raise TypeError("Invalid type found on field {} (of type {})".format(field_type, type(field_type)))



################################################################################
# load_data
#
# Top level helper function to load a json string into a dataclass without
# worrying about creating or managing the DataclassLoader object.
################################################################################
def loads(
    data_class: Type[T],
    data: str,
    allow_whole_float_as_int: bool = True,
    strict: bool = True
) -> T:
    loader = DataclassLoader()
    return loader.loads(data_class, data, allow_whole_float_as_int=allow_whole_float_as_int, strict=strict)


################################################################################
# load_data
#
# Top level helper function to load data into a dataclass without worrying
# about creating or managing the DataclassLoader object.
################################################################################
def load_data(
    data_class: Type[T],
    data: JSONObject,
    allow_whole_float_as_int: bool = True,
    strict: bool = True
) -> T:
    loader = DataclassLoader()
    return loader.load_data(data_class, data, allow_whole_float_as_int=allow_whole_float_as_int, strict=strict)
