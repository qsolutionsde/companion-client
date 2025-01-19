from typing import Annotated, Literal, Sequence
from pydantic import BaseModel, Field, NonNegativeInt
from pydantic_extra_types.pendulum_dt import DateTime
from companion_client.model.course_structure import CourseTopic
from companion_client.model.schema import MaterialTypeDescription, SlotTypeDescription
from companion_client.model.base import CourseType, SemesterType, OptionalMultiGroupType


class Material(BaseModel, arbitrary_types_allowed=True, validate_assignment=True):
    id: int
    qid: str

    title: str | None = None
    display_title: Annotated[str, Field(validation_alias="display_title_")]
    display_title_compact: Annotated[str, Field(validation_alias="display_title_compact_")]

    description: str | None = None
    display_description: Annotated[str, Field(validation_alias="display_description_")]

    lang: str | None = None

    material_type: MaterialTypeDescription
    topics: Sequence[CourseTopic] = []

    seqno: NonNegativeInt | None
    section_title: str | None
    section_title_compact: str | None

    spoiler_protect: bool = False

    course: CourseType | None
    course_long: str | None
    semester: SemesterType | None
    course_instance_title: str | None = None
    course_instance_description: str | None = None

    slot_type: SlotTypeDescription | None
    slot_id: NonNegativeInt | None = None
    start_date: DateTime | None = None
    end_date: DateTime | None = None

    groups: OptionalMultiGroupType | None

    url: str | None = None
    full_url: str | None = None
    full_direct_url: str | None = None
    full_preview_url: str | None = None
    alt_url_title: str | None = None
    alt_url: str | None = None
    url_pattern: str | None = None

    index_only_url: str | None = None
    index_only_full_url: str | None = None
    no_indexing: bool = False
    reindex_interval: int | None = None
    last_indexed: DateTime | None = None

    indexing_strategy: Literal["standard", "multimodal", "premium"]
    split_method: Literal["page", "h1", "h2"] = "page"

    indexing_context_prefix: str | None = None

    @property
    def key(self) -> str | None:
        if self.url is None or self.url.startswith("http"):
            return None

        return self.get_relative_url()

    def get_relative_url(self, url: str | None = None) -> str:
        url = url if url is not None else self.url
        return f"{self.course}/{url}" if self.semester is None else f"{self.course}/{self.semester}/{url}"
