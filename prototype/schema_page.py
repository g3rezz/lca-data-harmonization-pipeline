import streamlit as st
import streamlit.components.v1 as components
from streamlit_theme import st_theme
import textwrap

# Retrieve active theme, fallback to light if None.
theme = st_theme() or {"base": "light"}
base_theme = theme.get("base", "light").lower()

# Set dynamic colors
bg_color = "#0E1117" if base_theme == "dark" else "#ffffff"
font_color = "white" if base_theme == "dark" else "black"


legend_html = """
<html>
  <head>
    <style>
      html, body {
          margin: 0;
          padding: 0;
      }
      .mermaid {
          width: 100%;
      }
    </style>
  </head>
  <body>
    <div class="mermaid">
    erDiagram
        K }|--o{ L : R1
        M |o--|| N : R2
    </div>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs';
      mermaid.initialize({ startOnLoad: true });
    </script>
  </body>
</html>
"""

with st.sidebar:
    st.markdown("### ER Diagram Legend")
    components.html(legend_html, height=300)


MERMAID_ER_DIAGRAM = textwrap.dedent(
    """
    erDiagram
    ProcessDataSet {
        string id
        string version        
    }
    ReferenceBase {
        string type
        UUIDType refObjectId  
        string version        
        string refObjectUri   
        string id
    }
    ShortDescripAndType {     
        string type
        UUIDType refObjectId  
        string version        
        string refObjectUri   
        string id
    }
    ShortDescripTypeRef {
        string type
        UUIDType refObjectId
        string version
        string refObjectUri
        string id
    }
    ShortDescripTypeRefVersion {
        string type
        UUIDType refObjectId
        string version
        string refObjectUri
        string id
    }
    ShortDescripTypeRefVersionUri {
        string type
        UUIDType refObjectId
        string version
        string refObjectUri
        string id
    }
    OtherContent {

    }
    AniesBase {
        string name
        string value
        UnixTimestamp timestampValue
        string module
        string id
    }
    AniesNameValue {
        string name
        string value
        UnixTimestamp timestampValue
        string module
        string id
    }
    AniesNameValueModule {
        string name
        string value
        UnixTimestamp timestampValue
        string module
        string id
    }
    AniesNameTimestamp {
        string name
        string value
        UnixTimestamp timestampValue
        string module
        string id
    }
    AniesNameObjectValue {
        string name
        string value
        UnixTimestamp timestampValue
        string module
        string id
    }
    AniesNameValueObjectValueModule {
        string name
        string value
        UnixTimestamp timestampValue
        string module
        string id
    }
    AniesNameTypedReference {
        string name
        string value
        UnixTimestamp timestampValue
        string module
        string id
    }
    AniesWithScenario {
        string name
        string value
        UnixTimestamp timestampValue
        string module
        string id
    }
    Scenario {
        string id
        string name
        boolean default
    }
    MultiLangString {
        string value
        string lang
        string id
    }
    ProcessInformation {
        string id
    }
    DataSetInformation {
        string id
        UUIDType UUID
    }
    DataSetName {
        string id
    }
    ClassificationInformation {
        string id
    }
    Classification {
        string id
        string name
    }
    ClassificationEntry {
        string id
        string value
        integer level
        string classId
    }
    DSIOtherContent {
        string id
    }
    QuantitativeReference {
        string id
        integerList referenceToReferenceFlow
        string type
    }
    TimeInformation {
        string id
        Year referenceYear
        Year dataSetValidUntil
    }
    GeographyInformation {
        string id
    }
    LocationInfo {
        string id
        string location
    }
    TechnologyInformation {
        string id
    }
    TimeOtherContent {
        string id
    }
    ModellingAndValidation {
        string id
    }
    LCIMethodAndAllocationEntry {
        string id
        string typeOfDataSet
    }
    DataSourcesTreatmentAndRepresentativeness {
        string id
    }
    ValidationInfo {
        string id
    }
    ReviewEntry {
        string id
        string type
    }
    ComplianceDeclarations {
        string id
    }
    ComplianceEntry {
        string id
    }
    MAVOtherContent {
        string id
    }
    DSTAROtherRoot {
        string id
    }
    DSTAREntry {
        string id
        string name
    }
    DSTARReference {
        string id
        string type
        UUIDType refObjectId
        string versionAsString
        ResourceURLList resourceURLs
    }
    ExtendedMultiLangString {
        string id
        string value
        string defaultValue
    }
    VersionDict {
        string id
        integer versionInt
        integer majorVersion
        integer minorVersion
        integer subMinorVersion
        boolean zero
        string versionString
    }
    UUIDDict {
        string id
        UUIDType uuidValue
    }
    MAAOtherContent {
        string id
    }
    AdministrativeInformation {
        string id
    }
    CommissionerAndGoal {
        string id
    }
    DataGenerator {
        string id
    }
    DataEntryBy {
        string id
        UnixTimestamp timeStamp
    }
    PublicationAndOwnership {
        string id
        string dataSetVersion
        UnixTimestamp dateOfLastRevision
        string registrationNumber
        boolean copyright
        string licenseType
    }
    AdministrativeOtherContent {
        string id
    }
    Exchanges {
        string id
    }
    ExchangeEntry {
        string id
        integer dataSetInternalID
        float meanAmount
        boolean referenceFlow
        float resultingflowAmount
        string resolvedFlowVersion
        string typeOfFlow
        string exchangeDirection
    }
    ExchangeOtherContent {
        string id
    }
    FlowPropertyEntry {
        string id
        UUIDType uuidFP
        boolean referenceFlowProperty
        float meanValue
        string referenceUnit
        UUIDType unitGroupUUID
    }
    ExchangeClassification {
        string id
        string classHierarchy
        string nameClass
    }
    MaterialPropEntry {
        string id
        string name
        string value
        string unit
        string unitDescription
    }
    LCIAResults {
        string id
    }
    LCIAResultEntry {
        string id
        float meanAmount
    }
    ReferenceToLCIAMethodDataSetEntry {
        string id
        string type
        UUIDType refObjectId
        string version
        string refObjectUri
    }
    LCIAOtherContent {
        string id
    }

    ProcessDataSet ||--|o ProcessInformation : "processInformation"
    ProcessDataSet ||--|o ModellingAndValidation : "modellingAndValidation"
    ProcessDataSet ||--|o AdministrativeInformation : "administrativeInformation"
    ProcessDataSet ||--|o Exchanges : "exchanges"
    ProcessDataSet ||--|o LCIAResults : "lciaResults"
    ReferenceBase ||--}o MultiLangString : "shortDescription"
    ShortDescripAndType ||--}o MultiLangString : "shortDescription"
    ShortDescripTypeRef ||--}o MultiLangString : "shortDescription"
    ShortDescripTypeRefVersion ||--}o MultiLangString : "shortDescription"
    ShortDescripTypeRefVersionUri ||--}o MultiLangString : "shortDescription"
    OtherContent ||--}o AniesBase : "anies"
    AniesBase ||--|o ShortDescripTypeRefVersion : "objectValue"
    AniesBase ||--}o Scenario : "scenario"
    AniesNameValue ||--|o ShortDescripTypeRefVersion : "objectValue"
    AniesNameValue ||--}o Scenario : "scenario"
    AniesNameValueModule ||--|o ShortDescripTypeRefVersion : "objectValue"
    AniesNameValueModule ||--}o Scenario : "scenario"
    AniesNameTimestamp ||--|o ShortDescripTypeRefVersion : "objectValue"
    AniesNameTimestamp ||--}o Scenario : "scenario"
    AniesNameObjectValue ||--|o ShortDescripTypeRefVersion : "objectValue"
    AniesNameObjectValue ||--}o Scenario : "scenario"
    AniesNameValueObjectValueModule ||--|o ShortDescripTypeRefVersion : "objectValue"
    AniesNameValueObjectValueModule ||--}o Scenario : "scenario"
    AniesNameTypedReference ||--|o ShortDescripTypeRefVersion : "objectValue"
    AniesNameTypedReference ||--}o Scenario : "scenario"
    AniesWithScenario ||--|o ShortDescripTypeRefVersion : "objectValue"
    AniesWithScenario ||--}o Scenario : "scenario"
    Scenario ||--}o MultiLangString : "description"
    ProcessInformation ||--|| DataSetInformation : "dataSetInformation"
    ProcessInformation ||--|o QuantitativeReference : "quantitativeReference"
    ProcessInformation ||--|o TimeInformation : "timeInformation"
    ProcessInformation ||--|o GeographyInformation : "geography"
    ProcessInformation ||--|o TechnologyInformation : "technology"
    DataSetInformation ||--|o DataSetName : "dataSetName"
    DataSetInformation ||--}o MultiLangString : "synonyms"
    DataSetInformation ||--|o ClassificationInformation : "classificationInformation"
    DataSetInformation ||--}o MultiLangString : "generalComment"
    DataSetInformation ||--|o DSIOtherContent : "otherDSI"
    DataSetName ||--}| MultiLangString : "baseName"
    DataSetName ||--}o MultiLangString : "functionalUnitFlowProperties"
    ClassificationInformation ||--}o Classification : "classification"
    Classification ||--}o ClassificationEntry : "classEntries"
    DSIOtherContent ||--}o AniesWithScenario : "anies"
    TimeInformation ||--}o MultiLangString : "timeRepresentativenessDescription"
    TimeInformation ||--|o TimeOtherContent : "otherTime"
    GeographyInformation ||--|o LocationInfo : "locationOfOperationSupplyOrProduction"
    LocationInfo ||--}o MultiLangString : "descriptionOfRestrictions"
    TechnologyInformation ||--}o MultiLangString : "technologyDescriptionAndIncludedProcesses"
    TechnologyInformation ||--}o MultiLangString : "technologicalApplicability"
    TechnologyInformation ||--}o ShortDescripTypeRefVersionUri : "referenceToTechnologyFlowDiagrammOrPicture"
    TechnologyInformation ||--}o ShortDescripTypeRefVersionUri : "referenceToTechnologyPictogramme"
    TimeOtherContent ||--}o AniesNameTimestamp : "anies"
    ModellingAndValidation ||--|o LCIMethodAndAllocationEntry : "LCIMethodAndAllocation"
    ModellingAndValidation ||--|o DataSourcesTreatmentAndRepresentativeness : "dataSourcesTreatmentAndRepresentativeness"
    ModellingAndValidation ||--|o ValidationInfo : "validationInfo"
    ModellingAndValidation ||--|o ComplianceDeclarations : "complianceDeclarations"
    ModellingAndValidation ||--|o MAVOtherContent : "otherMAV"
    LCIMethodAndAllocationEntry ||--}o ShortDescripTypeRefVersion : "referenceToLCAMethodDetails"
    LCIMethodAndAllocationEntry ||--|o MAAOtherContent : "otherMAA"
    DataSourcesTreatmentAndRepresentativeness ||--}o ShortDescripTypeRefVersion : "referenceToDataSource"
    DataSourcesTreatmentAndRepresentativeness ||--}o MultiLangString : "useAdviceForDataSet"
    DataSourcesTreatmentAndRepresentativeness ||--|o DSTAROtherRoot : "otherDSTAR"
    ValidationInfo ||--}o ReviewEntry : "review"
    ReviewEntry ||--}o ShortDescripAndType : "referenceToNameOfReviewerAndInstitution"
    ComplianceDeclarations ||--}o ComplianceEntry : "compliance"
    ComplianceEntry ||--}o ShortDescripTypeRefVersion : "referenceToComplianceSystem"
    MAVOtherContent ||--}o AniesNameTypedReference : "anies"
    DSTAROtherRoot ||--}o DSTAREntry : "aniesDSTAR"
    DSTAREntry ||--|o DSTARReference : "valueDSTAR"
    DSTARReference ||--|o ExtendedMultiLangString : "shortDescriptionExtended"
    DSTARReference ||--|o VersionDict : "versionDict"
    DSTARReference ||--|o UUIDDict : "uuidDict"
    ExtendedMultiLangString ||--}o MultiLangString : "lstrings"
    MAAOtherContent ||--}o AniesNameValue : "anies"
    AdministrativeInformation ||--|o CommissionerAndGoal : "commissionerAndGoal"
    AdministrativeInformation ||--|o DataGenerator : "dataGenerator"
    AdministrativeInformation ||--|o DataEntryBy : "dataEntryBy"
    AdministrativeInformation ||--|o PublicationAndOwnership : "publicationAndOwnership"
    CommissionerAndGoal ||--}o ShortDescripTypeRefVersion : "referenceToCommissioner"
    DataGenerator ||--}o ShortDescripTypeRefVersion : "referenceToPersonOrEntityGeneratingTheDataSet"
    DataEntryBy ||--}o ShortDescripTypeRefVersionUri : "referenceToDataSetFormat"
    DataEntryBy ||--}o ShortDescripTypeRefVersionUri : "referenceToPersonOrEntityEnteringTheData"
    PublicationAndOwnership ||--|o ShortDescripTypeRefVersion : "referenceToRegistrationAuthority"
    PublicationAndOwnership ||--|o ShortDescripTypeRefVersion : "referenceToOwnershipOfDataSet"
    PublicationAndOwnership ||--}o MultiLangString : "accessRestrictions"
    PublicationAndOwnership ||--|o AdministrativeOtherContent : "otherPAO"
    AdministrativeOtherContent ||--}o AniesNameTypedReference : "anies"
    Exchanges ||--}o ExchangeEntry : "exchange"
    ExchangeEntry ||--|o ShortDescripTypeRefVersion : "referenceToFlowDataSet"
    ExchangeEntry ||--}o FlowPropertyEntry : "flowProperties"
    ExchangeEntry ||--}o MaterialPropEntry : "materialProperties"
    ExchangeEntry ||--|o ExchangeOtherContent : "otherEx"
    ExchangeEntry ||--|o ExchangeClassification : "classificationEx"
    ExchangeOtherContent ||--}o AniesNameValueObjectValueModule : "anies"
    FlowPropertyEntry ||--}o MultiLangString : "nameFP"
    LCIAResults ||--}o LCIAResultEntry : "LCIAResult"
    LCIAResultEntry ||--|o ReferenceToLCIAMethodDataSetEntry : "referenceToLCIAMethodDataSet"
    LCIAResultEntry ||--|o LCIAOtherContent : "otherLCIA"
    ReferenceToLCIAMethodDataSetEntry ||--}o MultiLangString : "shortDescription"
    LCIAOtherContent ||--}o AniesNameValueObjectValueModule : "anies"
    """
)


