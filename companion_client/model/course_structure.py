from typing import Sequence
from pydantic import BaseModel

from companion_client.model.schema import SlotTypeDescription


class CourseTopic(BaseModel):
    id: str
    title_de: str
    title_en: str
    sort_order: int = 999
    description: str | None = None

    def title_long(self, lang: str) -> str:
        return self.title(lang)

    def title_short(self, lang: str) -> str:
        return self.title(lang)

    def title(self, lang: str) -> str:
        return self.title_de if lang == "de" else self.title_en

class Section(BaseModel):
    seqno: int
    seqno_padded: str
    seqno_end: int | None = None
    seqno_end_padded: str | None = None
    seqnos: list[int]

    seqno_perm: int | None = None
    seqno_perm_end: int | None = None

    title_short_de: str | None = None
    title_short_en: str | None = None
    title_long_de: str | None = None
    title_long_en: str | None = None

    description_de: str | None = None
    description_en: str | None = None

    topics: list[CourseTopic] | None = None


type SectionType = Section | int


class CourseInstanceSlot(BaseModel, arbitrary_types_allowed=True):
    id: int
    course: str
    semester: str
    slot_type: SlotTypeDescription
    start: str | None = None
    title: str | None = None
    description: str | None = None
    groups: Sequence[str] | None = None
    seqno: int | None = None
    topics: Sequence[CourseTopic] | None = None
    summary: str | None = None


class CourseDescription(BaseModel):
    course_short: str
    course_long: str
    description: str | None = None
    default_language: str
    icon: str | None = None

    proper_course: bool

    # Features for companion
    has_slots: bool
    has_bot: bool
    has_sections: bool
    has_topics: bool
    show_qa: bool
    
    # Bot UI configuration
    bot_intro: str | None = None
    show_topic_suggestions: bool = True
    max_topic_suggestions: int = 3
    topic_suggestions_placement: str | None = "message"

    show_question_suggestions: bool = True
    max_question_suggestions: int = 3
    question_chips_placement: str  | None = "message"

    show_thumbs_voting: bool = True

    show_similar_materials: bool = True
    max_sources_display: int | None = 5

    show_sources: bool = True
    max_score_sources_display: float | None = None

    in_place_nav: bool = True
    survey_link: str | None = None

    # Agent
    functions: list = []
    use_agent: bool = True

    # Bot backend configuraion
    max_sources_raw: int
    max_sources_context: int
    max_score_sources_context: float
    max_topic_suggestions_history: int
    max_question_suggestions_history: int
    material_type_weight: float
    history_ttl_minutes: int
    max_history: int
    bot_temperature: float | None = None
    reranking_strategy: str | None = None
    vectordb: str | None = None
    model_question: str | None = None
    model_answer: str | None = None
    model_topic: str | None = None
    model_slot_query: str | None = None
    source_template: str | None = None
    document_group_intro_template: str | None = None
    group_sources: bool
    prompt_for_info: bool
    prompt_for_info_continue: bool
    prompt_info_prompt: str | None = None
    prompt_info_model: str | None = None
    prompt_info_temperature: int | None = None
    prompt_selection_strategy: str | None = None
    prompt_selection_prompt: str | None = None
    prompt_selection_model: str | None = None
    prompt_selection_temperature: int | None = None
    condense_history: bool
    check_slot_prompt: bool
    rewrite_query: bool
 

class CourseInstance(BaseModel):
    course: str
    semester: str
    description: str | None = None

    default_lang: str | None = None
    course_default_lang: str | None = None
    override_lang: str | None = None

    default_duration: int
    complete: bool
    intro: str | None = None

    course_description: CourseDescription