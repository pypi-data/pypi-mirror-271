from typing import Optional

from pydantic import BaseModel, Field


class ExpandInput(BaseModel):
    """Input for the expand operation"""

    key: dict | str
    relation: str


class EdgeKeys(BaseModel):
    start: dict | str
    end: dict | str


class EdgeUserset(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None


class EdgeInput(BaseModel):
    """RelationKey model."""

    keys: EdgeKeys
    user_set: EdgeUserset = Field(EdgeUserset(), alias="userset")
    relation: str