def render_mermaid_chart(height: int = 600) -> None:
    html_code = f"""
    <html>
      <head>
        <style>
          html, body {{
            margin: 0;
            padding: 0;
            background-color: {bg_color};
          }}
          #mermaid-container {{
            width: 100%;
            height: {height}px;
            overflow: auto;
          }}
          .mermaid {{
            width: 100%;
            visibility: hidden;
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
          }}
        </style>
      </head>
      <body>
        <div id="mermaid-container">
          <div id="mermaid-diagram" class="mermaid">
            {MERMAID_ER_DIAGRAM}
          </div>
        </div>
        <!-- Include Mermaid JS library -->
        <script type="module">
          import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11.4.1/dist/mermaid.esm.min.mjs';
          mermaid.initialize({{ startOnLoad: true }});
        </script>
        <!-- Include Panzoom for interactivity -->
        <script src="https://cdn.jsdelivr.net/npm/panzoom@9.4.0/dist/panzoom.min.js"></script>
        <script>
          // Wait for Mermaid to finish rendering, then reveal the diagram.
          window.addEventListener("load", function() {{
            const diagram = document.getElementById("mermaid-diagram");
            if(diagram) {{
                diagram.style.visibility = "visible";
                diagram.style.opacity = "1";
            }}
          }});
          // Initialize panzoom
          const elem = document.getElementById("mermaid-container");
          if (elem) {{
              panzoom(elem, {{
                  maxZoom: 10,
                  minZoom: 1,
                  smoothScroll: false
              }});
          }}
        </script>
      </body>
    </html>
    """
    components.html(html_code, height=height + 50)


render_mermaid_chart(height=750)
