"""
Data models for the datasets endpoint
"""
import enum
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, HttpUrl, validator
from pydantic.utils import is_valid_identifier

# pylint: disable=too-few-public-methods


class ColumnDataType(str, enum.Enum):
    """
    The datatype provided by the api
    """

    CALENDAR_DATE = "Calendar date"
    CHECKBOX = "Checkbox"
    DATE = "Date"
    MULTILINE = "MultiLine"
    MULTIPOINT = "MultiPoint"
    MULTIPOLYGON = "MultiPolygon"
    NUMBER = "Number"
    POINT = "Point"
    POLYGON = "Polygon"
    TEXT = "Text"
    URL = "URL"

    @property
    def type_annotation(self) -> str:
        """
        Return the data type as a python type annotation
        """
        if self == ColumnDataType.DATE:
            return "datetime"
        if self == ColumnDataType.NUMBER:
            return "float"
        if self == ColumnDataType.CHECKBOX:
            return "bool"
        return "str"


class PageViews(BaseModel):
    """
    Page views data model
    """

    page_views_last_week: int
    page_views_last_month: int
    page_views_total: int
    page_views_last_week_log: float
    page_views_last_month_log: float
    page_views_total_log: float


class ColumnFormat(BaseModel):
    """
    Description of column formatting
    """

    align: Optional[str]
    noCommas: Optional[bool]
    precisionStyle: Optional[str]
    view: Optional[str]


class Column(BaseModel):
    """
    A column specification for the data
    """

    name: str
    datatype: ColumnDataType
    description: str
    format: ColumnFormat

    def cleaned_name(self) -> str:
        return _clean_for_python(self.name)

    def needs_cleaning(self) -> bool:
        return self.name != self.cleaned_name()


def _clean_for_python(name: str) -> str:
    reserved_words = {
        "False",
        "def",
        "if",
        "raise",
        "None",
        "del",
        "import",
        "return",
        "True",
        "elif",
        "in",
        "try",
        "and",
        "else",
        "is",
        "while",
        "as",
        "except",
        "lambda",
        "with",
        "assert",
        "finally",
        "nonlocal",
        "yield",
        "break",
        "for",
        "not",
        "class",
        "form",
        "or",
        "continue",
        "global",
        "pass",
        "str",
        "bool",
        "int",
        "register",
    }
    max_len = 50
    cleaned = "".join([c for c in name if c.isalnum()])[:max_len]
    if is_valid_identifier(cleaned) and cleaned not in reserved_words:
        return cleaned
    cleaned = f"_{cleaned}"
    if is_valid_identifier(cleaned) and cleaned not in reserved_words:
        return cleaned
    raise ValueError(f"Could not clean {name}\n{cleaned}")


class Resource(BaseModel):
    """
    Generic resource from api
    """

    name: str
    id: str
    parent_fxf: List
    description: str
    attribution: Optional[str]
    attribution_link: Optional[HttpUrl]
    contact_email: Optional[str]
    type: str
    updatedAt: datetime
    createdAt: datetime
    metadata_updated_at: datetime
    data_updated_at: Optional[datetime]
    page_views: PageViews
    columns_name: List[str]
    columns_field_name: List[str]
    columns_datatype: List[ColumnDataType]
    columns_description: List[str]
    columns_format: List[ColumnFormat]
    download_count: int
    provenance: str
    lens_view_type: str
    lens_display_type: str
    blob_mime_type: Optional[Any]
    hide_from_data_json: bool
    publication_date: datetime

    @property
    def columns(self) -> List[Column]:
        """
        The available columns for this resource
        """
        return [
            Column(name=name, description=description, format=format, datatype=datatype)
            for name, description, format, datatype in zip(
                self.columns_field_name,
                self.columns_description,
                self.columns_format,
                self.columns_datatype,
            )
        ]

    @validator("name")
    @classmethod
    def _can_be_cleaned(cls, value):
        _clean_for_python(value)
        return value

    @property
    def _class_name(self) -> str:
        return _clean_for_python(self.name)


class KeyValue(BaseModel):
    """Simple key value pair"""

    key: str
    value: str


class Classification(BaseModel):
    """
    Classification of a dataset
    """

    categories: List[str]
    tags: List[str]
    domain_category: Optional[str]
    domain_tags: List[str]
    domain_metadata: List[KeyValue]


class Metadata(BaseModel):
    """
    Dataset metadata info
    """

    domain: str


class User(BaseModel):
    """
    Dataset user
    """

    id: str
    user_type: str
    display_name: str


class Dataset(BaseModel):
    """
    A dataset available from the nyc open data api
    """

    resource: Resource
    classification: Classification
    metadata: Metadata
    permalink: HttpUrl
    link: HttpUrl
    owner: User
    creator: User

    def _as_code(self) -> str:
        return self.__repr_str__(" ")
