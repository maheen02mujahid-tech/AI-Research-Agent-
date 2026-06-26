from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def summarize_document(vector_store):
    retriever = vector_store.as_retriever(search_kwargs={"k": 10})
    docs = retriever.invoke("main topic key points conclusion important concepts")

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = ChatPromptTemplate.from_template("""
You are an AI research assistant.

Summarize the document using ONLY the context below.

Include:
1. Main topic
2. Key points
3. Important terms
4. Short conclusion

Context:
{context}
""")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({"context": context})


def extract_comparison_terms(comparison_request: str):
    prompt = ChatPromptTemplate.from_template("""
Extract the two main concepts being compared from the request.

Request:
{comparison_request}

Return only the two concepts separated by a comma.
Example:
self-checking logic, monotonic logic
""")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({"comparison_request": comparison_request})
    terms = [term.strip() for term in result.split(",")]

    if len(terms) < 2:
        return comparison_request, comparison_request

    return terms[0], terms[1]


def compare_concepts(vector_store, comparison_request: str):
    retriever = vector_store.as_retriever(search_kwargs={"k": 6})

    concept_a, concept_b = extract_comparison_terms(comparison_request)

    docs_a = retriever.invoke(concept_a)
    docs_b = retriever.invoke(concept_b)

    context_a = "\n\n".join(doc.page_content for doc in docs_a)
    context_b = "\n\n".join(doc.page_content for doc in docs_b)

    prompt = ChatPromptTemplate.from_template("""
You are an AI research assistant.

Compare the two concepts using ONLY the retrieved document context below.
If one side has weaker document support, say so clearly.

Concept A:
{concept_a}

Context for Concept A:
{context_a}

Concept B:
{concept_b}

Context for Concept B:
{context_b}

User comparison request:
{comparison_request}

Write the answer with:
1. Short definition of Concept A
2. Short definition of Concept B
3. Key similarities
4. Key differences
5. Document coverage limitations, if any
""")

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    chain = prompt | llm | StrOutputParser()

    return chain.invoke({
        "concept_a": concept_a,
        "context_a": context_a,
        "concept_b": concept_b,
        "context_b": context_b,
        "comparison_request": comparison_request
    })