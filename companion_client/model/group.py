
from collections.abc import Sequence
from enum import StrEnum
from typing import Literal, Self
from pydantic import BaseModel

from companion_client.model.course_structure import CourseTopic, SlotTypeDescription, Section
from companion_client.model.base import CourseType, GroupType
from companion_client.model.material import Material


class MaterialGroupType(StrEnum):
    SLOT = "slot"
    EXERCISE = "exercise"

class MaterialGroup(BaseModel):
    title: str
    description: str | None = None
    type: MaterialGroupType = MaterialGroupType.SLOT
    topics: Sequence[CourseTopic] | None = None
    section: Section | None = None
    groups: Sequence[GroupType] | None = None
    slot_id: int | None = None
    slot_title: str | None = None
    slot_description: str | None = None
    slot_type: SlotTypeDescription | None = None
    icon: str | None = None
    materials: Sequence[Material] = []
    material_label_by_type: bool = True
    more: bool = False
    more_items: Sequence[Material] = []

    @property
    def qids(self) -> Sequence[str]:
        return [m.qid for m in self.materials] + [m.qid for m in self.more_items]

    @property
    def course(self) -> CourseType | None:
        for m in self.materials:
            if m.course is not None:
                return m.course
        for m in self.more_items:
            if m.course is not None:
                return m.course

        return None

MaterialOrGroup = Material | MaterialGroup
MaterialOrGroupList = Sequence[MaterialOrGroup]

class Displayable(BaseModel, frozen=True):
    id: int | str | None = None
    title: str
    description: str | None = None


class GroupResult(Displayable, frozen=True):
    result: MaterialOrGroupList = []
    children: Sequence[Self] = []
    intro: str | None = None
    topics: Sequence[CourseTopic] | None = None
    place: Literal["online", "hybrid", "in-person"] | None = None

