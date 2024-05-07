from enum import StrEnum, IntEnum
from typing import Optional

from pydantic import BaseModel, computed_field, Field


# TODO: Add more entities as needed
class AnalyticsReportType(StrEnum):
    """
    Enum for the type of analytics report to generate.

    Attributes
    ----------
    EFFORT : Effort report.
    PIPELINE : Pipeline report.
    """
    EFFORT = "Effort"
    PIPELINE = "Pipeline"


class FindLeadsQueryStatus(IntEnum):
    """
    Enum for the status of a lead.

    Attributes
    ----------
    OPEN : Open status.
    CANCELLED : Cancelled status.
    LOST : Lost status.
    WON : Won status.
    """
    OPEN = 0
    CANCELLED = 12
    LOST = 11
    WON = 10


class FindLeadsQueryFilter(IntEnum):
    """
    Enum for the filter to apply to the leads query.

    ...
    Attributes
    ----------
    MY_LEADS : My leads filter.
    MY_TEAM_LEADS : My team leads filter.
    ALL_LEADS : All leads filter.
    """
    MY_LEADS = 0
    MY_TEAM_LEADS = 1
    ALL_LEADS = 2


class User(BaseModel):
    """
    Represents a user in the Nutshell API.

    ...
    Attributes
    ----------
    stub : bool
        Whether the user info is a stub.
    id : int
        The id of the User object.
    entity_type : str
        The entity type (Users).
    rev : str
        The revision of the User object.
    name : str
        The name of the user.
    first_name : str
        The first name of the user.
    last_name : str
        The last name of the user.
    is_enabled : bool
        Whether the user is enabled.
    is_administrator : bool
        Whether the user is an administrator.
    emails : list[str]
        The emails associated with the user.
    modified_time : str
        The time of last modification of the user.
    created_time : str
        The time the user was created.
    """
    stub: bool = None
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Users")
    rev: str
    name: str
    first_name: str = Field(None, alias="firstName")
    last_name: str = Field(None, alias="lastName")
    is_enabled: bool = Field(..., alias="isEnabled")
    is_administrator: bool = Field(..., alias="isAdministrator")
    emails: list[str]
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class Team(BaseModel):
    """
    Represents a team object from the Nutshell API.

    ...
    Attributes
    ----------
    stub : bool
        Whether the team info is a stub.
    id : int
        The id of the Team object.
    name : str
        The name of the team.
    rev : str
        The revision of the Team object.
    entity_type : str
        The entity type (Teams).
    modified_time : str
        The time of last modification of the team.
    created_time : str
        The time the team was created.
    """
    stub: bool
    id: int
    name: str
    rev: str
    entity_type: str = Field(..., alias="entityType", pattern=r"Teams")
    modified_time: str = Field(..., alias="modifiedTime")
    created_time: str = Field(..., alias="createdTime")


class ActivityType(BaseModel):
    """
    Represents an activity type object from the Nutshell API.

    ...
    Attributes
    ----------
    stub : bool
        Whether the activity type info is a stub.
    id : int
        The id of the ActivityType object.
    rev : str
        The revision of the ActivityType object.
    entity_type : str
        The entity type (Activity_Types).
    name : str
        The name of the activity type.
    """
    stub: bool
    id: int
    rev: str
    entity_type: str = Field(..., alias="entityType", pattern=r"Activity_Types")
    name: str


class TimeSeriesData(BaseModel):
    """
    Represents the time series data for an analytics report response.

    ...
    Attributes
    ----------
    total_effort : list[list[int]]
        The total effort data.
    successful_effort : list[list[int]]
        Only the successful effort data.
    """
    total_effort: list[list[int]]
    successful_effort: list[list[int]]


class SummaryData(BaseModel):
    """
    Represents the summary data for an analytics report response.

    ...
    Attributes
    ----------
    sum : float
        The sum value.
    avg : float
        The average value.
    min : float
        The minimum value.
    max : float
        The maximum value.
    sum_delta : float
        The sum delta value.
    avg_delta : float
        The average delta value.
    min_delta : float
        The minimum delta value.
    max_delta : float
        The maximum delta value.
    """
    sum: float
    avg: float
    min: float
    max: float
    sum_delta: float
    avg_delta: float
    min_delta: float
    max_delta: float


