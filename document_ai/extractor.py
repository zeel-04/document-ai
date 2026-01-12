from typing import Any

from .base import BaseExtractor
from .llm import BaseLLM
from .schemas import Document, Mode, PydanticModel


class PDFExtractor(BaseExtractor):
    def __init__(self, llm: BaseLLM):
        super().__init__(llm)

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
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        return self.llm.generate_structured_output(
            model=model,
            messages=messages,
            reasoning=reasoning,
            output_format=response_format,
            openai_text=openai_text,
        )
