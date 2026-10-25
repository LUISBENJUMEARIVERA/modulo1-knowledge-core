import os
from langchain_core.output_parsers import StrOutputParser
from src.core.config import config
from src.core.llm_factory import get_llm
from src.chains.prompts import SUMMARY_PROMPT, FAQ_PROMPT, QA_PROMPT

class KnowledgeService:
    def __init__(self):
        self.context = self._load_context()
        self.llm = get_llm()

    def _load_context(self) -> str:
        if not os.path.exists(config.output_processed_file):
            return "No hay datos disponibles en la base de conocimiento."
        with open(config.output_processed_file, "r", encoding="utf-8") as f:
            return f.read().strip()

    def get_summary_stream(self):
        chain = SUMMARY_PROMPT | self.llm | StrOutputParser()
        return chain.stream({"context": self.context})

    def get_faq_stream(self):
        chain = FAQ_PROMPT | self.llm | StrOutputParser()
        return chain.stream({"context": self.context})

    def answer_question_stream(self, question: str):
        chain = QA_PROMPT | self.llm | StrOutputParser()
        return chain.stream({"context": self.context, "question": question})

# Instancia singleton para reutilizar
service = KnowledgeService()