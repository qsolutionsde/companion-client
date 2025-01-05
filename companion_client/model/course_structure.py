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
    seqno_end: int
    seqno_end_padded: str
    seqnos: list[int]

    seqno_perm: int | None = None
    seqno_perm_end: int | None = None

    title_short_de: int | None = None
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
    description: str
    default_language: str
    icon: str

    proper_course: bool

    # Features for companion
    has_slots: bool
    has_bot: bool
    has_sections: bool
    has_topics: bool
    show_qa: bool
    
    # Bot UI configuration
    bot_intro: str
    show_topic_suggestions: bool
    max_topic_suggestions: int
    topic_suggestions_placement: str

    show_question_suggestions: bool
    max_question_suggestions: int
    question_chips_placement: str

    show_thumbs_voting: bool

    show_similar_materials: bool
    max_sources_display: int

    show_sources: bool
    max_score_sources_display: int

    in_place_nav: bool
    survey_link: str

    # Agent
    functions: list
    use_agent: bool

    # Bot backend configuraion
    max_sources_raw: int
    max_sources_context: int
    max_score_sources_context: int
    max_topic_suggestions_history: int
    max_question_suggestions_history: int
    material_type_weight: int
    history_ttl_minutes: int
    max_history: int
    bot_temperature: int
    reranking_strategy: str
    vectordb: str
    model_question: str
    model_answer: str
    model_topic: str
    model_slot_query: str
    source_template: str
    document_group_intro_template: str
    group_sources: bool
    prompt_for_info: bool
    prompt_for_info_continue: bool
    prompt_info_prompt: str
    prompt_info_model: str
    prompt_info_temperature: int
    prompt_selection_strategy: str
    prompt_selection_prompt: str
    prompt_selection_model: str
    prompt_selection_temperature: int
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