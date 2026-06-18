
from math import exp


def build_book_context(top_books):
    """Convert a set of top book rows into a formatted context string."""

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
    """Build the prompt used to generate an explanation for recommended books.

    Args:
        query: The user's request for book recommendations.
        context: The formatted book context to include in the prompt.

    Returns:
        A formatted prompt string for the language model.
    """

    return f"""
        You are a book recommendation assistant.
        IMPORTANT:
        - Always respond in Turkish.
        - Do not use English unless book titles require it.
        - Keep explanations natural and fluent.

        User query:
        {query}

        Retrieved books:

        {context}

        Explain why these books match the user's request.

        For each book:
        - mention relevance
        - mention themes
        - be concise

        Do not invent information.
        """


def recommend_with_explanation(query, books, llm):
    """Generate book recommendations with an explanation.

    Args:
        query: The user's request for book recommendations.
        books: A dataframe of books to include in the context.
        llm: The language model used to generate the explanation.

    Returns:
        A dictionary containing the books and the generated explanation.
    """

    context = build_book_context(
        books
    )

    prompt = create_explain_prompt(
        query,
        context
    )

    explanation = llm.invoke(
        prompt
    )

    return explanation
