from .logging import configure_logging
from .structure import (
    Collection,
    Column,
    Subject,
    Vendor,
    merge_collections,
    merge_subjects,
)

configure_logging("ERROR")
