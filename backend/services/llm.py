from urllib import response

from pygments.unistring import No
from sklearn.utils import resample
from sympy import im

from .utilize import cached_llm


def build_book_context(top_books):
    """Convert top books into prompt context."""

    context = ""

    for _, row in top_books.iterrows():

        context += f"""
            Title: {row['title']}
            Rating: {row['semantic_score']}

            Description:
            {row['description'][:500]}

            ---
        """

    return context


def create_explain_prompt(query, context):
    """Build LLM prompt for explanation."""

    return f"""
        You are a book recommendation assistant.

        IMPORTANT:
        - Always respond in Turkish
        - Do not use English unless book titles require it
        - Be natural and concise

        User query:
        {query}

        Retrieved books:

        {context}

        Task:
        Explain why each book matches the request.

        Rules:
        - Mention relevance
        - Mention themes
        - Do not invent information
    """


@cached_llm("gemini-2.5-flash-lite")
def recommend_with_explanation(query: str, books, llm):
    """Generate explanation for recommended books."""
    context = build_book_context(books)

    prompt = create_explain_prompt(query, context)

    response = llm.invoke(prompt)

    return response
