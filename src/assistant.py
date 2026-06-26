from src.rag import answer_question
from src.tools import summarize_document, compare_concepts


class AIResearchAssistant:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.history = []

    def ask(self, question: str):
        answer, sources = answer_question(
            self.vector_store,
            question,
            self.history
        )

        self.history.append({
            "user": question,
            "assistant": answer
        })

        return answer, sources

    def summarize(self):
        summary = summarize_document(self.vector_store)

        self.history.append({
            "user": "Summarize the document",
            "assistant": summary
        })

        return summary

    def compare(self, comparison_request: str):
        comparison = compare_concepts(self.vector_store, comparison_request)

        self.history.append({
            "user": comparison_request,
            "assistant": comparison
        })

        return comparison

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []