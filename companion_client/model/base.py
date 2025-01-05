from collections.abc import Sequence
from typing import Annotated, TypeVar

from pydantic import AfterValidator, BeforeValidator, Field, StringConstraints
from pydantic_core import Url

from companion_client.model.enum import MaterialType, SlotType

SAFE_CHARACTERS = r"^[A-Za-z0-9\u0080-\uFFFF._~()!*:/@,;+?-]*$"
LANG_UNDEF = "__"

T = TypeVar("T")

def empty_to_false(v: T | None) -> T | None | bool:
    if v is None:
        return False
    if v == "":
        return False
    return v

def empty_to_undef(v: str) -> str:
    if v is None:
        return LANG_UNDEF
    if v == "":
        return LANG_UNDEF
    if v.lower() == "none":
        return LANG_UNDEF
    return v

def empty_to_none(v: str) -> str | None:
    if v is None:
        return None
    if v == "":
        return None
    if v.lower() == "none":
        return None
    if v.lower() == "undefined":
        return None
    return v

def empty_or_boolean_to_none(v: str) -> str | None:
    r = empty_to_none(v)
    if r is None:
        return None
    if v.lower() in {"true", "false"}:
        return None
    if v.lower() in {"0", "1"}:
        return None
    return v


def canonicalize_semester(semester: str | None) -> str | None:
    if semester is None:
        return None

    semester = semester.upper()
    semester = semester.replace("/", "").replace(" ", "")
    if semester.startswith("SS"):
        if len(semester) == 4:  # noqa: PLR2004
            return f"20{semester[-2:]}-{semester[:2]}"
        if len(semester) >= 6:  # noqa: PLR2004
            return f"{semester[-4:]}-{semester[:2]}"
    elif semester.startswith("WS"):
        if len(semester) == 4:  # noqa: PLR2004
            return f"20{semester[-2:]}-{semester[:2]}"
        if len(semester) == 6:  # noqa: PLR2004
            if semester[-3] == "2":
                return f"20{semester[-4:-2]}-{semester[:2]}"
            return f"{semester[-4:]}-{semester[:2]}"
        if len(semester) == 8:  # noqa: PLR2004
            return f"{semester[-6:-2]}-{semester[:2]}"

    return semester

MarkdownStr = str

SafeStr = Annotated[str,
                    StringConstraints(pattern=SAFE_CHARACTERS)]
CourseType = Annotated[str,
                       StringConstraints(pattern=r"[A-Za-z]", to_upper=True),
                       Field(title="Course in its short form", examples=["MOD", "UCD", "ESM", "SCKM"])]
OptionalCourseType = Annotated[CourseType | None,
                       BeforeValidator(empty_to_none),
                       Field(title="Course in its short form", examples=["MOD", "UCD", "ESM", "SCKM"])]

SemesterType = Annotated[str,
                         StringConstraints(pattern=r"20[0-9][0-9]-[s,w,S,W][s,S]"),
                         Field(title="Semester",
                         description="Semester in the format of 'YYYY-SS' or 'YYYY-WS', where 'SS' stands for summer semester and 'WS' for winter semester.",
                         examples=["2023-WS", "2024-WS", "2024-SS"])]
OptionalSemesterType = Annotated[SemesterType | None,
                         BeforeValidator(empty_to_none),
                         Field(title="Semester", examples=["2023-WS", "2023-SS"])]


LangType = Annotated[str,
                     BeforeValidator(empty_to_undef),
                     StringConstraints(pattern=r"^[a-z_][a-z_]$"),
                     Field(title="Language (two-letter code)", examples=["de", "en"])]

OptionalLangType = Annotated[LangType | None, BeforeValidator(empty_to_none),
                             Field(title="Language (two-letter code)", examples=["de", "en"])]

GroupType = Annotated[str,
                      StringConstraints(pattern=r"[a-z,0-9]"),
                      Field(title="Group name", examples=["a", "b"])]

OptionalGroupType = Annotated[GroupType | None,
                              BeforeValidator(empty_to_none),
                              Field(title="Formal course group", examples=["a", "b", "c", "d"])]

URLStr = Annotated[str,
                   AfterValidator(lambda s: str(Url(s)).rstrip("/"))
                   ]

type SingleOrSequence[T] = T | Sequence[T]
type OptionalSingleOrSequence[T] = T | Sequence[T] | None


MultiGroupType = Annotated[SingleOrSequence[GroupType],
                           Field(title="Group name or list of formal group names", examples=["a", ["b", "c"]])]

OptionalMultiGroupType = Annotated[OptionalSingleOrSequence[GroupType],
                           Field(title="Group name or list of formal group names", examples=["a", ["b", "c"]])]

OptionalSlotType = Annotated[SlotType | None,
                             BeforeValidator(empty_to_none),
                             Field(title="Slot type", examples=["lecture", "tutorial"])]
MultiSlotType = SingleOrSequence[SlotType]
OptionalMultiSlotType = OptionalSingleOrSequence[SlotType]
MultiMaterialType = SingleOrSequence[MaterialType]
OptionalMultiMaterialType = OptionalSingleOrSequence[MaterialType]
