from typing import Any, AsyncGenerator
import pytest
import pytest_asyncio
from httpx import AsyncClient
from companion_client.client import CompanionClient
from companion_client.model.base import SemesterType
from companion_client.model.enum import SlotType
from companion_client.model.group import GroupResult
from companion_client.model.material import Material
from companion_client.model.query import MaterialQuery, SimpleMaterialQuery, SlotQuery
from companion_client.model.schema import MaterialTypeDescription, SlotTypeDescription

from companion_client.model.course_structure import (
    CourseDescription,
    CourseInstance,
    CourseInstanceSlot,
    CourseTopic,
)

DEV = True

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[CompanionClient, Any]:
    yield CompanionClient(base_url="https://dev-companion.hka-cloud.de/v1" if DEV else "https://companion-api.hka-cloud.de/v1")

@pytest.mark.asyncio
async def test_get_material_types(client: CompanionClient):
    result = await client.get_material_types()
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_slot_types(client):
    result = await client.get_slot_types()
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_semesters(client):
    result = await client.get_semesters()
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_latest_semester(client):
    result = await client.get_latest_semester()
    assert result

@pytest.mark.asyncio
async def test_get_current_semester(client):
    result = await client.get_current_semester()
    assert result

@pytest.mark.asyncio
async def test_get_courses(client):
    result = await client.get_courses()
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_course(client):
    result = await client.get_course("MOD")
    assert result

@pytest.mark.asyncio
async def test_get_default_lang(client):
    result = await client.get_default_lang("MOD")
    assert result == 'de'

@pytest.mark.asyncio
async def test_get_course_instance(client):
    result = await client.get_course_instance("MOD", "2024-WS")
    assert isinstance(result, CourseInstance)

@pytest.mark.asyncio
async def test_get_slot(client):
    result = await client.get_slot(1)
    assert isinstance(result, CourseInstanceSlot)

@pytest.mark.asyncio
async def test_get_slots(client):
    query = SlotQuery(course="MOD", semester="2024-WS")
    result = await client.get_slots(query)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_recent_slots(client):
    query = SlotQuery(course="MOD", semester="2024-WS")
    result = await client.get_recent_slots(query)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_upcoming_slots(client):
    query = SlotQuery(course="MOD", semester="2024-WS")
    result = await client.get_upcoming_slots(query)

@pytest.mark.asyncio
async def test_get_topics(client):
    result = await client.get_topics("MOD")
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_materials(client):
    query = MaterialQuery(course="MOD", semester="2024-WS")
    result = await client.get_materials(query)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_material(client):
    result = await client.get_material("cis:455")
    assert isinstance(result, Material)

@pytest.mark.asyncio
async def test_get_material_for_courseslot(client):
    result = await client.get_material_for_courseslot(322)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_grouped_materials_by_topic(client):
    query = SimpleMaterialQuery(course="MOD", semester="2024-WS")
    result = await client.get_grouped_materials_by_topic(query)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_grouped_materials_by_section(client):
    query = SimpleMaterialQuery(course="MOD", semester="2024-WS")
    result = await client.get_grouped_materials_by_section(query)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_grouped_materials_by_slot(client):
    query = SimpleMaterialQuery(course="MOD", semester="2024-WS", slot_type=SlotType.LECTURE)
    result = await client.get_grouped_materials_by_slot(query)
    assert len(result) > 0

@pytest.mark.asyncio
async def test_get_sections(client):
    result = await client.get_sections("MOD", "2024-WS")
    assert len(result) > 0