class AnalyticsReport(BaseModel):
    """
    Represents an analytics report response from the Nutshell API.

    ...
    Attributes
    ----------
    series_data : TimeSeriesData
        The time series data.
    summary_data : dict[str, SummaryData]
        The summary data.
    period_description : str
        The human-readable period description.
    delta_period_description : str
        The human-readable delta period description.
    """
    series_data: TimeSeriesData = Field(..., alias="seriesData")
    summary_data: dict[str, SummaryData] = Field(..., alias="summaryData")
    period_description: str = Field(..., alias="periodDescription")
    delta_period_description: str = Field(..., alias="deltaPeriodDescription")


class Stageset(BaseModel):
    """
    Represents a stageset object from the Nutshell API.

    ...
    Attributes
    ----------
    id : int
        The id of the Stageset object.
    entity_type : str
        The entity type (Stagesets).
    name : str
        The name of the stageset.
    default : int
        The default value.
    position : int
        The position value.
    """
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Stagesets")
    name: str
    default: Optional[int] = None
    position: Optional[int] = None


class Milestone(BaseModel):
    """
    Represents a milestone object from the Nutshell API.

    ...
    Attributes
    ----------
    id : int
        The id of the Milestone object.
    entity_type : str
        The entity type (Milestones).
    rev : str
        The revision of the Milestone object.
    name : str
        The name of the milestone.
    position : int
        The position value.
    stageset_id : int
        The stageset id.
    """
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Milestones")
    rev: str
    name: str
    position: Optional[int] = None
    stageset_id: Optional[int] = Field(None, alias="stagesetId")


class Lead(BaseModel):
    """
    Represents a lead object from the Nutshell API.

    ...
    Attributes
    ----------
    stub : bool
        Whether the lead info is a stub.
    id : int
        The id of the Lead object.
    entity_type : str
        The entity type (Leads).
    rev : str
        The revision of the Lead object.
    name : str
        The name of the lead.

    """
    stub: Optional[bool] = None
    id: int
    entity_type: str = Field(..., alias="entityType", pattern=r"Leads")
    rev: str
    name: str
    html_url: Optional[str] = Field(None, alias="htmlUrl")
    tags: Optional[list[str]] = None
    description: str
    created_time: Optional[str] = Field(None, alias="createdTime")
    creator: Optional[User] = None
    milestone: Optional[Milestone] = None
    stageset: Optional[Stageset] = None
    status: int
    confidence: Optional[int] = None
    assignee: Optional[User | Team] = None
    due_time: str = Field(..., alias="dueTime")
    value: Optional[dict[str, float | str]] = 0
    normalized_value: Optional[dict[str, float | str]] = Field(None, alias="normalizedValue")
    products: Optional[list[dict]] = None
    primary_account: Optional[dict] = Field(None, alias="primaryAccount")


class FindLeadsQuery(BaseModel):
    """
    For building a valid query for the findLeads method.

    ...
    Attributes:
        status : FindLeadsQueryStatus
            The status of the leads.
        filter : FindLeadsQueryFilter
            The filter to apply to the leads query.
        milestone_id : int
            The milestone id.
        milestone_ids : list[int]
            The milestone ids.
        stageset_id : int
            The stageset id.
        stageset_ids : list[int]
            The stageset ids.
        due_time : str
            The due time of the leads.
        assignee : list[User | Team]
            The assignee of the leads.
        number : int
            The number of leads.

    Computed Attributes:
        query : dict
            A correctly formed query dictionsary for the findLeads method.
    """
    status: Optional[FindLeadsQueryStatus] = None
    filter: Optional[FindLeadsQueryFilter] = None
    milestone_id: Optional[int] = None
    milestone_ids: Optional[list[int]] = None
    stageset_id: Optional[int] = None
    stageset_ids: Optional[list[int]] = None
    due_time: Optional[str] = None
    assignee: Optional[list[User | Team]] = None
    number: Optional[int] = None

    @computed_field
    @property
    def query(self) -> dict:
        query_dict = {}

        if isinstance(self.status, FindLeadsQueryStatus):
            query_dict["status"] = self.status.value
        if self.filter:
            query_dict["filter"] = self.filter.value
        if self.milestone_id:
            query_dict["milestoneId"] = self.milestone_id
        if self.milestone_ids:
            query_dict["milestoneIds"] = self.milestone_ids
        if self.stageset_id:
            query_dict["stagesetId"] = self.stageset_id
        if self.stageset_ids:
            query_dict["stagesetIds"] = self.stageset_ids
        if self.due_time:
            query_dict["dueTime"] = self.due_time
        if self.assignee:
            query_dict["assignee"] = [
                {"entityType": entity.entity_type, "id": entity.id} for entity in self.assignee
            ]
        if self.number:
            query_dict["number"] = self.number

        return query_dict
