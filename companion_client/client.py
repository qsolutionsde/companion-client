import json
from typing import Annotated, Any, Literal, Sequence, TypeVar

from httpx import AsyncClient
from pydantic import BaseModel, PositiveInt, StringConstraints, validate_call
from pendulum import DateTime

from companion_client.model.course_structure import CourseDescription, CourseInstance, CourseInstanceSlot, Section
from companion_client.model.base import CourseType, SemesterType, OptionalMultiMaterialType
from companion_client.model.group import GroupResult
from companion_client.model.material import Material
from companion_client.model.course_structure import CourseTopic, SlotTypeDescription
from companion_client.model.query import MaterialQuery, SimpleMaterialQuery, SlotQuery
from companion_client.model.schema import MaterialTypeDescription

type PARAMS = dict[str, str | int | None]

def date_to_str(date: DateTime | None) -> str | None:
    return date.to_iso8601_string() if date else None

def serialize(value: Any) -> str | None:
    return str(value) if value else None

class CompanionClient:
    def __init__(self, base_url: str, token: str = ""):
        self.client = AsyncClient(base_url=base_url, headers={"Authorization": f"Bearer {token}"})

    # Semesters

    async def _get(self, path: str, params: PARAMS = {}) -> str:
        if params:
            params = { k: v for k,v in params.items() if v is not None }
        return (await self.client.get(path, params=params)).text

    T = TypeVar('T', bound=BaseModel, covariant=True)

    async def _get_model(self, path: str, model: type[T], params: PARAMS = {}) -> T:
        if params:
            params = { k: v for k,v in params.items() if v is not None }
        return model.model_validate_json((await self.client.get(path, params=params)).text)

    async def _get_model_list(self, path: str, model: type[T], params: PARAMS = {}) -> Sequence[T]:
        if params:
            params = { k: v for k,v in params.items() if v is not None }
        r  = (await self.client.get(path, params=params)).json()
        return [model.model_validate_json(x) for x in r]

    async def _search_model_list(self, path: str, model: type[T], params: PARAMS = {}) -> Sequence[T]:
        if params:
            params = { k: v for k,v in params.items() if v is not None }
        r  = (await self.client.request("SEARCH", path, data=params)).json()
        return [model.model_validate_json(x) for x in r]


    @validate_call
    async def get_material_types(self) -> Sequence[MaterialTypeDescription]:
        return await self._get_model_list("/material_types", MaterialTypeDescription)

    @validate_call
    async def get_slot_types(self) -> Sequence[SlotTypeDescription]:
        return await self._get_model_list("/slot_types", SlotTypeDescription)


    @validate_call
    async def get_semesters(self) -> Sequence[SemesterType]:
        return json.loads(await self._get("/semesters"))

    @validate_call
    async def get_latest_semester(self) -> SemesterType:
        return await self._get("/semesters/latest")

    @validate_call
    async def get_current_semester(self) -> SemesterType:
        return await self._get("/semesters/current")


    @validate_call
    async def get_courses(self) -> Sequence[CourseDescription]:
        return await self._get_model_list("/courses", CourseDescription)

    @validate_call
    async def get_course(self, course: CourseType) -> CourseDescription:
        return await self._get_model(f"/courses/{course}", CourseDescription)

    @validate_call
    async def get_default_lang(self, course: CourseType, semester: SemesterType | None = None) -> str:
        if semester is None:
            return await self._get(f"/lang/{course}")
        return await self._get(f"/lang/{course}/{semester}")

    @validate_call
    async def get_course_instance(self, course: str, semester: str) -> CourseInstance:
        return await self._get_model(f"/courses/{course}/{semester}", CourseInstance)


    @validate_call
    async def get_slot(self, slot_id: int) -> CourseInstanceSlot:
        return await self._get_model(f"/slots/{slot_id}", CourseInstanceSlot)

    @validate_call
    async def get_slots(self, q: SlotQuery) -> Sequence[CourseInstanceSlot]:
        return await self._get_slots("",q)

    async def _get_slots(self, suffix: str, q: SlotQuery) -> Sequence[CourseInstanceSlot]:      
        return await self._get_model_list(f"/slots/{q.course}/{q.semester}{suffix}", 
                                          CourseInstanceSlot,
                                           params=q.model_dump())

    @validate_call
    async def get_recent_slots(self, q: SlotQuery) -> Sequence[CourseInstanceSlot]:
        return await self._get_slots("/latest", q)

    @validate_call
    async def get_upcoming_slots(self, q: SlotQuery) -> Sequence[CourseInstanceSlot]:
        return await self._get_slots("/upcoming", q)

    @validate_call
    async def get_topics(self, course: str) -> Sequence[CourseTopic]:
        return await self._get_model_list(f"/topics/{course}", CourseTopic)

    @validate_call
    async def get_materials(self, q: MaterialQuery):
        return await self._get_model_list("/materials", Material, params=q.dict())

    @validate_call
    async def get_material(self, qid: Annotated[str, StringConstraints(pattern="ci[s]?:[0-9]+")] | None = None,
                           mtype: Literal['ci','cis'] | None = None, 
                           m_id: PositiveInt | None = None) -> Material | None:
        if qid:
            mtype, m_id = qid.split(":") # type: ignore
        
        return await self._get_model(f"/material/{mtype}/{m_id}", Material)

    @validate_call
    async def get_material_for_courseslot(self, slot: CourseInstanceSlot | int,
                                             material_type: OptionalMultiMaterialType = None) -> Sequence[Material]:
        slot = slot.id if isinstance(slot, CourseInstanceSlot) else slot
        if material_type is None:
            return await self._get_model_list(path=f"/materials/{slot}", model=Material)
        return await self._get_model_list(path=f"/materials/{slot}/{material_type}", model=Material)

    @validate_call
    async def get_grouped_materials_by_topic(self, q: SimpleMaterialQuery) -> Sequence[GroupResult]:
        return await self._get_model_list(f"/grouped/by-topic/{q.course}/{q.semester}", GroupResult, params=q.model_dump())

    @validate_call
    async def get_grouped_materials_by_section(self, q: SimpleMaterialQuery) -> Sequence[GroupResult]:
        return await self._get_model_list(f"/grouped/by-section/{q.course}/{q.semester}", GroupResult, params=q.model_dump())

    @validate_call
    async def get_grouped_materials_by_slot(self, q: SimpleMaterialQuery) -> Sequence[GroupResult]:
        return await self._get_model_list(f"/grouped/by-slot/{q.course}/{q.semester}", GroupResult, params=q.model_dump())


    @validate_call
    async def get_sections(self, course: CourseType, semester: SemesterType) -> Sequence[Section]:
        return await self._get_model_list(f"/sections/{course}", Section)

    @validate_call
    async def get_section(self, course: str, seqno: int, semester: str | None = None ) -> Section | None:
        return await self._get_model(f"/sections/{course}/{seqno}", Section)
        
    