from pydantic import BaseModel

from companion_client.model.enum import MaterialType


class SlotTypeDescription(BaseModel):
    """
    Describes types of course instance slots, such as lecture, or workshop.
    In contrast to the SlotType enum, this contains additional metadata
    from the CMS.
    """

    id: str
    title_short_de: str
    title_short_en: str
    title_long_en: str
    title_long_de: str
    icon: str | None = None

    def title_long(self, lang: str) -> str:
        return self.title_long_de if lang == "de" else self.title_long_en

    def title_short(self, lang: str) -> str:
        return self.title_short_de if lang == "de" else self.title_short_en

    def title(self, lang: str) -> str:
        return self.title_long(lang)


class MaterialTypeDescription(BaseModel):
    """
    Describes material types, such as slides, recordings, boards.
    In contrast to the MaterialType enum, this contains additional metadata
    from the CMS.
    """

    id: int
    material_type: MaterialType
    material_long_de: str
    material_long_en: str
    slot_specific: bool
    icon: str | None = None

    def title_long(self, lang: str) -> str:
        return self.material_long_de if lang == "de" else self.material_long_en

    def title_short(self, _) -> str:
        return self.material_type

    def title(self, lang: str) -> str:
        return self.title_long(lang)


class Question(BaseModel, frozen=True):
    id: int
    question: str | None = None
    answer_text: str | None = None
    course: str
    semester: str | None = None
