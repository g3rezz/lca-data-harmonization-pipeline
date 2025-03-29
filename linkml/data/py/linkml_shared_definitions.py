# Auto generated from linkml_shared_definitions.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-03-29T14:50:57
# Schema: SharedDefinitions
#
# id: https://example.org/SharedDefinitions
# description:
# license: CC-BY-4.0

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Boolean, Float, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCDSD = CurieNamespace('ILCDsd', 'https://example.org/SharedDefinitions/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCDSD


# Types
class UUIDType(str):
    """ A standard UUID (8-4-4-4-12 hex digits). """
    type_class_uri = LINKML["UUIDType"]
    type_class_curie = "linkml:UUIDType"
    type_name = "UUIDType"
    type_model_uri = ILCDSD.UUIDType


class Year(int):
    """ 4-digit year. """
    type_class_uri = LINKML["Year"]
    type_class_curie = "linkml:Year"
    type_name = "Year"
    type_model_uri = ILCDSD.Year


class UnixTimestamp(int):
    """ Unix timestamp (milliseconds since epoch). """
    type_class_uri = LINKML["UnixTimestamp"]
    type_class_curie = "linkml:UnixTimestamp"
    type_name = "UnixTimestamp"
    type_model_uri = ILCDSD.UnixTimestamp


class ResourceURL(str):
    """ A URL string representing a resource location. """
    type_class_uri = LINKML["ResourceURL"]
    type_class_curie = "linkml:ResourceURL"
    type_name = "ResourceURL"
    type_model_uri = ILCDSD.ResourceURL


# Class references
class GlobalReferenceTypeId(extended_str):
    pass


class AniesBaseId(extended_str):
    pass


class AniesNameValueId(AniesBaseId):
    pass


class AniesNameValueModuleId(AniesBaseId):
    pass


class AniesNameTimestampId(AniesBaseId):
    pass


class AniesNameObjectValueId(AniesBaseId):
    pass


class AniesNameValueObjectValueModuleId(AniesBaseId):
    pass


class AniesNameTypedReferenceId(AniesBaseId):
    pass


class AniesWithScenarioId(AniesBaseId):
    pass


class ScenarioId(extended_str):
    pass


class MultiLangStringId(extended_str):
    pass


@dataclass(repr=False)
class GlobalReferenceType(YAMLRoot):
    """
    Master reference pattern with optional shortDesc, type, refObjectId, version, refObjectUri.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["GlobalReferenceType"]
    class_class_curie: ClassVar[str] = "ILCDsd:GlobalReferenceType"
    class_name: ClassVar[str] = "GlobalReferenceType"
    class_model_uri: ClassVar[URIRef] = ILCDSD.GlobalReferenceType

    id: Union[str, GlobalReferenceTypeId] = None
    shortDescription: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, "MultiLangString"]], List[Union[dict, "MultiLangString"]]]] = empty_dict()
    type: Optional[str] = None
    refObjectId: Optional[str] = None
    version: Optional[str] = None
    refObjectUri: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GlobalReferenceTypeId):
            self.id = GlobalReferenceTypeId(self.id)

        self._normalize_inlined_as_list(slot_name="shortDescription", slot_type=MultiLangString, key_name="id", keyed=True)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.refObjectId is not None and not isinstance(self.refObjectId, str):
            self.refObjectId = str(self.refObjectId)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.refObjectUri is not None and not isinstance(self.refObjectUri, str):
            self.refObjectUri = str(self.refObjectUri)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OtherContent(YAMLRoot):
    """
    A container holding 'anies' a list of anies objects
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["OtherContent"]
    class_class_curie: ClassVar[str] = "ILCDsd:OtherContent"
    class_name: ClassVar[str] = "OtherContent"
    class_model_uri: ClassVar[URIRef] = ILCDSD.OtherContent

    anies: Optional[Union[Dict[Union[str, AniesBaseId], Union[dict, "AniesBase"]], List[Union[dict, "AniesBase"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="anies", slot_type=AniesBase, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesBase(YAMLRoot):
    """
    Master pattern for anies with optional name, value, timestampValue, objectValue, module.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["AniesBase"]
    class_class_curie: ClassVar[str] = "ILCDsd:AniesBase"
    class_name: ClassVar[str] = "AniesBase"
    class_model_uri: ClassVar[URIRef] = ILCDSD.AniesBase

    id: Union[str, AniesBaseId] = None
    name: Optional[str] = None
    value: Optional[str] = None
    timestampValue: Optional[int] = None
    objectValue: Optional[Union[dict, GlobalReferenceType]] = None
    module: Optional[str] = None
    scenario: Optional[str] = None
    margins: Optional[float] = None
    description: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, "MultiLangString"]], List[Union[dict, "MultiLangString"]]]] = empty_dict()
    objectScenario: Optional[Union[Dict[Union[str, ScenarioId], Union[dict, "Scenario"]], List[Union[dict, "Scenario"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AniesBaseId):
            self.id = AniesBaseId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.timestampValue is not None and not isinstance(self.timestampValue, int):
            self.timestampValue = int(self.timestampValue)

        if self.objectValue is not None and not isinstance(self.objectValue, GlobalReferenceType):
            self.objectValue = GlobalReferenceType(**as_dict(self.objectValue))

        if self.module is not None and not isinstance(self.module, str):
            self.module = str(self.module)

        if self.scenario is not None and not isinstance(self.scenario, str):
            self.scenario = str(self.scenario)

        if self.margins is not None and not isinstance(self.margins, float):
            self.margins = float(self.margins)

        self._normalize_inlined_as_list(slot_name="description", slot_type=MultiLangString, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="objectScenario", slot_type=Scenario, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesNameValue(AniesBase):
    """
    Only name + value, ignoring timestampValue, objectValue, module.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["AniesNameValue"]
    class_class_curie: ClassVar[str] = "ILCDsd:AniesNameValue"
    class_name: ClassVar[str] = "AniesNameValue"
    class_model_uri: ClassVar[URIRef] = ILCDSD.AniesNameValue

    id: Union[str, AniesNameValueId] = None
    timestampValue: Optional[int] = None
    objectValue: Optional[Union[dict, GlobalReferenceType]] = None
    module: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AniesNameValueId):
            self.id = AniesNameValueId(self.id)

        if self.timestampValue is not None and not isinstance(self.timestampValue, int):
            self.timestampValue = int(self.timestampValue)

        if self.objectValue is not None and not isinstance(self.objectValue, GlobalReferenceType):
            self.objectValue = GlobalReferenceType(**as_dict(self.objectValue))

        if self.module is not None and not isinstance(self.module, str):
            self.module = str(self.module)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesNameValueModule(AniesBase):
    """
    Requires 'module' but discards timestampValue, objectValue.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["AniesNameValueModule"]
    class_class_curie: ClassVar[str] = "ILCDsd:AniesNameValueModule"
    class_name: ClassVar[str] = "AniesNameValueModule"
    class_model_uri: ClassVar[URIRef] = ILCDSD.AniesNameValueModule

    id: Union[str, AniesNameValueModuleId] = None
    module: str = None
    timestampValue: Optional[int] = None
    objectValue: Optional[Union[dict, GlobalReferenceType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AniesNameValueModuleId):
            self.id = AniesNameValueModuleId(self.id)

        if self._is_empty(self.module):
            self.MissingRequiredField("module")
        if not isinstance(self.module, str):
            self.module = str(self.module)

        if self.timestampValue is not None and not isinstance(self.timestampValue, int):
            self.timestampValue = int(self.timestampValue)

        if self.objectValue is not None and not isinstance(self.objectValue, GlobalReferenceType):
            self.objectValue = GlobalReferenceType(**as_dict(self.objectValue))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesNameTimestamp(AniesBase):
    """
    Includes name and timestampValue. Ignores value, objectValue, and module.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["AniesNameTimestamp"]
    class_class_curie: ClassVar[str] = "ILCDsd:AniesNameTimestamp"
    class_name: ClassVar[str] = "AniesNameTimestamp"
    class_model_uri: ClassVar[URIRef] = ILCDSD.AniesNameTimestamp

    id: Union[str, AniesNameTimestampId] = None
    value: Optional[str] = None
    objectValue: Optional[Union[dict, GlobalReferenceType]] = None
    module: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AniesNameTimestampId):
            self.id = AniesNameTimestampId(self.id)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.objectValue is not None and not isinstance(self.objectValue, GlobalReferenceType):
            self.objectValue = GlobalReferenceType(**as_dict(self.objectValue))

        if self.module is not None and not isinstance(self.module, str):
            self.module = str(self.module)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesNameObjectValue(AniesBase):
    """
    Includes name and objectValue. Ignores value, timestampValue, and module.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["AniesNameObjectValue"]
    class_class_curie: ClassVar[str] = "ILCDsd:AniesNameObjectValue"
    class_name: ClassVar[str] = "AniesNameObjectValue"
    class_model_uri: ClassVar[URIRef] = ILCDSD.AniesNameObjectValue

    id: Union[str, AniesNameObjectValueId] = None
    value: Optional[str] = None
    timestampValue: Optional[int] = None
    module: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AniesNameObjectValueId):
            self.id = AniesNameObjectValueId(self.id)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.timestampValue is not None and not isinstance(self.timestampValue, int):
            self.timestampValue = int(self.timestampValue)

        if self.module is not None and not isinstance(self.module, str):
            self.module = str(self.module)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesNameValueObjectValueModule(AniesBase):
    """
    Includes name, value, objectValue and module. Ignores timestampValue.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["AniesNameValueObjectValueModule"]
    class_class_curie: ClassVar[str] = "ILCDsd:AniesNameValueObjectValueModule"
    class_name: ClassVar[str] = "AniesNameValueObjectValueModule"
    class_model_uri: ClassVar[URIRef] = ILCDSD.AniesNameValueObjectValueModule

    id: Union[str, AniesNameValueObjectValueModuleId] = None
    timestampValue: Optional[int] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AniesNameValueObjectValueModuleId):
            self.id = AniesNameValueObjectValueModuleId(self.id)

        if self.timestampValue is not None and not isinstance(self.timestampValue, int):
            self.timestampValue = int(self.timestampValue)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesNameTypedReference(AniesBase):
    """
    An anies pattern where 'name' is required and 'objectValue' is a ShortDescripTypeRefVersion.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["AniesNameTypedReference"]
    class_class_curie: ClassVar[str] = "ILCDsd:AniesNameTypedReference"
    class_name: ClassVar[str] = "AniesNameTypedReference"
    class_model_uri: ClassVar[URIRef] = ILCDSD.AniesNameTypedReference

    id: Union[str, AniesNameTypedReferenceId] = None
    value: Optional[str] = None
    timestampValue: Optional[int] = None
    module: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AniesNameTypedReferenceId):
            self.id = AniesNameTypedReferenceId(self.id)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.timestampValue is not None and not isinstance(self.timestampValue, int):
            self.timestampValue = int(self.timestampValue)

        if self.module is not None and not isinstance(self.module, str):
            self.module = str(self.module)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesWithScenario(AniesBase):
    """
    Anies object that allows scenarios.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["AniesWithScenario"]
    class_class_curie: ClassVar[str] = "ILCDsd:AniesWithScenario"
    class_name: ClassVar[str] = "AniesWithScenario"
    class_model_uri: ClassVar[URIRef] = ILCDSD.AniesWithScenario

    id: Union[str, AniesWithScenarioId] = None
    name: Optional[str] = None
    value: Optional[str] = None
    timestampValue: Optional[int] = None
    objectValue: Optional[Union[dict, GlobalReferenceType]] = None
    module: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AniesWithScenarioId):
            self.id = AniesWithScenarioId(self.id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.timestampValue is not None and not isinstance(self.timestampValue, int):
            self.timestampValue = int(self.timestampValue)

        if self.objectValue is not None and not isinstance(self.objectValue, GlobalReferenceType):
            self.objectValue = GlobalReferenceType(**as_dict(self.objectValue))

        if self.module is not None and not isinstance(self.module, str):
            self.module = str(self.module)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Scenario(YAMLRoot):
    """
    A list of scenarios stored inside 'anies'.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["Scenario"]
    class_class_curie: ClassVar[str] = "ILCDsd:Scenario"
    class_name: ClassVar[str] = "Scenario"
    class_model_uri: ClassVar[URIRef] = ILCDSD.Scenario

    id: Union[str, ScenarioId] = None
    description: Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, "MultiLangString"]], List[Union[dict, "MultiLangString"]]]] = empty_dict()
    name: Optional[str] = None
    default: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ScenarioId):
            self.id = ScenarioId(self.id)

        self._normalize_inlined_as_list(slot_name="description", slot_type=MultiLangString, key_name="id", keyed=True)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.default is not None and not isinstance(self.default, Bool):
            self.default = Bool(self.default)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MultiLangString(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["MultiLangString"]
    class_class_curie: ClassVar[str] = "ILCDsd:MultiLangString"
    class_name: ClassVar[str] = "MultiLangString"
    class_model_uri: ClassVar[URIRef] = ILCDSD.MultiLangString

    id: Union[str, MultiLangStringId] = None
    value: Optional[str] = None
    lang: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MultiLangStringId):
            self.id = MultiLangStringId(self.id)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.lang is not None and not isinstance(self.lang, str):
            self.lang = str(self.lang)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=ILCDSD.id, name="id", curie=ILCDSD.curie('id'),
                   model_uri=ILCDSD.id, domain=None, range=URIRef)

slots.shortDescription = Slot(uri=ILCDSD.shortDescription, name="shortDescription", curie=ILCDSD.curie('shortDescription'),
                   model_uri=ILCDSD.shortDescription, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.description = Slot(uri=ILCDSD.description, name="description", curie=ILCDSD.curie('description'),
                   model_uri=ILCDSD.description, domain=None, range=Optional[Union[Dict[Union[str, MultiLangStringId], Union[dict, MultiLangString]], List[Union[dict, MultiLangString]]]])

slots.type = Slot(uri=ILCDSD.type, name="type", curie=ILCDSD.curie('type'),
                   model_uri=ILCDSD.type, domain=None, range=Optional[str])

slots.refObjectId = Slot(uri=ILCDSD.refObjectId, name="refObjectId", curie=ILCDSD.curie('refObjectId'),
                   model_uri=ILCDSD.refObjectId, domain=None, range=Optional[str])

slots.version = Slot(uri=ILCDSD.version, name="version", curie=ILCDSD.curie('version'),
                   model_uri=ILCDSD.version, domain=None, range=Optional[str])

slots.name = Slot(uri=ILCDSD.name, name="name", curie=ILCDSD.curie('name'),
                   model_uri=ILCDSD.name, domain=None, range=Optional[str])

slots.value = Slot(uri=ILCDSD.value, name="value", curie=ILCDSD.curie('value'),
                   model_uri=ILCDSD.value, domain=None, range=Optional[str])

slots.timestampValue = Slot(uri=ILCDSD.timestampValue, name="timestampValue", curie=ILCDSD.curie('timestampValue'),
                   model_uri=ILCDSD.timestampValue, domain=None, range=Optional[int])

slots.objectValue = Slot(uri=ILCDSD.objectValue, name="objectValue", curie=ILCDSD.curie('objectValue'),
                   model_uri=ILCDSD.objectValue, domain=None, range=Optional[Union[dict, GlobalReferenceType]])

slots.anies = Slot(uri=ILCDSD.anies, name="anies", curie=ILCDSD.curie('anies'),
                   model_uri=ILCDSD.anies, domain=None, range=Optional[Union[Dict[Union[str, AniesBaseId], Union[dict, AniesBase]], List[Union[dict, AniesBase]]]])

slots.lang = Slot(uri=ILCDSD.lang, name="lang", curie=ILCDSD.curie('lang'),
                   model_uri=ILCDSD.lang, domain=None, range=Optional[str])

slots.refObjectUri = Slot(uri=ILCDSD.refObjectUri, name="refObjectUri", curie=ILCDSD.curie('refObjectUri'),
                   model_uri=ILCDSD.refObjectUri, domain=None, range=Optional[str])

slots.UUID = Slot(uri=ILCDSD.UUID, name="UUID", curie=ILCDSD.curie('UUID'),
                   model_uri=ILCDSD.UUID, domain=None, range=str)

slots.module = Slot(uri=ILCDSD.module, name="module", curie=ILCDSD.curie('module'),
                   model_uri=ILCDSD.module, domain=None, range=Optional[str])

slots.meanAmount = Slot(uri=ILCDSD.meanAmount, name="meanAmount", curie=ILCDSD.curie('meanAmount'),
                   model_uri=ILCDSD.meanAmount, domain=None, range=Optional[float])

slots.objectScenario = Slot(uri=ILCDSD.objectScenario, name="objectScenario", curie=ILCDSD.curie('objectScenario'),
                   model_uri=ILCDSD.objectScenario, domain=None, range=Optional[Union[Dict[Union[str, ScenarioId], Union[dict, Scenario]], List[Union[dict, Scenario]]]])

slots.default = Slot(uri=ILCDSD.default, name="default", curie=ILCDSD.curie('default'),
                   model_uri=ILCDSD.default, domain=None, range=Optional[Union[bool, Bool]])

slots.margins = Slot(uri=ILCDSD.margins, name="margins", curie=ILCDSD.curie('margins'),
                   model_uri=ILCDSD.margins, domain=None, range=Optional[float])

slots.scenario = Slot(uri=ILCDSD.scenario, name="scenario", curie=ILCDSD.curie('scenario'),
                   model_uri=ILCDSD.scenario, domain=None, range=Optional[str])

slots.uncertaintyDistributionType = Slot(uri=ILCDSD.uncertaintyDistributionType, name="uncertaintyDistributionType", curie=ILCDSD.curie('uncertaintyDistributionType'),
                   model_uri=ILCDSD.uncertaintyDistributionType, domain=None, range=Optional[str])

slots.aniesBase__id = Slot(uri=ILCDSD.id, name="aniesBase__id", curie=ILCDSD.curie('id'),
                   model_uri=ILCDSD.aniesBase__id, domain=None, range=URIRef)

slots.multiLangString__id = Slot(uri=ILCDSD.id, name="multiLangString__id", curie=ILCDSD.curie('id'),
                   model_uri=ILCDSD.multiLangString__id, domain=None, range=URIRef)

slots.AniesNameValue_timestampValue = Slot(uri=ILCDSD.timestampValue, name="AniesNameValue_timestampValue", curie=ILCDSD.curie('timestampValue'),
                   model_uri=ILCDSD.AniesNameValue_timestampValue, domain=AniesNameValue, range=Optional[int])

slots.AniesNameValue_objectValue = Slot(uri=ILCDSD.objectValue, name="AniesNameValue_objectValue", curie=ILCDSD.curie('objectValue'),
                   model_uri=ILCDSD.AniesNameValue_objectValue, domain=AniesNameValue, range=Optional[Union[dict, GlobalReferenceType]])

slots.AniesNameValue_module = Slot(uri=ILCDSD.module, name="AniesNameValue_module", curie=ILCDSD.curie('module'),
                   model_uri=ILCDSD.AniesNameValue_module, domain=AniesNameValue, range=Optional[str])

slots.AniesNameValueModule_timestampValue = Slot(uri=ILCDSD.timestampValue, name="AniesNameValueModule_timestampValue", curie=ILCDSD.curie('timestampValue'),
                   model_uri=ILCDSD.AniesNameValueModule_timestampValue, domain=AniesNameValueModule, range=Optional[int])

slots.AniesNameValueModule_objectValue = Slot(uri=ILCDSD.objectValue, name="AniesNameValueModule_objectValue", curie=ILCDSD.curie('objectValue'),
                   model_uri=ILCDSD.AniesNameValueModule_objectValue, domain=AniesNameValueModule, range=Optional[Union[dict, GlobalReferenceType]])

slots.AniesNameValueModule_module = Slot(uri=ILCDSD.module, name="AniesNameValueModule_module", curie=ILCDSD.curie('module'),
                   model_uri=ILCDSD.AniesNameValueModule_module, domain=AniesNameValueModule, range=str)

slots.AniesNameTimestamp_value = Slot(uri=ILCDSD.value, name="AniesNameTimestamp_value", curie=ILCDSD.curie('value'),
                   model_uri=ILCDSD.AniesNameTimestamp_value, domain=AniesNameTimestamp, range=Optional[str])

slots.AniesNameTimestamp_objectValue = Slot(uri=ILCDSD.objectValue, name="AniesNameTimestamp_objectValue", curie=ILCDSD.curie('objectValue'),
                   model_uri=ILCDSD.AniesNameTimestamp_objectValue, domain=AniesNameTimestamp, range=Optional[Union[dict, GlobalReferenceType]])

slots.AniesNameTimestamp_module = Slot(uri=ILCDSD.module, name="AniesNameTimestamp_module", curie=ILCDSD.curie('module'),
                   model_uri=ILCDSD.AniesNameTimestamp_module, domain=AniesNameTimestamp, range=Optional[str])

slots.AniesNameObjectValue_value = Slot(uri=ILCDSD.value, name="AniesNameObjectValue_value", curie=ILCDSD.curie('value'),
                   model_uri=ILCDSD.AniesNameObjectValue_value, domain=AniesNameObjectValue, range=Optional[str])

slots.AniesNameObjectValue_timestampValue = Slot(uri=ILCDSD.timestampValue, name="AniesNameObjectValue_timestampValue", curie=ILCDSD.curie('timestampValue'),
                   model_uri=ILCDSD.AniesNameObjectValue_timestampValue, domain=AniesNameObjectValue, range=Optional[int])

slots.AniesNameObjectValue_module = Slot(uri=ILCDSD.module, name="AniesNameObjectValue_module", curie=ILCDSD.curie('module'),
                   model_uri=ILCDSD.AniesNameObjectValue_module, domain=AniesNameObjectValue, range=Optional[str])

slots.AniesNameValueObjectValueModule_timestampValue = Slot(uri=ILCDSD.timestampValue, name="AniesNameValueObjectValueModule_timestampValue", curie=ILCDSD.curie('timestampValue'),
                   model_uri=ILCDSD.AniesNameValueObjectValueModule_timestampValue, domain=AniesNameValueObjectValueModule, range=Optional[int])

slots.AniesNameTypedReference_value = Slot(uri=ILCDSD.value, name="AniesNameTypedReference_value", curie=ILCDSD.curie('value'),
                   model_uri=ILCDSD.AniesNameTypedReference_value, domain=AniesNameTypedReference, range=Optional[str])

slots.AniesNameTypedReference_timestampValue = Slot(uri=ILCDSD.timestampValue, name="AniesNameTypedReference_timestampValue", curie=ILCDSD.curie('timestampValue'),
                   model_uri=ILCDSD.AniesNameTypedReference_timestampValue, domain=AniesNameTypedReference, range=Optional[int])

slots.AniesNameTypedReference_module = Slot(uri=ILCDSD.module, name="AniesNameTypedReference_module", curie=ILCDSD.curie('module'),
                   model_uri=ILCDSD.AniesNameTypedReference_module, domain=AniesNameTypedReference, range=Optional[str])

slots.AniesWithScenario_name = Slot(uri=ILCDSD.name, name="AniesWithScenario_name", curie=ILCDSD.curie('name'),
                   model_uri=ILCDSD.AniesWithScenario_name, domain=AniesWithScenario, range=Optional[str])

slots.AniesWithScenario_value = Slot(uri=ILCDSD.value, name="AniesWithScenario_value", curie=ILCDSD.curie('value'),
                   model_uri=ILCDSD.AniesWithScenario_value, domain=AniesWithScenario, range=Optional[str])

slots.AniesWithScenario_timestampValue = Slot(uri=ILCDSD.timestampValue, name="AniesWithScenario_timestampValue", curie=ILCDSD.curie('timestampValue'),
                   model_uri=ILCDSD.AniesWithScenario_timestampValue, domain=AniesWithScenario, range=Optional[int])

slots.AniesWithScenario_objectValue = Slot(uri=ILCDSD.objectValue, name="AniesWithScenario_objectValue", curie=ILCDSD.curie('objectValue'),
                   model_uri=ILCDSD.AniesWithScenario_objectValue, domain=AniesWithScenario, range=Optional[Union[dict, GlobalReferenceType]])

slots.AniesWithScenario_module = Slot(uri=ILCDSD.module, name="AniesWithScenario_module", curie=ILCDSD.curie('module'),
                   model_uri=ILCDSD.AniesWithScenario_module, domain=AniesWithScenario, range=Optional[str])