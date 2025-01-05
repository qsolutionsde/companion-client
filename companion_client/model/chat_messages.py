from collections.abc import Sequence
from datetime import datetime
from typing import Literal
from pydantic import BaseModel

from companion_client.model.course_structure import CourseTopic
from companion_client.model.similarity_search import DocumentChunk


class GPTBaseMessage(BaseModel, extra="ignore"):
    type: Literal["system", "ai", "human"]
    timestamp: datetime
    content: str

    req_id: str | None = None
    course: str | None = None
    semester: str | None = None

    additional_kwargs: dict = {}


class GPTSystemMessage(GPTBaseMessage):
    type: Literal["system"] = "system"

def none_to_false(value: bool | None) -> bool:
    return value if value is not None else False

class GPTAIMessage(GPTBaseMessage):
    type: Literal["ai"] = "ai"
    material_ids: Sequence[str] = []
    topic_suggestions_id: Sequence[str] = []
    question_suggestions: Sequence[str] = []
    documents: Sequence[DocumentChunk] = []
    is_info_prompt: bool = False

    def set_topic_suggestions(self, topics: Sequence[CourseTopic]) -> None:
        self.topic_suggestions = topics
        self.topic_suggestions_id = [t.id for t in topics]


class GPTHumanMessage(GPTBaseMessage):
    type: Literal["human"] = "human"

type GPTMessage = GPTHumanMessage | GPTAIMessage
