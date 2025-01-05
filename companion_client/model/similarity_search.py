from pydantic import BaseModel
from companion_client.model.base import CourseType, OptionalSemesterType
from companion_client.model.enum import ArtifactType, MaterialType
from companion_client.model.material import Material


class DocumentChunk(BaseModel):
    id: str | None = None
    qid: str | None = None

    qid_scheme: str | None = None
    local_id: str | None = None

    pos: int | None = None
    pos_end: int | None = None

    course: CourseType
    semester: OptionalSemesterType = None

    title: str | None = None
    content: str = ""
    slot_title: str | None = None
    material_type: MaterialType | ArtifactType = ArtifactType.NONE
    similarity_score: float | None = None
    url: str | None = None
    etag: str | None = None
    material: Material | None = None

