import jpype
import jpype.imports

from java.util import List as List_  # type: ignore
from java.util import EnumSet as EnumSet_  # type: ignore
from com.github.romualdrousseau.shuju.json import JSON as JSON_  # type: ignore


@jpype._jcustomizer.JConversion("java.util.List", instanceof=list)
def _JListConvert(jcls, obj):
    return List_.of(obj)


@jpype._jcustomizer.JConversion(
    "com.github.romualdrousseau.shuju.json.JSONObject", instanceof=str
)
def _JJSONObjectConvert(jcls, obj):
    return JSON_.objectOf(obj)


@jpype._jcustomizer.JConversion("java.util.EnumSet", instanceof=list)
def _JEnumSetConvert(jcls, obj):
    return EnumSet_.of(*obj)
