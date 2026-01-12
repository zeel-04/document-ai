from abc import ABC, abstractmethod
from typing import Any

from .llm import BaseLLM
from .schemas import Document, Mode, PydanticModel


class BaseParser(ABC):
    @abstractmethod
    def parse(self, document: Document) -> PydanticModel:
        pass


class BaseFormatter(ABC):
    @abstractmethod
    def format_for_llm(self, content: PydanticModel, mode: Mode) -> list[str] | str:
        pass


class BaseExtractor(ABC):
    def __init__(self, llm: BaseLLM):
        self.llm = llm

    @abstractmethod
    def extract(
        self,
        document: Document,
        model: str,
        reasoning: Any,
        response_format: PydanticModel,
        system_prompt: str,
        user_prompt: str,
        mode: Mode,
        openai_text: dict[str, Any] | None = None,
    ) -> Any:
        pass


class DocumentProcessor:
    def __init__(
        self,
        parser: BaseParser,
        formatter: BaseFormatter,
        extractor: BaseExtractor,
        document: Document,
        mode: Mode,
    ):
        self.parser = parser
        self.formatter = formatter
        self.extractor = extractor
        self.document = document
        self.mode = mode

    def parse(self) -> Document:
        self.document.content = self.parser.parse(self.document)
        return self.document

    def formatted_input_for_llm(self) -> list[str] | str:
        if not self.document.content:
            raise ValueError("Please parse the document first")
        self.document.llm_input = self.formatter.format_for_llm(
            self.document.content,  # type: ignore
            self.mode,
        )
        return self.document.llm_input

    def extract(
        self,
        model: str,
        reasoning: Any,
        response_format: PydanticModel,
        system_prompt: str,
        user_prompt: str,
        openai_text: dict[str, Any] | None = None,
    ) -> Any:
        if not self.document.content and not self.document.llm_input:
            raise ValueError("Either document content or llm input is missing")
        return self.extractor.extract(
            document=self.document,
            model=model,
            reasoning=reasoning,
            response_format=response_format,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            mode=self.mode,
            openai_text=openai_text,
        )
