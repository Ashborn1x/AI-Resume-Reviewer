from app.parsers.base import ResumeParser
from app.parsers.docx_parser import DocxResumeParser
from app.parsers.pdf_parser import PdfResumeParser
from app.parsers.txt_parser import TxtResumeParser
from app.services.exceptions import ParsingError


class ResumeParserFactory:
    def __init__(self) -> None:
        self._parsers: dict[str, ResumeParser] = {
            "pdf": PdfResumeParser(),
            "docx": DocxResumeParser(),
            "txt": TxtResumeParser(),
        }

    def get_parser(self, extension: str) -> ResumeParser:
        parser = self._parsers.get(extension.lower())
        if parser is None:
            raise ParsingError("No parser is available for this resume format.")
        return parser
