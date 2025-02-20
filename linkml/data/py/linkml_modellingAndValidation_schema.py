# Auto generated from linkml_modellingAndValidation_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-02-20T11:54:34
# Schema: ILCDmodellingAndValidation
#
# id: https://example.org/ILCDmodellingAndValidation
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

from . linkml_shared_definitions import MultiLangString, OtherContent, ShortDescripAndType, ShortDescripTypeRefVersion
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
ILCDMAV = CurieNamespace('ILCDmav', 'https://example.org/ILCDmodellingAndValidation/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = ILCDMAV


# Types

# Class references



@dataclass(repr=False)
class ModellingAndValidation(YAMLRoot):
    """
    Top-level container for the modellingAndValidation section.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ModellingAndValidation"]
    class_class_curie: ClassVar[str] = "ILCDmav:ModellingAndValidation"
    class_name: ClassVar[str] = "ModellingAndValidation"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ModellingAndValidation

    LCIMethodAndAllocation: Optional[Union[dict, "LCIMethodAndAllocation"]] = None
    dataSourcesTreatmentAndRepresentativeness: Optional[Union[dict, "DataSourcesTreatmentAndRepresentativeness"]] = None
    validationInfo: Optional[Union[dict, "ValidationInfo"]] = None
    complianceDeclarations: Optional[Union[dict, "ComplianceDeclarations"]] = None
    otherMAV: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.LCIMethodAndAllocation is not None and not isinstance(self.LCIMethodAndAllocation, LCIMethodAndAllocation):
            self.LCIMethodAndAllocation = LCIMethodAndAllocation(**as_dict(self.LCIMethodAndAllocation))

        if self.dataSourcesTreatmentAndRepresentativeness is not None and not isinstance(self.dataSourcesTreatmentAndRepresentativeness, DataSourcesTreatmentAndRepresentativeness):
            self.dataSourcesTreatmentAndRepresentativeness = DataSourcesTreatmentAndRepresentativeness(**as_dict(self.dataSourcesTreatmentAndRepresentativeness))

        if self.validationInfo is not None and not isinstance(self.validationInfo, ValidationInfo):
            self.validationInfo = ValidationInfo(**as_dict(self.validationInfo))

        if self.complianceDeclarations is not None and not isinstance(self.complianceDeclarations, ComplianceDeclarations):
            self.complianceDeclarations = ComplianceDeclarations(**as_dict(self.complianceDeclarations))

        if self.otherMAV is not None and not isinstance(self.otherMAV, OtherContent):
            self.otherMAV = OtherContent(**as_dict(self.otherMAV))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class LCIMethodAndAllocation(YAMLRoot):
    """
    Holds LCI method, allocation info, references, other content.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["LCIMethodAndAllocation"]
    class_class_curie: ClassVar[str] = "ILCDmav:LCIMethodAndAllocation"
    class_name: ClassVar[str] = "LCIMethodAndAllocation"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.LCIMethodAndAllocation

    typeOfDataSet: Optional[str] = None
    referenceToLCAMethodDetails: Optional[Union[Union[dict, ShortDescripTypeRefVersion], List[Union[dict, ShortDescripTypeRefVersion]]]] = empty_list()
    otherMAA: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.typeOfDataSet is not None and not isinstance(self.typeOfDataSet, str):
            self.typeOfDataSet = str(self.typeOfDataSet)

        if not isinstance(self.referenceToLCAMethodDetails, list):
            self.referenceToLCAMethodDetails = [self.referenceToLCAMethodDetails] if self.referenceToLCAMethodDetails is not None else []
        self.referenceToLCAMethodDetails = [v if isinstance(v, ShortDescripTypeRefVersion) else ShortDescripTypeRefVersion(**as_dict(v)) for v in self.referenceToLCAMethodDetails]

        if self.otherMAA is not None and not isinstance(self.otherMAA, OtherContent):
            self.otherMAA = OtherContent(**as_dict(self.otherMAA))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataSourcesTreatmentAndRepresentativeness(YAMLRoot):
    """
    Holds references to data sources, usage advice, and other extras.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["DataSourcesTreatmentAndRepresentativeness"]
    class_class_curie: ClassVar[str] = "ILCDmav:DataSourcesTreatmentAndRepresentativeness"
    class_name: ClassVar[str] = "DataSourcesTreatmentAndRepresentativeness"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.DataSourcesTreatmentAndRepresentativeness

    referenceToDataSource: Optional[Union[Union[dict, ShortDescripTypeRefVersion], List[Union[dict, ShortDescripTypeRefVersion]]]] = empty_list()
    useAdviceForDataSet: Optional[Union[Union[dict, MultiLangString], List[Union[dict, MultiLangString]]]] = empty_list()
    otherDSTAR: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.referenceToDataSource, list):
            self.referenceToDataSource = [self.referenceToDataSource] if self.referenceToDataSource is not None else []
        self.referenceToDataSource = [v if isinstance(v, ShortDescripTypeRefVersion) else ShortDescripTypeRefVersion(**as_dict(v)) for v in self.referenceToDataSource]

        if not isinstance(self.useAdviceForDataSet, list):
            self.useAdviceForDataSet = [self.useAdviceForDataSet] if self.useAdviceForDataSet is not None else []
        self.useAdviceForDataSet = [v if isinstance(v, MultiLangString) else MultiLangString(**as_dict(v)) for v in self.useAdviceForDataSet]

        if self.otherDSTAR is not None and not isinstance(self.otherDSTAR, OtherContent):
            self.otherDSTAR = OtherContent(**as_dict(self.otherDSTAR))

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ValidationInfo(YAMLRoot):
    """
    Represents the validation object containing review info.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ValidationInfo"]
    class_class_curie: ClassVar[str] = "ILCDmav:ValidationInfo"
    class_name: ClassVar[str] = "ValidationInfo"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ValidationInfo

    review: Optional[Union[Union[dict, "ReviewEntry"], List[Union[dict, "ReviewEntry"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.review, list):
            self.review = [self.review] if self.review is not None else []
        self.review = [v if isinstance(v, ReviewEntry) else ReviewEntry(**as_dict(v)) for v in self.review]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ReviewEntry(YAMLRoot):
    """
    A single review entry with name of reviewer, institution, etc.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ReviewEntry"]
    class_class_curie: ClassVar[str] = "ILCDmav:ReviewEntry"
    class_name: ClassVar[str] = "ReviewEntry"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ReviewEntry

    referenceToNameOfReviewerAndInstitution: Optional[Union[Union[dict, ShortDescripAndType], List[Union[dict, ShortDescripAndType]]]] = empty_list()
    type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.referenceToNameOfReviewerAndInstitution, list):
            self.referenceToNameOfReviewerAndInstitution = [self.referenceToNameOfReviewerAndInstitution] if self.referenceToNameOfReviewerAndInstitution is not None else []
        self.referenceToNameOfReviewerAndInstitution = [v if isinstance(v, ShortDescripAndType) else ShortDescripAndType(**as_dict(v)) for v in self.referenceToNameOfReviewerAndInstitution]

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ComplianceDeclarations(YAMLRoot):
    """
    Container for compliance-related declarations.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ComplianceDeclarations"]
    class_class_curie: ClassVar[str] = "ILCDmav:ComplianceDeclarations"
    class_name: ClassVar[str] = "ComplianceDeclarations"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ComplianceDeclarations

    compliance: Optional[Union[Union[dict, "ComplianceEntry"], List[Union[dict, "ComplianceEntry"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.compliance, list):
            self.compliance = [self.compliance] if self.compliance is not None else []
        self.compliance = [v if isinstance(v, ComplianceEntry) else ComplianceEntry(**as_dict(v)) for v in self.compliance]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ComplianceEntry(YAMLRoot):
    """
    Holds a reference to a specific compliance system.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = ILCDMAV["ComplianceEntry"]
    class_class_curie: ClassVar[str] = "ILCDmav:ComplianceEntry"
    class_name: ClassVar[str] = "ComplianceEntry"
    class_model_uri: ClassVar[URIRef] = ILCDMAV.ComplianceEntry

    referenceToComplianceSystem: Optional[Union[dict, ShortDescripTypeRefVersion]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.referenceToComplianceSystem is not None and not isinstance(self.referenceToComplianceSystem, ShortDescripTypeRefVersion):
            self.referenceToComplianceSystem = ShortDescripTypeRefVersion(**as_dict(self.referenceToComplianceSystem))

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.LCIMethodAndAllocation = Slot(uri=ILCDMAV.LCIMethodAndAllocation, name="LCIMethodAndAllocation", curie=ILCDMAV.curie('LCIMethodAndAllocation'),
                   model_uri=ILCDMAV.LCIMethodAndAllocation, domain=None, range=Optional[Union[dict, LCIMethodAndAllocation]])

slots.dataSourcesTreatmentAndRepresentativeness = Slot(uri=ILCDMAV.dataSourcesTreatmentAndRepresentativeness, name="dataSourcesTreatmentAndRepresentativeness", curie=ILCDMAV.curie('dataSourcesTreatmentAndRepresentativeness'),
                   model_uri=ILCDMAV.dataSourcesTreatmentAndRepresentativeness, domain=None, range=Optional[Union[dict, DataSourcesTreatmentAndRepresentativeness]])

slots.validationInfo = Slot(uri=ILCDMAV.validationInfo, name="validationInfo", curie=ILCDMAV.curie('validationInfo'),
                   model_uri=ILCDMAV.validationInfo, domain=None, range=Optional[Union[dict, ValidationInfo]])

slots.complianceDeclarations = Slot(uri=ILCDMAV.complianceDeclarations, name="complianceDeclarations", curie=ILCDMAV.curie('complianceDeclarations'),
                   model_uri=ILCDMAV.complianceDeclarations, domain=None, range=Optional[Union[dict, ComplianceDeclarations]])

slots.otherMAV = Slot(uri=ILCDMAV.otherMAV, name="otherMAV", curie=ILCDMAV.curie('otherMAV'),
                   model_uri=ILCDMAV.otherMAV, domain=None, range=Optional[Union[dict, OtherContent]])

slots.typeOfDataSet = Slot(uri=ILCDMAV.typeOfDataSet, name="typeOfDataSet", curie=ILCDMAV.curie('typeOfDataSet'),
                   model_uri=ILCDMAV.typeOfDataSet, domain=None, range=Optional[str])

slots.referenceToLCAMethodDetails = Slot(uri=ILCDMAV.referenceToLCAMethodDetails, name="referenceToLCAMethodDetails", curie=ILCDMAV.curie('referenceToLCAMethodDetails'),
                   model_uri=ILCDMAV.referenceToLCAMethodDetails, domain=None, range=Optional[Union[Union[dict, ShortDescripTypeRefVersion], List[Union[dict, ShortDescripTypeRefVersion]]]])

slots.otherMAA = Slot(uri=ILCDMAV.otherMAA, name="otherMAA", curie=ILCDMAV.curie('otherMAA'),
                   model_uri=ILCDMAV.otherMAA, domain=None, range=Optional[Union[dict, OtherContent]])

slots.referenceToDataSource = Slot(uri=ILCDMAV.referenceToDataSource, name="referenceToDataSource", curie=ILCDMAV.curie('referenceToDataSource'),
                   model_uri=ILCDMAV.referenceToDataSource, domain=None, range=Optional[Union[Union[dict, ShortDescripTypeRefVersion], List[Union[dict, ShortDescripTypeRefVersion]]]])

slots.useAdviceForDataSet = Slot(uri=ILCDMAV.useAdviceForDataSet, name="useAdviceForDataSet", curie=ILCDMAV.curie('useAdviceForDataSet'),
                   model_uri=ILCDMAV.useAdviceForDataSet, domain=None, range=Optional[Union[Union[dict, MultiLangString], List[Union[dict, MultiLangString]]]])

slots.otherDSTAR = Slot(uri=ILCDMAV.otherDSTAR, name="otherDSTAR", curie=ILCDMAV.curie('otherDSTAR'),
                   model_uri=ILCDMAV.otherDSTAR, domain=None, range=Optional[Union[dict, OtherContent]])

slots.review = Slot(uri=ILCDMAV.review, name="review", curie=ILCDMAV.curie('review'),
                   model_uri=ILCDMAV.review, domain=None, range=Optional[Union[Union[dict, ReviewEntry], List[Union[dict, ReviewEntry]]]])

slots.referenceToNameOfReviewerAndInstitution = Slot(uri=ILCDMAV.referenceToNameOfReviewerAndInstitution, name="referenceToNameOfReviewerAndInstitution", curie=ILCDMAV.curie('referenceToNameOfReviewerAndInstitution'),
                   model_uri=ILCDMAV.referenceToNameOfReviewerAndInstitution, domain=None, range=Optional[Union[Union[dict, ShortDescripAndType], List[Union[dict, ShortDescripAndType]]]])

slots.compliance = Slot(uri=ILCDMAV.compliance, name="compliance", curie=ILCDMAV.curie('compliance'),
                   model_uri=ILCDMAV.compliance, domain=None, range=Optional[Union[Union[dict, ComplianceEntry], List[Union[dict, ComplianceEntry]]]])

slots.referenceToComplianceSystem = Slot(uri=ILCDMAV.referenceToComplianceSystem, name="referenceToComplianceSystem", curie=ILCDMAV.curie('referenceToComplianceSystem'),
                   model_uri=ILCDMAV.referenceToComplianceSystem, domain=None, range=Optional[Union[dict, ShortDescripTypeRefVersion]])