# Auto generated from linkml_processInformation_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-02-16T13:13:28
# Schema: ILCDprocessInformation
#
# id: https://example.org/ILCDprocessInformation
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

from linkml_runtime.linkml_model.types import Integer, String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
THIS = CurieNamespace('this', 'https://example.org/ILCDprocessInformation/')
DEFAULT_ = THIS


# Types
class UUIDType(str):
    """ Universally Unique Identifier. """
    type_class_uri = LINKML["UUIDType"]
    type_class_curie = "linkml:UUIDType"
    type_name = "UUIDType"
    type_model_uri = THIS.UUIDType


class Year(int):
    """ 4-digit year. """
    type_class_uri = LINKML["Year"]
    type_class_curie = "linkml:Year"
    type_name = "Year"
    type_model_uri = THIS.Year


# Class references



@dataclass(repr=False)
class ProcessInformation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["ProcessInformation"]
    class_class_curie: ClassVar[str] = "this:ProcessInformation"
    class_name: ClassVar[str] = "ProcessInformation"
    class_model_uri: ClassVar[URIRef] = THIS.ProcessInformation

    dataSetInformation: Optional[Union[dict, "DataSetInformation"]] = None
    quantitativeReference: Optional[Union[dict, "QuantitativeReference"]] = None
    time: Optional[Union[dict, "TimeInformation"]] = None
    geography: Optional[Union[dict, "GeographyInformation"]] = None
    technology: Optional[Union[dict, "TechnologyInformation"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.dataSetInformation is not None and not isinstance(self.dataSetInformation, DataSetInformation):
            self.dataSetInformation = DataSetInformation(**as_dict(self.dataSetInformation))

        if self.quantitativeReference is not None and not isinstance(self.quantitativeReference, QuantitativeReference):
            self.quantitativeReference = QuantitativeReference(**as_dict(self.quantitativeReference))

        if self.time is not None and not isinstance(self.time, TimeInformation):
            self.time = TimeInformation(**as_dict(self.time))

        if self.geography is not None and not isinstance(self.geography, GeographyInformation):
            self.geography = GeographyInformation(**as_dict(self.geography))

        if self.technology is not None and not isinstance(self.technology, TechnologyInformation):
            self.technology = TechnologyInformation(**as_dict(self.technology))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataSetInformation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["DataSetInformation"]
    class_class_curie: ClassVar[str] = "this:DataSetInformation"
    class_name: ClassVar[str] = "DataSetInformation"
    class_model_uri: ClassVar[URIRef] = THIS.DataSetInformation

    UUID: Optional[str] = None
    dataSetName: Optional[Union[dict, "DataSetName"]] = None
    classificationInformation: Optional[Union[dict, "ClassificationInformation"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.UUID is not None and not isinstance(self.UUID, str):
            self.UUID = str(self.UUID)

        if self.dataSetName is not None and not isinstance(self.dataSetName, DataSetName):
            self.dataSetName = DataSetName(**as_dict(self.dataSetName))

        if self.classificationInformation is not None and not isinstance(self.classificationInformation, ClassificationInformation):
            self.classificationInformation = ClassificationInformation(**as_dict(self.classificationInformation))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataSetName(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["DataSetName"]
    class_class_curie: ClassVar[str] = "this:DataSetName"
    class_name: ClassVar[str] = "DataSetName"
    class_model_uri: ClassVar[URIRef] = THIS.DataSetName

    baseName: Optional[Union[Union[dict, "MultiLangString"], List[Union[dict, "MultiLangString"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.baseName, list):
            self.baseName = [self.baseName] if self.baseName is not None else []
        self.baseName = [v if isinstance(v, MultiLangString) else MultiLangString(**as_dict(v)) for v in self.baseName]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClassificationInformation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["ClassificationInformation"]
    class_class_curie: ClassVar[str] = "this:ClassificationInformation"
    class_name: ClassVar[str] = "ClassificationInformation"
    class_model_uri: ClassVar[URIRef] = THIS.ClassificationInformation

    classification: Optional[Union[Union[dict, "Classification"], List[Union[dict, "Classification"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.classification, list):
            self.classification = [self.classification] if self.classification is not None else []
        self.classification = [v if isinstance(v, Classification) else Classification(**as_dict(v)) for v in self.classification]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Classification(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["Classification"]
    class_class_curie: ClassVar[str] = "this:Classification"
    class_name: ClassVar[str] = "Classification"
    class_model_uri: ClassVar[URIRef] = THIS.Classification

    name: Optional[str] = None
    classEntries: Optional[Union[Union[dict, "ClassificationEntry"], List[Union[dict, "ClassificationEntry"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if not isinstance(self.classEntries, list):
            self.classEntries = [self.classEntries] if self.classEntries is not None else []
        self.classEntries = [v if isinstance(v, ClassificationEntry) else ClassificationEntry(**as_dict(v)) for v in self.classEntries]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClassificationEntry(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["ClassificationEntry"]
    class_class_curie: ClassVar[str] = "this:ClassificationEntry"
    class_name: ClassVar[str] = "ClassificationEntry"
    class_model_uri: ClassVar[URIRef] = THIS.ClassificationEntry

    value: Optional[str] = None
    level: Optional[int] = None
    classId: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.level is not None and not isinstance(self.level, int):
            self.level = int(self.level)

        if self.classId is not None and not isinstance(self.classId, str):
            self.classId = str(self.classId)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QuantitativeReference(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["QuantitativeReference"]
    class_class_curie: ClassVar[str] = "this:QuantitativeReference"
    class_name: ClassVar[str] = "QuantitativeReference"
    class_model_uri: ClassVar[URIRef] = THIS.QuantitativeReference

    referenceToReferenceFlow: Optional[Union[int, List[int]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.referenceToReferenceFlow, list):
            self.referenceToReferenceFlow = [self.referenceToReferenceFlow] if self.referenceToReferenceFlow is not None else []
        self.referenceToReferenceFlow = [v if isinstance(v, int) else int(v) for v in self.referenceToReferenceFlow]

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TimeInformation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["TimeInformation"]
    class_class_curie: ClassVar[str] = "this:TimeInformation"
    class_name: ClassVar[str] = "TimeInformation"
    class_model_uri: ClassVar[URIRef] = THIS.TimeInformation

    referenceYear: Optional[int] = None
    dataSetValidUntil: Optional[int] = None
    timeRepresentativenessDescription: Optional[Union[Union[dict, "MultiLangString"], List[Union[dict, "MultiLangString"]]]] = empty_list()
    otherTime: Optional[Union[dict, "OtherContent"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.referenceYear is not None and not isinstance(self.referenceYear, int):
            self.referenceYear = int(self.referenceYear)

        if self.dataSetValidUntil is not None and not isinstance(self.dataSetValidUntil, int):
            self.dataSetValidUntil = int(self.dataSetValidUntil)

        if not isinstance(self.timeRepresentativenessDescription, list):
            self.timeRepresentativenessDescription = [self.timeRepresentativenessDescription] if self.timeRepresentativenessDescription is not None else []
        self.timeRepresentativenessDescription = [v if isinstance(v, MultiLangString) else MultiLangString(**as_dict(v)) for v in self.timeRepresentativenessDescription]

        if self.otherTime is not None and not isinstance(self.otherTime, OtherContent):
            self.otherTime = OtherContent(**as_dict(self.otherTime))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class OtherContent(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["OtherContent"]
    class_class_curie: ClassVar[str] = "this:OtherContent"
    class_name: ClassVar[str] = "OtherContent"
    class_model_uri: ClassVar[URIRef] = THIS.OtherContent

    anies: Optional[Union[Union[dict, "AniesEntry"], List[Union[dict, "AniesEntry"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.anies, list):
            self.anies = [self.anies] if self.anies is not None else []
        self.anies = [v if isinstance(v, AniesEntry) else AniesEntry(**as_dict(v)) for v in self.anies]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AniesEntry(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["AniesEntry"]
    class_class_curie: ClassVar[str] = "this:AniesEntry"
    class_name: ClassVar[str] = "AniesEntry"
    class_model_uri: ClassVar[URIRef] = THIS.AniesEntry

    name: Optional[str] = None
    value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GeographyInformation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["GeographyInformation"]
    class_class_curie: ClassVar[str] = "this:GeographyInformation"
    class_name: ClassVar[str] = "GeographyInformation"
    class_model_uri: ClassVar[URIRef] = THIS.GeographyInformation

    locationOfOperationSupplyOrProduction: Optional[Union[dict, "LocationInfo"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.locationOfOperationSupplyOrProduction is not None and not isinstance(self.locationOfOperationSupplyOrProduction, LocationInfo):
            self.locationOfOperationSupplyOrProduction = LocationInfo(**as_dict(self.locationOfOperationSupplyOrProduction))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LocationInfo(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["LocationInfo"]
    class_class_curie: ClassVar[str] = "this:LocationInfo"
    class_name: ClassVar[str] = "LocationInfo"
    class_model_uri: ClassVar[URIRef] = THIS.LocationInfo

    descriptionOfRestrictions: Optional[Union[Union[dict, "MultiLangString"], List[Union[dict, "MultiLangString"]]]] = empty_list()
    location: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.descriptionOfRestrictions, list):
            self.descriptionOfRestrictions = [self.descriptionOfRestrictions] if self.descriptionOfRestrictions is not None else []
        self.descriptionOfRestrictions = [v if isinstance(v, MultiLangString) else MultiLangString(**as_dict(v)) for v in self.descriptionOfRestrictions]

        if self.location is not None and not isinstance(self.location, str):
            self.location = str(self.location)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TechnologyInformation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["TechnologyInformation"]
    class_class_curie: ClassVar[str] = "this:TechnologyInformation"
    class_name: ClassVar[str] = "TechnologyInformation"
    class_model_uri: ClassVar[URIRef] = THIS.TechnologyInformation

    technologyDescriptionAndIncludedProcesses: Optional[Union[Union[dict, "MultiLangString"], List[Union[dict, "MultiLangString"]]]] = empty_list()
    technologicalApplicability: Optional[Union[Union[dict, "MultiLangString"], List[Union[dict, "MultiLangString"]]]] = empty_list()
    referenceToTechnologyFlowDiagrammOrPicture: Optional[Union[Union[dict, "TechnologyReference"], List[Union[dict, "TechnologyReference"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.technologyDescriptionAndIncludedProcesses, list):
            self.technologyDescriptionAndIncludedProcesses = [self.technologyDescriptionAndIncludedProcesses] if self.technologyDescriptionAndIncludedProcesses is not None else []
        self.technologyDescriptionAndIncludedProcesses = [v if isinstance(v, MultiLangString) else MultiLangString(**as_dict(v)) for v in self.technologyDescriptionAndIncludedProcesses]

        if not isinstance(self.technologicalApplicability, list):
            self.technologicalApplicability = [self.technologicalApplicability] if self.technologicalApplicability is not None else []
        self.technologicalApplicability = [v if isinstance(v, MultiLangString) else MultiLangString(**as_dict(v)) for v in self.technologicalApplicability]

        if not isinstance(self.referenceToTechnologyFlowDiagrammOrPicture, list):
            self.referenceToTechnologyFlowDiagrammOrPicture = [self.referenceToTechnologyFlowDiagrammOrPicture] if self.referenceToTechnologyFlowDiagrammOrPicture is not None else []
        self.referenceToTechnologyFlowDiagrammOrPicture = [v if isinstance(v, TechnologyReference) else TechnologyReference(**as_dict(v)) for v in self.referenceToTechnologyFlowDiagrammOrPicture]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TechnologyReference(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["TechnologyReference"]
    class_class_curie: ClassVar[str] = "this:TechnologyReference"
    class_name: ClassVar[str] = "TechnologyReference"
    class_model_uri: ClassVar[URIRef] = THIS.TechnologyReference

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
class MultiLangString(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = THIS["MultiLangString"]
    class_class_curie: ClassVar[str] = "this:MultiLangString"
    class_name: ClassVar[str] = "MultiLangString"
    class_model_uri: ClassVar[URIRef] = THIS.MultiLangString

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

slots.dataSetInformation = Slot(uri=THIS.dataSetInformation, name="dataSetInformation", curie=THIS.curie('dataSetInformation'),
                   model_uri=THIS.dataSetInformation, domain=None, range=Optional[Union[dict, DataSetInformation]])

slots.quantitativeReference = Slot(uri=THIS.quantitativeReference, name="quantitativeReference", curie=THIS.curie('quantitativeReference'),
                   model_uri=THIS.quantitativeReference, domain=None, range=Optional[Union[dict, QuantitativeReference]])

slots.time = Slot(uri=THIS.time, name="time", curie=THIS.curie('time'),
                   model_uri=THIS.time, domain=None, range=Optional[Union[dict, TimeInformation]])

slots.geography = Slot(uri=THIS.geography, name="geography", curie=THIS.curie('geography'),
                   model_uri=THIS.geography, domain=None, range=Optional[Union[dict, GeographyInformation]])

slots.technology = Slot(uri=THIS.technology, name="technology", curie=THIS.curie('technology'),
                   model_uri=THIS.technology, domain=None, range=Optional[Union[dict, TechnologyInformation]])

slots.UUID = Slot(uri=THIS.UUID, name="UUID", curie=THIS.curie('UUID'),
                   model_uri=THIS.UUID, domain=None, range=Optional[str])

slots.dataSetName = Slot(uri=THIS.dataSetName, name="dataSetName", curie=THIS.curie('dataSetName'),
                   model_uri=THIS.dataSetName, domain=None, range=Optional[Union[dict, DataSetName]])

slots.classificationInformation = Slot(uri=THIS.classificationInformation, name="classificationInformation", curie=THIS.curie('classificationInformation'),
                   model_uri=THIS.classificationInformation, domain=None, range=Optional[Union[dict, ClassificationInformation]])

slots.baseName = Slot(uri=THIS.baseName, name="baseName", curie=THIS.curie('baseName'),
                   model_uri=THIS.baseName, domain=None, range=Optional[Union[Union[dict, MultiLangString], List[Union[dict, MultiLangString]]]])

slots.classification = Slot(uri=THIS.classification, name="classification", curie=THIS.curie('classification'),
                   model_uri=THIS.classification, domain=None, range=Optional[Union[Union[dict, Classification], List[Union[dict, Classification]]]])

slots.name = Slot(uri=THIS.name, name="name", curie=THIS.curie('name'),
                   model_uri=THIS.name, domain=None, range=Optional[str])

slots.classEntries = Slot(uri=THIS.classEntries, name="classEntries", curie=THIS.curie('classEntries'),
                   model_uri=THIS.classEntries, domain=None, range=Optional[Union[Union[dict, ClassificationEntry], List[Union[dict, ClassificationEntry]]]])

slots.value = Slot(uri=THIS.value, name="value", curie=THIS.curie('value'),
                   model_uri=THIS.value, domain=None, range=Optional[str])

slots.level = Slot(uri=THIS.level, name="level", curie=THIS.curie('level'),
                   model_uri=THIS.level, domain=None, range=Optional[int])

slots.classId = Slot(uri=THIS.classId, name="classId", curie=THIS.curie('classId'),
                   model_uri=THIS.classId, domain=None, range=Optional[str])

slots.referenceToReferenceFlow = Slot(uri=THIS.referenceToReferenceFlow, name="referenceToReferenceFlow", curie=THIS.curie('referenceToReferenceFlow'),
                   model_uri=THIS.referenceToReferenceFlow, domain=None, range=Optional[Union[int, List[int]]])

slots.type = Slot(uri=THIS.type, name="type", curie=THIS.curie('type'),
                   model_uri=THIS.type, domain=None, range=Optional[str])

slots.referenceYear = Slot(uri=THIS.referenceYear, name="referenceYear", curie=THIS.curie('referenceYear'),
                   model_uri=THIS.referenceYear, domain=None, range=Optional[int])

slots.dataSetValidUntil = Slot(uri=THIS.dataSetValidUntil, name="dataSetValidUntil", curie=THIS.curie('dataSetValidUntil'),
                   model_uri=THIS.dataSetValidUntil, domain=None, range=Optional[int])

slots.timeRepresentativenessDescription = Slot(uri=THIS.timeRepresentativenessDescription, name="timeRepresentativenessDescription", curie=THIS.curie('timeRepresentativenessDescription'),
                   model_uri=THIS.timeRepresentativenessDescription, domain=None, range=Optional[Union[Union[dict, MultiLangString], List[Union[dict, MultiLangString]]]])

slots.otherTime = Slot(uri=THIS.otherTime, name="otherTime", curie=THIS.curie('otherTime'),
                   model_uri=THIS.otherTime, domain=None, range=Optional[Union[dict, OtherContent]])

slots.anies = Slot(uri=THIS.anies, name="anies", curie=THIS.curie('anies'),
                   model_uri=THIS.anies, domain=None, range=Optional[Union[Union[dict, AniesEntry], List[Union[dict, AniesEntry]]]])

slots.locationOfOperationSupplyOrProduction = Slot(uri=THIS.locationOfOperationSupplyOrProduction, name="locationOfOperationSupplyOrProduction", curie=THIS.curie('locationOfOperationSupplyOrProduction'),
                   model_uri=THIS.locationOfOperationSupplyOrProduction, domain=None, range=Optional[Union[dict, LocationInfo]])

slots.descriptionOfRestrictions = Slot(uri=THIS.descriptionOfRestrictions, name="descriptionOfRestrictions", curie=THIS.curie('descriptionOfRestrictions'),
                   model_uri=THIS.descriptionOfRestrictions, domain=None, range=Optional[Union[Union[dict, MultiLangString], List[Union[dict, MultiLangString]]]])

slots.location = Slot(uri=THIS.location, name="location", curie=THIS.curie('location'),
                   model_uri=THIS.location, domain=None, range=Optional[str])

slots.technologyDescriptionAndIncludedProcesses = Slot(uri=THIS.technologyDescriptionAndIncludedProcesses, name="technologyDescriptionAndIncludedProcesses", curie=THIS.curie('technologyDescriptionAndIncludedProcesses'),
                   model_uri=THIS.technologyDescriptionAndIncludedProcesses, domain=None, range=Optional[Union[Union[dict, MultiLangString], List[Union[dict, MultiLangString]]]])

slots.technologicalApplicability = Slot(uri=THIS.technologicalApplicability, name="technologicalApplicability", curie=THIS.curie('technologicalApplicability'),
                   model_uri=THIS.technologicalApplicability, domain=None, range=Optional[Union[Union[dict, MultiLangString], List[Union[dict, MultiLangString]]]])

slots.referenceToTechnologyFlowDiagrammOrPicture = Slot(uri=THIS.referenceToTechnologyFlowDiagrammOrPicture, name="referenceToTechnologyFlowDiagrammOrPicture", curie=THIS.curie('referenceToTechnologyFlowDiagrammOrPicture'),
                   model_uri=THIS.referenceToTechnologyFlowDiagrammOrPicture, domain=None, range=Optional[Union[Union[dict, TechnologyReference], List[Union[dict, TechnologyReference]]]])

slots.shortDescription = Slot(uri=THIS.shortDescription, name="shortDescription", curie=THIS.curie('shortDescription'),
                   model_uri=THIS.shortDescription, domain=None, range=Optional[Union[Union[dict, MultiLangString], List[Union[dict, MultiLangString]]]])

slots.refObjectId = Slot(uri=THIS.refObjectId, name="refObjectId", curie=THIS.curie('refObjectId'),
                   model_uri=THIS.refObjectId, domain=None, range=Optional[str])

slots.lang = Slot(uri=THIS.lang, name="lang", curie=THIS.curie('lang'),
                   model_uri=THIS.lang, domain=None, range=Optional[str])