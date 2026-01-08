from pydantic import BaseModel

from .base import BaseFormatter
from .schemas import PydanticModel


class PDFFormatter(BaseFormatter):
    def _format_paginated(self, content: PydanticModel) -> list[str]:
        paginated = []
        if not content.pages:  # type: ignore
            raise ValueError("PDFFormatter: format_for_llm: Document pages are not set")
        for page_number, page in enumerate(content.pages):  # type: ignore
            lines_text = ""
            for line_number, line in enumerate(page.lines):
                line_text = f"{line_number}: {line.text}" + "\n"
                lines_text += line_text
            paginated.append(f"<page number={page_number}>\n{lines_text}</page>")
        return paginated

    def _format_complete(self, content: PydanticModel) -> str:
        complete = "\n".join(self._format_paginated(content))
        return complete

    def _format_paginated_without_line_numbers(
        self, content: PydanticModel
    ) -> list[str]:
        paginated = []
        if not content.pages:  # type: ignore
            raise ValueError("PDFFormatter: format_for_llm: Document pages are not set")
        for page_number, page in enumerate(content.pages):  # type: ignore
            lines_text = ""
            for _, line in enumerate(page.lines):
                line_text = f"{line.text}" + "\n"
                lines_text += line_text
            paginated.append(f"<page number={page_number}>\n{lines_text}</page>")
        return paginated

    def _format_complete_without_line_numbers(self, content: PydanticModel) -> str:
        complete = "\n".join(self._format_paginated_without_line_numbers(content))
        return complete

    def format_for_llm(
        self, content: PydanticModel, formatter_config: dict
    ) -> list[str] | str:
        flag = formatter_config.get("flag")
        if flag == "paginated_with_line_numbers":
            paginated = self._format_paginated(content)
            return paginated
        elif flag == "complete_with_line_numbers":
            complete = self._format_complete(content)
            return complete
        elif flag == "paginated_without_line_numbers":
            paginated_without_line_numbers = (
                self._format_paginated_without_line_numbers(content)
            )
            return paginated_without_line_numbers
        elif flag == "complete_without_line_numbers":
            complete_without_line_numbers = self._format_complete_without_line_numbers(
                content
            )
            return complete_without_line_numbers
        else:
            raise ValueError(f"PDFFormatter: format_for_llm: Invalid flag: {flag}")
