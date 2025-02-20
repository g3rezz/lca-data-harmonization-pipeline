# Auto generated from linkml_exchanges_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-02-20T16:07:13
# Schema: ILCDexchanges
#
# id: https://example.org/ILCDexchanges
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

from . linkml_shared_definitions import MaterialPropEntry, OtherContent, ShortDescripTypeRefVersion, UUIDType
from linkml_runtime.linkml_model.types import Boolean, Float, Integer, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCDEX = CurieNamespace('ILCDex', 'https://example.org/ILCDexchanges/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCDEX


# Types

# Class references



@dataclass(repr=False)
class Exchanges(YAMLRoot):
    """
    Top-level container for the 'exchanges' section.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDEX["Exchanges"]
    class_class_curie: ClassVar[str] = "ILCDex:Exchanges"
    class_name: ClassVar[str] = "Exchanges"
    class_model_uri: ClassVar[URIRef] = ILCDEX.Exchanges

    exchange: Optional[Union[Union[dict, "ExchangeEntry"], List[Union[dict, "ExchangeEntry"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.exchange, list):
            self.exchange = [self.exchange] if self.exchange is not None else []
        self.exchange = [v if isinstance(v, ExchangeEntry) else ExchangeEntry(**as_dict(v)) for v in self.exchange]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExchangeEntry(YAMLRoot):
    """
    A single exchange entry with flow data, amounts, and properties.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDEX["ExchangeEntry"]
    class_class_curie: ClassVar[str] = "ILCDex:ExchangeEntry"
    class_name: ClassVar[str] = "ExchangeEntry"
    class_model_uri: ClassVar[URIRef] = ILCDEX.ExchangeEntry

    dataSetInternalID: Optional[int] = None
    referenceToFlowDataSet: Optional[Union[dict, ShortDescripTypeRefVersion]] = None
    meanAmount: Optional[float] = None
    referenceFlow: Optional[Union[bool, Bool]] = None
    resultingflowAmount: Optional[float] = None
    flowProperties: Optional[Union[Union[dict, "FlowPropertyEntry"], List[Union[dict, "FlowPropertyEntry"]]]] = empty_list()
    resolvedFlowVersion: Optional[str] = None
    materialProperties: Optional[Union[Union[dict, MaterialPropEntry], List[Union[dict, MaterialPropEntry]]]] = empty_list()
    typeOfFlow: Optional[str] = None
    exchangeDirection: Optional[str] = None
    otherEx: Optional[Union[dict, OtherContent]] = None
    classificationEx: Optional[Union[dict, "ExchangeClassification"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.dataSetInternalID is not None and not isinstance(self.dataSetInternalID, int):
            self.dataSetInternalID = int(self.dataSetInternalID)

        if self.referenceToFlowDataSet is not None and not isinstance(self.referenceToFlowDataSet, ShortDescripTypeRefVersion):
            self.referenceToFlowDataSet = ShortDescripTypeRefVersion(**as_dict(self.referenceToFlowDataSet))

        if self.meanAmount is not None and not isinstance(self.meanAmount, float):
            self.meanAmount = float(self.meanAmount)

        if self.referenceFlow is not None and not isinstance(self.referenceFlow, Bool):
            self.referenceFlow = Bool(self.referenceFlow)

        if self.resultingflowAmount is not None and not isinstance(self.resultingflowAmount, float):
            self.resultingflowAmount = float(self.resultingflowAmount)

        if not isinstance(self.flowProperties, list):
            self.flowProperties = [self.flowProperties] if self.flowProperties is not None else []
        self.flowProperties = [v if isinstance(v, FlowPropertyEntry) else FlowPropertyEntry(**as_dict(v)) for v in self.flowProperties]

        if self.resolvedFlowVersion is not None and not isinstance(self.resolvedFlowVersion, str):
            self.resolvedFlowVersion = str(self.resolvedFlowVersion)

        if not isinstance(self.materialProperties, list):
            self.materialProperties = [self.materialProperties] if self.materialProperties is not None else []
        self.materialProperties = [v if isinstance(v, MaterialPropEntry) else MaterialPropEntry(**as_dict(v)) for v in self.materialProperties]

        if self.typeOfFlow is not None and not isinstance(self.typeOfFlow, str):
            self.typeOfFlow = str(self.typeOfFlow)

        if self.exchangeDirection is not None and not isinstance(self.exchangeDirection, str):
            self.exchangeDirection = str(self.exchangeDirection)

        if self.otherEx is not None and not isinstance(self.otherEx, OtherContent):
            self.otherEx = OtherContent(**as_dict(self.otherEx))

        if self.classificationEx is not None and not isinstance(self.classificationEx, ExchangeClassification):
            self.classificationEx = ExchangeClassification(**as_dict(self.classificationEx))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FlowPropertyEntry(YAMLRoot):
    """
    One flow property with name, uuid, referenceFlowProperty, meanValue, referenceUnit, unitGroupUUID.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDEX["FlowPropertyEntry"]
    class_class_curie: ClassVar[str] = "ILCDex:FlowPropertyEntry"
    class_name: ClassVar[str] = "FlowPropertyEntry"
    class_model_uri: ClassVar[URIRef] = ILCDEX.FlowPropertyEntry

    name: Optional[str] = None
    uuidFP: Optional[str] = None
    referenceFlowProperty: Optional[Union[bool, Bool]] = None
    meanValue: Optional[float] = None
    referenceUnit: Optional[str] = None
    unitGroupUUID: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.uuidFP is not None and not isinstance(self.uuidFP, str):
            self.uuidFP = str(self.uuidFP)

        if self.referenceFlowProperty is not None and not isinstance(self.referenceFlowProperty, Bool):
            self.referenceFlowProperty = Bool(self.referenceFlowProperty)

        if self.meanValue is not None and not isinstance(self.meanValue, float):
            self.meanValue = float(self.meanValue)

        if self.referenceUnit is not None and not isinstance(self.referenceUnit, str):
            self.referenceUnit = str(self.referenceUnit)

        if self.unitGroupUUID is not None and not isinstance(self.unitGroupUUID, str):
            self.unitGroupUUID = str(self.unitGroupUUID)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExchangeClassification(YAMLRoot):
    """
    Simple object for classification with 'classHierarchy' and 'name'.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDEX["ExchangeClassification"]
    class_class_curie: ClassVar[str] = "ILCDex:ExchangeClassification"
    class_name: ClassVar[str] = "ExchangeClassification"
    class_model_uri: ClassVar[URIRef] = ILCDEX.ExchangeClassification

    classHierarchy: Optional[str] = None
    nameClass: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.classHierarchy is not None and not isinstance(self.classHierarchy, str):
            self.classHierarchy = str(self.classHierarchy)

        if self.nameClass is not None and not isinstance(self.nameClass, str):
            self.nameClass = str(self.nameClass)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.exchange = Slot(uri=ILCDEX.exchange, name="exchange", curie=ILCDEX.curie('exchange'),
                   model_uri=ILCDEX.exchange, domain=None, range=Optional[Union[Union[dict, ExchangeEntry], List[Union[dict, ExchangeEntry]]]])

slots.dataSetInternalID = Slot(uri=ILCDEX.dataSetInternalID, name="dataSetInternalID", curie=ILCDEX.curie('dataSetInternalID'),
                   model_uri=ILCDEX.dataSetInternalID, domain=None, range=Optional[int])

slots.referenceToFlowDataSet = Slot(uri=ILCDEX.referenceToFlowDataSet, name="referenceToFlowDataSet", curie=ILCDEX.curie('referenceToFlowDataSet'),
                   model_uri=ILCDEX.referenceToFlowDataSet, domain=None, range=Optional[Union[dict, ShortDescripTypeRefVersion]])

slots.meanAmount = Slot(uri=ILCDEX.meanAmount, name="meanAmount", curie=ILCDEX.curie('meanAmount'),
                   model_uri=ILCDEX.meanAmount, domain=None, range=Optional[float])

slots.referenceFlow = Slot(uri=ILCDEX.referenceFlow, name="referenceFlow", curie=ILCDEX.curie('referenceFlow'),
                   model_uri=ILCDEX.referenceFlow, domain=None, range=Optional[Union[bool, Bool]])

slots.resultingflowAmount = Slot(uri=ILCDEX.resultingflowAmount, name="resultingflowAmount", curie=ILCDEX.curie('resultingflowAmount'),
                   model_uri=ILCDEX.resultingflowAmount, domain=None, range=Optional[float])

slots.flowProperties = Slot(uri=ILCDEX.flowProperties, name="flowProperties", curie=ILCDEX.curie('flowProperties'),
                   model_uri=ILCDEX.flowProperties, domain=None, range=Optional[Union[Union[dict, FlowPropertyEntry], List[Union[dict, FlowPropertyEntry]]]])

slots.materialProperties = Slot(uri=ILCDEX.materialProperties, name="materialProperties", curie=ILCDEX.curie('materialProperties'),
                   model_uri=ILCDEX.materialProperties, domain=None, range=Optional[Union[Union[dict, MaterialPropEntry], List[Union[dict, MaterialPropEntry]]]])

slots.resolvedFlowVersion = Slot(uri=ILCDEX.resolvedFlowVersion, name="resolvedFlowVersion", curie=ILCDEX.curie('resolvedFlowVersion'),
                   model_uri=ILCDEX.resolvedFlowVersion, domain=None, range=Optional[str])

slots.typeOfFlow = Slot(uri=ILCDEX.typeOfFlow, name="typeOfFlow", curie=ILCDEX.curie('typeOfFlow'),
                   model_uri=ILCDEX.typeOfFlow, domain=None, range=Optional[str])

slots.exchangeDirection = Slot(uri=ILCDEX.exchangeDirection, name="exchangeDirection", curie=ILCDEX.curie('exchangeDirection'),
                   model_uri=ILCDEX.exchangeDirection, domain=None, range=Optional[str])

slots.otherEx = Slot(uri=ILCDEX.otherEx, name="otherEx", curie=ILCDEX.curie('otherEx'),
                   model_uri=ILCDEX.otherEx, domain=None, range=Optional[Union[dict, OtherContent]])

slots.classificationEx = Slot(uri=ILCDEX.classificationEx, name="classificationEx", curie=ILCDEX.curie('classificationEx'),
                   model_uri=ILCDEX.classificationEx, domain=None, range=Optional[Union[dict, ExchangeClassification]])

slots.uuidFP = Slot(uri=ILCDEX.uuidFP, name="uuidFP", curie=ILCDEX.curie('uuidFP'),
                   model_uri=ILCDEX.uuidFP, domain=None, range=Optional[str])

slots.referenceFlowProperty = Slot(uri=ILCDEX.referenceFlowProperty, name="referenceFlowProperty", curie=ILCDEX.curie('referenceFlowProperty'),
                   model_uri=ILCDEX.referenceFlowProperty, domain=None, range=Optional[Union[bool, Bool]])

slots.meanValue = Slot(uri=ILCDEX.meanValue, name="meanValue", curie=ILCDEX.curie('meanValue'),
                   model_uri=ILCDEX.meanValue, domain=None, range=Optional[float])

slots.referenceUnit = Slot(uri=ILCDEX.referenceUnit, name="referenceUnit", curie=ILCDEX.curie('referenceUnit'),
                   model_uri=ILCDEX.referenceUnit, domain=None, range=Optional[str])

slots.unitGroupUUID = Slot(uri=ILCDEX.unitGroupUUID, name="unitGroupUUID", curie=ILCDEX.curie('unitGroupUUID'),
                   model_uri=ILCDEX.unitGroupUUID, domain=None, range=Optional[str])

slots.classHierarchy = Slot(uri=ILCDEX.classHierarchy, name="classHierarchy", curie=ILCDEX.curie('classHierarchy'),
                   model_uri=ILCDEX.classHierarchy, domain=None, range=Optional[str])

slots.nameClass = Slot(uri=ILCDEX.nameClass, name="nameClass", curie=ILCDEX.curie('nameClass'),
                   model_uri=ILCDEX.nameClass, domain=None, range=Optional[str])