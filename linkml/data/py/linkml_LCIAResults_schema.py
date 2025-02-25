# Auto generated from linkml_LCIAResults_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-02-25T13:39:00
# Schema: ILCDLCIAResults
#
# id: https://example.org/ILCDLCIAResults
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

from . linkml_shared_definitions import MultiLangString, ShortDescripTypeRefVersion, ShortDescripTypeRefVersionUri, UUIDType
from linkml_runtime.linkml_model.types import Float, String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCDLCIA = CurieNamespace('ILCDlcia', 'https://example.org/ILCDLCIAResults/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCDLCIA


# Types

# Class references
class LCIAResultsId(extended_str):
    pass


class LCIAResultEntryId(extended_str):
    pass


class LCIAOtherContentId(extended_str):
    pass


class AniesLCIAResultEntryId(extended_str):
    pass


class ReferenceToLCIAMethodDataSetEntryId(extended_str):
    pass


@dataclass(repr=False)
class LCIAResults(YAMLRoot):
    """
    Top-level container for the LCIAResults section.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDLCIA["LCIAResults"]
    class_class_curie: ClassVar[str] = "ILCDlcia:LCIAResults"
    class_name: ClassVar[str] = "LCIAResults"
    class_model_uri: ClassVar[URIRef] = ILCDLCIA.LCIAResults

    id: Union[str, LCIAResultsId] = None
    LCIAResult: Optional[Union[Dict[Union[str, LCIAResultEntryId], Union[dict, "LCIAResultEntry"]], List[Union[dict, "LCIAResultEntry"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LCIAResultsId):
            self.id = LCIAResultsId(self.id)

        self._normalize_inlined_as_list(slot_name="LCIAResult", slot_type=LCIAResultEntry, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LCIAResultEntry(YAMLRoot):
    """
    Represents a single LCIA result object.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDLCIA["LCIAResultEntry"]
    class_class_curie: ClassVar[str] = "ILCDlcia:LCIAResultEntry"
    class_name: ClassVar[str] = "LCIAResultEntry"
    class_model_uri: ClassVar[URIRef] = ILCDLCIA.LCIAResultEntry

    id: Union[str, LCIAResultEntryId] = None
    referenceToLCIAMethodDataSet: Optional[Union[dict, "ReferenceToLCIAMethodDataSetEntry"]] = None
    meanAmount: Optional[float] = None
    otherLCIA: Optional[Union[dict, "LCIAOtherContent"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LCIAResultEntryId):
            self.id = LCIAResultEntryId(self.id)

        if self.referenceToLCIAMethodDataSet is not None and not isinstance(self.referenceToLCIAMethodDataSet, ReferenceToLCIAMethodDataSetEntry):
            self.referenceToLCIAMethodDataSet = ReferenceToLCIAMethodDataSetEntry(**as_dict(self.referenceToLCIAMethodDataSet))

        if self.meanAmount is not None and not isinstance(self.meanAmount, float):
            self.meanAmount = float(self.meanAmount)

        if self.otherLCIA is not None and not isinstance(self.otherLCIA, LCIAOtherContent):
            self.otherLCIA = LCIAOtherContent(**as_dict(self.otherLCIA))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LCIAOtherContent(YAMLRoot):
    """
    Custom class for LCIA 'other'.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDLCIA["LCIAOtherContent"]
    class_class_curie: ClassVar[str] = "ILCDlcia:LCIAOtherContent"
    class_name: ClassVar[str] = "LCIAOtherContent"
    class_model_uri: ClassVar[URIRef] = ILCDLCIA.LCIAOtherContent

    id: Union[str, LCIAOtherContentId] = None
    aniesLCIAResult: Optional[Union[Dict[Union[str, AniesLCIAResultEntryId], Union[dict, "AniesLCIAResultEntry"]], List[Union[dict, "AniesLCIAResultEntry"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LCIAOtherContentId):
            self.id = LCIAOtherContentId(self.id)

        self._normalize_inlined_as_list(slot_name="aniesLCIAResult", slot_type=AniesLCIAResultEntry, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesLCIAResultEntry(YAMLRoot):
    """
    Specialized class for modules with an explicit ID for named resources.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDLCIA["AniesLCIAResultEntry"]
    class_class_curie: ClassVar[str] = "ILCDlcia:AniesLCIAResultEntry"
    class_name: ClassVar[str] = "aniesLCIAResultEntry"
    class_model_uri: ClassVar[URIRef] = ILCDLCIA.AniesLCIAResultEntry

    id: Union[str, AniesLCIAResultEntryId] = None
    value: Optional[str] = None
    module: Optional[str] = None
    name: Optional[str] = None
    objectValue: Optional[Union[dict, ShortDescripTypeRefVersion]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AniesLCIAResultEntryId):
            self.id = AniesLCIAResultEntryId(self.id)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.module is not None and not isinstance(self.module, str):
            self.module = str(self.module)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.objectValue is not None and not isinstance(self.objectValue, ShortDescripTypeRefVersion):
            self.objectValue = ShortDescripTypeRefVersion(**as_dict(self.objectValue))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReferenceToLCIAMethodDataSetEntry(ShortDescripTypeRefVersionUri):
    """
    Local sub-class for referenceToLCIAMethodDataSet, inheriting from ShortDescripTypeRefVersionUri
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDLCIA["ReferenceToLCIAMethodDataSetEntry"]
    class_class_curie: ClassVar[str] = "ILCDlcia:ReferenceToLCIAMethodDataSetEntry"
    class_name: ClassVar[str] = "referenceToLCIAMethodDataSetEntry"
    class_model_uri: ClassVar[URIRef] = ILCDLCIA.ReferenceToLCIAMethodDataSetEntry

    id: Union[str, ReferenceToLCIAMethodDataSetEntryId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReferenceToLCIAMethodDataSetEntryId):
            self.id = ReferenceToLCIAMethodDataSetEntryId(self.id)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.LCIAResult = Slot(uri=ILCDLCIA.LCIAResult, name="LCIAResult", curie=ILCDLCIA.curie('LCIAResult'),
                   model_uri=ILCDLCIA.LCIAResult, domain=None, range=Optional[Union[Dict[Union[str, LCIAResultEntryId], Union[dict, LCIAResultEntry]], List[Union[dict, LCIAResultEntry]]]])

slots.referenceToLCIAMethodDataSet = Slot(uri=ILCDLCIA.referenceToLCIAMethodDataSet, name="referenceToLCIAMethodDataSet", curie=ILCDLCIA.curie('referenceToLCIAMethodDataSet'),
                   model_uri=ILCDLCIA.referenceToLCIAMethodDataSet, domain=None, range=Optional[Union[dict, ReferenceToLCIAMethodDataSetEntry]])

slots.meanAmount = Slot(uri=ILCDLCIA.meanAmount, name="meanAmount", curie=ILCDLCIA.curie('meanAmount'),
                   model_uri=ILCDLCIA.meanAmount, domain=None, range=Optional[float])

slots.otherLCIA = Slot(uri=ILCDLCIA.otherLCIA, name="otherLCIA", curie=ILCDLCIA.curie('otherLCIA'),
                   model_uri=ILCDLCIA.otherLCIA, domain=None, range=Optional[Union[dict, LCIAOtherContent]])

slots.aniesLCIAResult = Slot(uri=ILCDLCIA.aniesLCIAResult, name="aniesLCIAResult", curie=ILCDLCIA.curie('aniesLCIAResult'),
                   model_uri=ILCDLCIA.aniesLCIAResult, domain=None, range=Optional[Union[Dict[Union[str, AniesLCIAResultEntryId], Union[dict, AniesLCIAResultEntry]], List[Union[dict, AniesLCIAResultEntry]]]])

slots.lCIAResults__id = Slot(uri=ILCDLCIA.id, name="lCIAResults__id", curie=ILCDLCIA.curie('id'),
                   model_uri=ILCDLCIA.lCIAResults__id, domain=None, range=URIRef)

slots.lCIAResultEntry__id = Slot(uri=ILCDLCIA.id, name="lCIAResultEntry__id", curie=ILCDLCIA.curie('id'),
                   model_uri=ILCDLCIA.lCIAResultEntry__id, domain=None, range=URIRef)

slots.referenceToLCIAMethodDataSetEntry__id = Slot(uri=ILCDLCIA.id, name="referenceToLCIAMethodDataSetEntry__id", curie=ILCDLCIA.curie('id'),
                   model_uri=ILCDLCIA.referenceToLCIAMethodDataSetEntry__id, domain=None, range=URIRef)

slots.lCIAOtherContent__id = Slot(uri=ILCDLCIA.id, name="lCIAOtherContent__id", curie=ILCDLCIA.curie('id'),
                   model_uri=ILCDLCIA.lCIAOtherContent__id, domain=None, range=URIRef)

slots.aniesLCIAResultEntry__id = Slot(uri=ILCDLCIA.id, name="aniesLCIAResultEntry__id", curie=ILCDLCIA.curie('id'),
                   model_uri=ILCDLCIA.aniesLCIAResultEntry__id, domain=None, range=URIRef)