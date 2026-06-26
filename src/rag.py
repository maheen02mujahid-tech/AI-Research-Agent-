from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def answer_question(vector_store, question: str, history=None):
    retriever = vector_store.as_retriever(search_kwargs={"k": 8})
    docs = retriever.invoke(question)

    context = "\n\n".join(doc.page_content for doc in docs)

    if history is None:
        history = []

    history_text = ""
    for item in history[-3:]:
        history_text += f"User: {item['user']}\nAssistant: {item['assistant']}\n\n"

    prompt = ChatPromptTemplate.from_template(
        """
You are an AI research assistant and tutor.

Use the conversation history to understand follow-up questions.

You are allowed to use BOTH:
1. The uploaded document context
2. General AI knowledge

But you must clearly separate them.

Rules:
- If the uploaded documents contain relevant information, explain it under "From the uploaded documents".
- If useful extra explanation is needed, add it under "Additional explanation".
- If the uploaded documents do not contain enough information, say that clearly under "Document coverage".
- Do not pretend that general knowledge came from the documents.
- Keep the answer clear and student-friendly.

Conversation history:
{history}

Uploaded document context:
{context}

Question:
{question}

Answer using this format:

From the uploaded documents:
...

Additional explanation:
...

Document coverage:
...
"""
    )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    chain = prompt | llm | StrOutputParser()

    answer = chain.invoke({
        "history": history_text,
        "context": context,
        "question": question
    })

    return answer, docs