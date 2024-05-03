from typing import Dict, List, Union

JSONString = str
JSONNumber = float
JSONNull = type(None)
JSONArray = List["JSONData"]
JSONObject = Dict[str, "JSONData"]

JSONData = Union[JSONString, JSONNumber, JSONNull, JSONArray, JSONObject]
