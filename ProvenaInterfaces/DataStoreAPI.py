from __future__ import annotations
from typing import Dict, Any, List, Optional, Tuple, Union, ForwardRef
from pydantic import ConfigDict, BaseModel, Field, HttpUrl, AnyHttpUrl, validator
from datetime import datetime, date
from enum import Enum

HOURS_TO_SECS = 3600


# Interface exports prefer relative imports
# where as pip install prefers module level import
try:
    from ProvenaInterfaces.SharedTypes import Status, StatusResponse
    from ProvenaInterfaces.RegistryModels import ItemDataset, S3Location, CollectionFormat, Roles, IdentifiedResource
except:
    from .SharedTypes import Status, StatusResponse
    from .RegistryModels import ItemDataset, S3Location, CollectionFormat, Roles, IdentifiedResource

Handle = str
ROCrate = Dict[str, Any]

# RONode = ForwardRef('RONode')


class ROConnectionFlat(BaseModel):
    name: str
    value: Union[str, List[str]]
    model_config = ConfigDict(str_min_length=1, extra="forbid")


class ROConnectionIDNonExpanded(BaseModel):
    name: str
    value_id: str
    model_config = ConfigDict(str_min_length=1, extra="forbid")


class ROConnectionExpandedUniqueName(BaseModel):
    name: str
    to: RONode
    model_config = ConfigDict(str_min_length=1, extra="forbid")


class ROConnectionExpandedIdName(BaseModel):
    name: str
    to: RONode
    special_id: str
    model_config = ConfigDict(str_min_length=1, extra="forbid")


ROConnectionType = Union[ROConnectionFlat, ROConnectionIDNonExpanded,
                         ROConnectionExpandedUniqueName, ROConnectionExpandedIdName]


class RONode(BaseModel):
    connections: Dict[str, ROConnectionType]
    type: Union[str, List[str]]
    model_config = ConfigDict(str_min_length=1, extra="forbid")


ROConnectionExpandedUniqueName.update_forward_refs()
ROConnectionExpandedIdName.update_forward_refs()


class ROGraph(BaseModel):
    root_node: RONode
    model_config = ConfigDict(str_min_length=1, extra="forbid")


class Schema(BaseModel):
    json_schema: Dict[Any, Any]


class MintResponse(BaseModel):
    status: Status
    handle: Optional[str] = None
    s3_location: Optional[S3Location] = None
    register_create_activity_session_id: Optional[str] = None


class UpdateMetadataResponse(BaseModel):
    status: Status
    handle: str
    s3_location: S3Location

class Credentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    expiry: datetime


class CredentialsRequest(BaseModel):
    dataset_id: str
    console_session_required: bool


class CredentialResponse(BaseModel):
    status: Status
    credentials: Credentials
    console_session_url: Optional[str] = None


# class LockActionType(str, Enum):
#    LOCK = "LOCK"
#    UNLOCK = "UNLOCK"
#
#
# class LockEvent(BaseModel):
#    # Locked or unlocked
#    action_type: LockActionType
#    # Who did it?
#    actor_email: str
#    # Why did they lock/unlock it
#    reason: str
#    # When did this happen? (unix timestamp)
#    timestamp: int
#
#
# class DatasetLockConfiguration(BaseModel):
#    # is the dataset locked down?
#    locked: bool
#    # what is the history of lock changes
#    history: List[LockEvent]


class RegistryFetchResponse(StatusResponse):
    item: Optional[ItemDataset] = None
    roles: Optional[Roles] = None
    locked: Optional[bool] = None


class ListRegistryResponse(BaseModel):
    status: Status
    num_items: int
    registry_items: List[ItemDataset]
    pagination_key: Optional[Dict[str, Any]] = None


class InputConvertRocrateCollectionFormat(BaseModel):
    rocrate_items: List[Dict[str, Any]]


class CollectionFormatConversion(BaseModel):
    handle: str
    collection_format: CollectionFormat
    s3: S3Location
    created_time: datetime
    updated_time: datetime


class InputConvertCollectionFormatRocrate(BaseModel):
    collection_format_items: List[CollectionFormatConversion]


class PossibleCollectionFormat(BaseModel):
    success: bool
    collection_format: Optional[CollectionFormat] = None
    error_message: Optional[str] = None


class PossibleRocrate(BaseModel):
    success: bool
    rocrate: Optional[ROCrate] = None
    error_message: Optional[str] = None


class ResponseConvertRocrateCollectionFormat(BaseModel):
    collection_format_items: List[PossibleCollectionFormat]


class ResponseConvertCollectionFormatRocrate(BaseModel):
    rocrate_items: List[PossibleRocrate]


class ReleaseApprovalRequest(BaseModel):
    dataset_id: IdentifiedResource
    approver_id: IdentifiedResource
    notes: str

class ReleaseApprovalRequestResponse(BaseModel):
    dataset_id: IdentifiedResource
    approver_id: IdentifiedResource
    details: str


class ActionApprovalRequest(BaseModel):
    dataset_id: IdentifiedResource
    approve: bool
    notes: str

class ActionApprovalRequestResponse(BaseModel):
    dataset_id: IdentifiedResource
    approved: bool
    details: str


class PresignedURLRequest(BaseModel):
    dataset_id: IdentifiedResource
    file_path: str
    expires_in: int = Field(
        HOURS_TO_SECS*3, 
        description="The number of seconds the presigned URL is valid for. Defaults to 3 hours (3600*3).",
        ge=1,
        le=HOURS_TO_SECS*24,
    )

class PresignedURLResponse(BaseModel):
    dataset_id: IdentifiedResource
    file_path: str
    presigned_url: str