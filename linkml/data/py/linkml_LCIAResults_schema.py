# Auto generated from linkml_LCIAResults_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-02-20T16:23:36
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

from . linkml_shared_definitions import OtherContent, ShortDescripTypeRefVersionUri
from linkml_runtime.linkml_model.types import Float

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

    LCIAResult: Optional[Union[Union[dict, "LCIAResultEntry"], List[Union[dict, "LCIAResultEntry"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.LCIAResult, list):
            self.LCIAResult = [self.LCIAResult] if self.LCIAResult is not None else []
        self.LCIAResult = [v if isinstance(v, LCIAResultEntry) else LCIAResultEntry(**as_dict(v)) for v in self.LCIAResult]

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

    referenceToLCIAMethodDataSet: Optional[Union[dict, ShortDescripTypeRefVersionUri]] = None
    meanAmount: Optional[float] = None
    otherLCIA: Optional[Union[dict, OtherContent]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.referenceToLCIAMethodDataSet is not None and not isinstance(self.referenceToLCIAMethodDataSet, ShortDescripTypeRefVersionUri):
            self.referenceToLCIAMethodDataSet = ShortDescripTypeRefVersionUri(**as_dict(self.referenceToLCIAMethodDataSet))

        if self.meanAmount is not None and not isinstance(self.meanAmount, float):
            self.meanAmount = float(self.meanAmount)

        if self.otherLCIA is not None and not isinstance(self.otherLCIA, OtherContent):
            self.otherLCIA = OtherContent(**as_dict(self.otherLCIA))

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.LCIAResult = Slot(uri=ILCDLCIA.LCIAResult, name="LCIAResult", curie=ILCDLCIA.curie('LCIAResult'),
                   model_uri=ILCDLCIA.LCIAResult, domain=None, range=Optional[Union[Union[dict, LCIAResultEntry], List[Union[dict, LCIAResultEntry]]]])

slots.referenceToLCIAMethodDataSet = Slot(uri=ILCDLCIA.referenceToLCIAMethodDataSet, name="referenceToLCIAMethodDataSet", curie=ILCDLCIA.curie('referenceToLCIAMethodDataSet'),
                   model_uri=ILCDLCIA.referenceToLCIAMethodDataSet, domain=None, range=Optional[Union[dict, ShortDescripTypeRefVersionUri]])

slots.meanAmount = Slot(uri=ILCDLCIA.meanAmount, name="meanAmount", curie=ILCDLCIA.curie('meanAmount'),
                   model_uri=ILCDLCIA.meanAmount, domain=None, range=Optional[float])

slots.otherLCIA = Slot(uri=ILCDLCIA.otherLCIA, name="otherLCIA", curie=ILCDLCIA.curie('otherLCIA'),
                   model_uri=ILCDLCIA.otherLCIA, domain=None, range=Optional[Union[dict, OtherContent]])