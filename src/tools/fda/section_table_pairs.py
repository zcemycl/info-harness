"""Map FDA prose section attrs to their companion table attrs."""

from __future__ import annotations

from model.fda.fda_attr_name import FdaAttrName

_SECTION_TO_TABLES: dict[FdaAttrName, FdaAttrName] = {
    FdaAttrName.ADVERSE_EFFECTS: FdaAttrName.ADVERSE_EFFECT_TABLES,
    FdaAttrName.CLINICAL_TRIALS: FdaAttrName.CLINICAL_TRIAL_TABLES,
}


def section_table_pair(attr: FdaAttrName) -> FdaAttrName | None:
    """Return the paired ``*_tables`` attr, or None if attr is not a prose section."""
    return _SECTION_TO_TABLES.get(attr)


def is_section_with_tables(attr: FdaAttrName) -> bool:
    """True when attr is a prose section that may embed table placeholders."""
    return attr in _SECTION_TO_TABLES


def is_tables_attr(attr: FdaAttrName) -> bool:
    """True when attr is a companion tables field."""
    return attr in _SECTION_TO_TABLES.values()
