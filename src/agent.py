from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.assistant import AIResearchAssistant


class AgentState(TypedDict):
    user_input: str
    route: Optional[str]
    answer: Optional[str]


def classify_request(state: AgentState):
    prompt = ChatPromptTemplate.from_template("""
Classify the user's request into exactly one category:

- question: normal questions, teaching requests, explanations, follow-up questions, or requests to simplify a previous answer
- summarize: only when the user clearly asks to summarize the whole document
- compare: only when the user asks to compare two or more concepts/documents

Examples:
"What is self-checking logic?" -> question
"Explain it more simply" -> question
"Teach me hardware redundancy" -> question
"Summarize the document" -> summarize
"Compare self-checking logic and monotonic logic" -> compare

User request:
{user_input}

Return only one word: question, summarize, or compare.
""")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm | StrOutputParser()

    route = chain.invoke({"user_input": state["user_input"]}).strip().lower()

    if route not in ["question", "summarize", "compare"]:
        route = "question"

    return {"route": route}


def route_decision(state: AgentState):
    return state["route"]


def format_sources(sources):
    seen = set()
    source_text = "\n\nSources:"

    for doc in sources:
        page = doc.metadata.get("page", 0) + 1
        source = doc.metadata.get("source", "unknown file")

        source_name = source.replace("\\", "/").split("/")[-1]
        key = (source_name, page)

        if key in seen:
            continue

        seen.add(key)

        snippet = doc.page_content.replace("\n", " ").strip()
        snippet = snippet[:250]

        source_text += (
            f"\n\n---\n"
            f"File: {source_name}\n"
            f"Page: {page}\n"
            f"Excerpt: {snippet}..."
        )

    return source_text


def build_research_agent(assistant: AIResearchAssistant):
    graph = StateGraph(AgentState)

    def question_node(state: AgentState):
        answer, sources = assistant.ask(state["user_input"])
        source_text = format_sources(sources)
        return {"answer": answer + source_text}

    def summarize_node(state: AgentState):
        summary = assistant.summarize()
        return {"answer": summary}

    def compare_node(state: AgentState):
        comparison = assistant.compare(state["user_input"])
        return {"answer": comparison}

    graph.add_node("classify", classify_request)
    graph.add_node("question", question_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("compare", compare_node)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        route_decision,
        {
            "question": "question",
            "summarize": "summarize",
            "compare": "compare",
        }
    )

    graph.add_edge("question", END)
    graph.add_edge("summarize", END)
    graph.add_edge("compare", END)

    return graph.compile()