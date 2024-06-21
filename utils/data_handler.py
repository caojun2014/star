from abc import ABC, abstractmethod
from langchain.document_loaders import PyPDFLoader

class DocumentHandler(ABC):
    @abstractmethod
    def handle(self, file_path: str) -> list:
        pass

class PdfHandler(DocumentHandler):
    def handle(self, file_path: str) -> list:
        loader = PyPDFLoader(file_path)
        return loader.load()


class DocumentHandlerFactory:
    @staticmethod
    def get_handler(file_type: str) -> DocumentHandler:
        if file_type == "pdf":
            return PdfHandler()
      
        else:
            raise ValueError(f"Unsupported file type: {file_type}")