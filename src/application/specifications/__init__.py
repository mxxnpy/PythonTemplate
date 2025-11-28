# specifications - regras de negocio
from src.application.specifications.example_specs import (
    ExampleActiveSpec,
    ExampleNotDeletedSpec,
    NameNotEmptySpec,
    ValueInRangeSpec,
    ValuePositiveSpec,
    example_can_be_modified,
)

__all__ = [
    "NameNotEmptySpec",
    "ValuePositiveSpec",
    "ValueInRangeSpec",
    "ExampleActiveSpec",
    "ExampleNotDeletedSpec",
    "example_can_be_modified",
]
