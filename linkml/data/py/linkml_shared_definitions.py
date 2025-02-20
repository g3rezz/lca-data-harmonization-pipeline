# Auto generated from linkml_shared_definitions.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-02-20T11:54:33
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

from linkml_runtime.linkml_model.types import String

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


class AnyObject(str):
    """ Placeholder for any dictionary-like JSON object. """
    type_class_uri = LINKML["AnyObject"]
    type_class_curie = "linkml:AnyObject"
    type_name = "AnyObject"
    type_model_uri = ILCDSD.AnyObject


# Class references



@dataclass(repr=False)
class ShortDescripTypeRef(YAMLRoot):
    """
    Base pattern with shortDescription, type, refObjectId.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["ShortDescripTypeRef"]
    class_class_curie: ClassVar[str] = "ILCDsd:ShortDescripTypeRef"
    class_name: ClassVar[str] = "ShortDescripTypeRef"
    class_model_uri: ClassVar[URIRef] = ILCDSD.ShortDescripTypeRef

    shortDescription: Optional[Union[Union[dict, "MultiLangString"], List[Union[dict, "MultiLangString"]]]] = empty_list()
    type: Optional[str] = None
    refObjectId: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.shortDescription, list):
            self.shortDescription = [self.shortDescription] if self.shortDescription is not None else []
        self.shortDescription = [v if isinstance(v, MultiLangString) else MultiLangString(**as_dict(v)) for v in self.shortDescription]

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.refObjectId is not None and not isinstance(self.refObjectId, str):
            self.refObjectId = str(self.refObjectId)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ShortDescripTypeRefVersion(YAMLRoot):
    """
    Base pattern with shortDescription, type, refObjectId, version.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["ShortDescripTypeRefVersion"]
    class_class_curie: ClassVar[str] = "ILCDsd:ShortDescripTypeRefVersion"
    class_name: ClassVar[str] = "ShortDescripTypeRefVersion"
    class_model_uri: ClassVar[URIRef] = ILCDSD.ShortDescripTypeRefVersion

    shortDescription: Optional[Union[Union[dict, "MultiLangString"], List[Union[dict, "MultiLangString"]]]] = empty_list()
    type: Optional[str] = None
    refObjectId: Optional[str] = None
    version: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.shortDescription, list):
            self.shortDescription = [self.shortDescription] if self.shortDescription is not None else []
        self.shortDescription = [v if isinstance(v, MultiLangString) else MultiLangString(**as_dict(v)) for v in self.shortDescription]

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.refObjectId is not None and not isinstance(self.refObjectId, str):
            self.refObjectId = str(self.refObjectId)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ShortDescripAndType(YAMLRoot):
    """
    Holds shortDescription and type only.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["ShortDescripAndType"]
    class_class_curie: ClassVar[str] = "ILCDsd:ShortDescripAndType"
    class_name: ClassVar[str] = "ShortDescripAndType"
    class_model_uri: ClassVar[URIRef] = ILCDSD.ShortDescripAndType

    shortDescription: Optional[Union[Union[dict, "MultiLangString"], List[Union[dict, "MultiLangString"]]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.shortDescription, list):
            self.shortDescription = [self.shortDescription] if self.shortDescription is not None else []
        self.shortDescription = [v if isinstance(v, MultiLangString) else MultiLangString(**as_dict(v)) for v in self.shortDescription]

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OtherContent(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["OtherContent"]
    class_class_curie: ClassVar[str] = "ILCDsd:OtherContent"
    class_name: ClassVar[str] = "OtherContent"
    class_model_uri: ClassVar[URIRef] = ILCDSD.OtherContent

    anies: Optional[Union[Union[dict, "AniesEntry"], List[Union[dict, "AniesEntry"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.anies, list):
            self.anies = [self.anies] if self.anies is not None else []
        self.anies = [v if isinstance(v, AniesEntry) else AniesEntry(**as_dict(v)) for v in self.anies]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesEntry(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["AniesEntry"]
    class_class_curie: ClassVar[str] = "ILCDsd:AniesEntry"
    class_name: ClassVar[str] = "AniesEntry"
    class_model_uri: ClassVar[URIRef] = ILCDSD.AniesEntry

    name: Optional[str] = None
    value: Optional[str] = None
    timestampValue: Optional[int] = None
    objectValue: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.timestampValue is not None and not isinstance(self.timestampValue, int):
            self.timestampValue = int(self.timestampValue)

        if self.objectValue is not None and not isinstance(self.objectValue, str):
            self.objectValue = str(self.objectValue)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MultiLangString(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDSD["MultiLangString"]
    class_class_curie: ClassVar[str] = "ILCDsd:MultiLangString"
    class_name: ClassVar[str] = "MultiLangString"
    class_model_uri: ClassVar[URIRef] = ILCDSD.MultiLangString

    value: Optional[str] = None
    lang: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.lang is not None and not isinstance(self.lang, str):
            self.lang = str(self.lang)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.shortDescription = Slot(uri=ILCDSD.shortDescription, name="shortDescription", curie=ILCDSD.curie('shortDescription'),
                   model_uri=ILCDSD.shortDescription, domain=None, range=Optional[Union[Union[dict, MultiLangString], List[Union[dict, MultiLangString]]]])

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
                   model_uri=ILCDSD.objectValue, domain=None, range=Optional[str])

slots.anies = Slot(uri=ILCDSD.anies, name="anies", curie=ILCDSD.curie('anies'),
                   model_uri=ILCDSD.anies, domain=None, range=Optional[Union[Union[dict, AniesEntry], List[Union[dict, AniesEntry]]]])

slots.lang = Slot(uri=ILCDSD.lang, name="lang", curie=ILCDSD.curie('lang'),
                   model_uri=ILCDSD.lang, domain=None, range=Optional[str])