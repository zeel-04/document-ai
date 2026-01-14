from typing import Any

from document_ai.base import (
    BaseExtractor,
    BaseFormatter,
    BaseParser,
)
from document_ai.extractor import PDFExtractor
from document_ai.formatter import PDFFormatter
from document_ai.llm import BaseLLM
from document_ai.parser import DigitalPDFParser
from document_ai.schemas import Document, Mode, PDFDocument, PydanticModel


class DocumentProcessor:
    def __init__(
        self,
        parser: BaseParser,
        formatter: BaseFormatter,
        extractor: BaseExtractor,
        document: Document,
        mode: Mode = Mode(),
    ):
        self.parser = parser
        self.formatter = formatter
        self.extractor = extractor
        self.document = document
        self.mode = mode

    @classmethod
    def from_pdf(
        cls, uri: str, llm: BaseLLM, mode: Mode | None = Mode(), **kwargs
    ) -> "DocumentProcessor":
        """Create processor for PDF documents"""
        return cls(
            parser=DigitalPDFParser(),
            formatter=PDFFormatter(),
            extractor=PDFExtractor(llm),
            document=PDFDocument(uri=uri),
            mode=mode,  # type: ignore
            **kwargs,
        )

    def parse(self) -> Document:
        self.document.content = self.parser.parse(self.document)
        return self.document

    def format_document_for_llm(self) -> str:
        if not self.document.content:
            raise ValueError("Please parse the document first")
        self.document.llm_input = self.formatter.format_document_for_llm(
            self.document,
            self.mode,
        )
        return self.document.llm_input

    def extract(
        self,
        model: str,
        reasoning: Any,
        response_format: PydanticModel,
        system_prompt: str | None = None,
        user_prompt: str | None = None,
        openai_text: dict[str, Any] | None = None,
    ) -> Any:
        # Auto-parse and format if not done
        if not self.document.content:
            self.parse()
        if not self.document.llm_input:
            self.format_document_for_llm()

        return self.extractor.extract(
            document=self.document,
            model=model,
            reasoning=reasoning,
            response_format=response_format,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            mode=self.mode,
            llm_input=self.document.llm_input,  # type: ignore[reportUnknownReturnType]
            openai_text=openai_text,
        )
