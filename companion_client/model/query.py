from collections.abc import Sequence

from pydantic import BaseModel, NonNegativeInt, PositiveInt
from pydantic_extra_types.pendulum_dt import DateTime as PendulumDateTime
from companion_client.model.base import SafeStr, OptionalCourseType, OptionalSemesterType, OptionalGroupType, OptionalSlotType, OptionalMultiGroupType, OptionalMultiSlotType, OptionalMultiMaterialType
from companion_client.model.schema import MaterialTypeDescription

class QueryBase(BaseModel, frozen=True):
    course: OptionalCourseType = None
    semester: OptionalSemesterType = None
    limit: PositiveInt | None = None
    start_date: PendulumDateTime | None = None
    end_date: PendulumDateTime | None = None


class SimpleMaterialQuery(QueryBase, frozen=True):
    group: OptionalGroupType = None
    seqno: NonNegativeInt | None = None
    topic: SafeStr | None = None
    slot_type: OptionalSlotType = None

    material_type: MaterialTypeDescription | None = None
    textual_query: str | None = None
    aggregate: bool = False


class CompanionQuery(QueryBase, arbitrary_types_allowed=True, frozen=True):
    course: OptionalCourseType = None
    semester: OptionalSemesterType = None

    group: OptionalMultiGroupType = None

    start_date: PendulumDateTime | None = None
    end_date: PendulumDateTime | None = None

    slot_type: OptionalMultiSlotType = None

    topic: SafeStr | Sequence[SafeStr] | None = None

    seqno: NonNegativeInt | Sequence[NonNegativeInt] | None = None

    limit: PositiveInt | None = None

class SlotQuery(CompanionQuery, frozen=True):
    """ Represents a conjunctive query for slots"""
    pass

class MaterialQuery(CompanionQuery, frozen=True):
    """ Represents a conjunctive query for materials"""
    material_type: OptionalMultiMaterialType = None
    textual_query: str | None = None
