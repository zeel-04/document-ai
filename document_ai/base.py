from abc import ABC, abstractmethod
from typing import Any

from .schemas import Document, PydanticModel


class BaseParser(ABC):
    @abstractmethod
    def parse(self, document: Document) -> PydanticModel:
        pass


class BaseFormatter(ABC):
    @abstractmethod
    def format_for_llm(
        self, content: PydanticModel, formatter_config: dict
    ) -> list[str] | str:
        pass


class DocumentProcessor:
    def __init__(
        self, parser: BaseParser, formatter: BaseFormatter, document: Document
    ):
        self.parser = parser
        self.formatter = formatter
        self.document = document

    def process(self, formatter_config: dict) -> Document:
        self.document.content = self.parser.parse(self.document)
        self.document.llm_input = self.formatter.format_for_llm(
            self.document.content,  # type: ignore
            formatter_config,  # type: ignore
        )
        return self.document
