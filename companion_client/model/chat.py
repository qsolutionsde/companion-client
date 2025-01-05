from __future__ import annotations
from collections.abc import Sequence
from datetime import timedelta
from enum import StrEnum
from pydantic import BaseModel
from companion_client.model.chat_messages import GPTBaseMessage
from companion_client.model.course_structure import CourseDescription, CourseTopic
from companion_client.model.group import MaterialGroup
from companion_client.model.material import Material
from companion_client.model.similarity_search import DocumentChunk


class CourseAware(BaseModel, frozen=True):
    course_description: CourseDescription
    semester: str
    course: str


class ThreadAware(BaseModel, frozen=True):
    user_id: str
    thread_id: str

    user_id_generated: bool = False
    thread_id_generated: bool = False

class SessionAware(ThreadAware, frozen=True):
    req_id: str
    req_id_generated: bool = False


class ChatStreamingRequest(CourseAware, SessionAware, frozen=True):
    course_desc: CourseDescription
    message: str
    use_history_summarization: bool = False
    max_history: int = 4
    max_question_suggestion_history: int = 2
    max_question_suggestions: int = 4
    max_topic_suggestion_history: int = 2
    max_topic_suggestions: int = 3
    time_window: timedelta = timedelta(hours=1)
    max_sources_context: int = 10
    max_sources_display: int = 4
    max_slots: int = 4

class StreamingResponseType(StrEnum):
    SOURCES = "sources"
    MATERIALS = "materials"
    START = "start"
    STREAMING = "streaming"
    RESPONSE = "response"
    QUERY_SUGGESTIONS = "query_suggestions"
    TOPIC_SUGGESTIONS = "topic_suggestions"
    END = "end"
    ERROR = "error"

    def response_class(self) -> type[ChatStreamingResponse]:
        match self:
            case self.STREAMING:
                return ChatStreamingChunkResponse
            case self.QUERY_SUGGESTIONS:
                return ChatStreamingQuerySuggestionResponse
            case self.TOPIC_SUGGESTIONS:
                return ChatStreamingTopicSuggestionResponse
            case self.SOURCES:
                return ChatStreamingSourcesResponse
            case _:
                return ChatStreamingResponse


class ChatStreamingResponse(BaseModel, frozen=True):
    """ A response event """

    type: StreamingResponseType

class ChatStreamingResponseEnd(ChatStreamingResponse, frozen=True):
    type: StreamingResponseType = StreamingResponseType.END
    full_answer: bool = True
class ChatStreamingMaterialResponse(ChatStreamingResponse, frozen=True):
    value: Sequence[Material | MaterialGroup]
    type: StreamingResponseType = StreamingResponseType.MATERIALS

class ChatStreamingChunkResponse(ChatStreamingResponse, frozen=True):
    value: str
    type: StreamingResponseType = StreamingResponseType.STREAMING

class ChatStreamingFullResponse(ChatStreamingResponse, frozen=True):
    value: str
    prompt: str
    prompt_messages: Sequence[GPTBaseMessage] = []
    type: StreamingResponseType = StreamingResponseType.RESPONSE

class ChatStreamingSourcesResponse(ChatStreamingResponse, frozen=True):
    value: Sequence[DocumentChunk]
    type: StreamingResponseType = StreamingResponseType.SOURCES

class ChatStreamingTopicSuggestionResponse(ChatStreamingResponse, frozen=True):
    value: Sequence[CourseTopic]
    type: StreamingResponseType = StreamingResponseType.TOPIC_SUGGESTIONS

class ChatStreamingQuerySuggestionResponse(ChatStreamingResponse, frozen=True):
    value: Sequence[str]
    type: StreamingResponseType = StreamingResponseType.QUERY_SUGGESTIONS
