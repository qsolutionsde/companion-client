from __future__ import annotations
from enum import StrEnum
from typing import Self

class ArtifactType(StrEnum):
    QA = "qa"
    ZULIP = "zulip"
    TOPIC = "topic"
    SLOT = "slot"
    OVERVIEW = "overview"
    NONE = "none"



class SlotType(StrEnum):
    LECTURE = "lecture"
    WORKSHOP = "workshop"
    PRESENTATION = "presentation"
    EXAM = "exam"
    TUTORIAL = "tutorial"

    @classmethod
    def of(cls, s: str | None) -> Self | None:
        return None if s is None or s == "" else cls(s)


class MaterialType(StrEnum):
    ZOOM = "zoom"
    SLIDES = "slides"
    BOARD = "board"
    PORTFOLIOTASKS = "portfolio_tasks"
    RECORDING = "recording"
    TRANSCRIPT = "transcript"
    PLAYLIST = "playlist"
    SUMMARY = "summary"
    INSTRUCTIONS = "instructions"
    DOCUMENTATION = "documentation"
    SELF_ASSESSMENT = "self-assessment"
    EXERCISE = "exercise"
    SOLUTION = "solution"
    EXAMPLE = "example"
    TEMPLATE = "template"
    SHORTVIDEO = "shortvideo"
    EVALUATIONRESULT = "evaluation_result"
    EXTRAVIDEO = "extravideo"
    EXTRABOOK = "extrabook"
    EXTRAARTICLE = "extraarticle"
    EXAMSHEET = "examsheet"
    ILIAS = "ilias"
    TOOL = "tool"
    BLOG = "blog"
    PROJECT = "project"
    LEARNINGVIDEO = "learning_video"
    OFFICIAL = "officialdoc"
    THESIS = "thesis"

    def is_slot_independent(self) -> bool:
        match self:
            case MaterialType.SUMMARY | MaterialType.PLAYLIST | MaterialType.ILIAS | MaterialType.TOOL | MaterialType.ZOOM | MaterialType.PORTFOLIOTASKS | MaterialType.BLOG | MaterialType.LEARNINGVIDEO | MaterialType.OFFICIAL | MaterialType.THESIS:
                return True
            case _:
                return False

    def is_singleton(self) -> bool:
        return self in MaterialType.singletons()

    @classmethod
    def singletons(cls) -> list["MaterialType"]:
        return [MaterialType.ZOOM, MaterialType.EXAMSHEET, MaterialType.ILIAS, MaterialType.BLOG, MaterialType.PORTFOLIOTASKS]

    @classmethod
    def of(cls, s: str | None) -> Self | None:
        return None if s is None or s == "" else cls(s)

    @classmethod
    def ord(cls, m: Self | None) -> int:
        return 0 if m is None else list(MaterialType).index(m) + 1
