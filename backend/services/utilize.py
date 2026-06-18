import sqlite3
import hashlib
import json
from datetime import datetime

import pandas as pd
from sympy import im

DB_PATH = "llm_cache.db"


def get_conn():
    return sqlite3.connect(DB_PATH)


def init_cache_db():
    conn = get_conn()

    conn.execute("""
    CREATE TABLE IF NOT EXISTS llm_cache (
        cache_key TEXT PRIMARY KEY,
        query TEXT,
        books TEXT,
        response TEXT,
        model TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


def make_cache_key(query, books, model):
    data = {
        "query": query,
        "books": books,
        "model": model
    }

    raw = json.dumps(data, sort_keys=True)

    return hashlib.md5(raw.encode()).hexdigest()


def get_cache(cache_key):
    conn = get_conn()

    row = conn.execute(
        "SELECT response FROM llm_cache WHERE cache_key=?",
        (cache_key,)
    ).fetchone()

    conn.close()

    return row[0] if row else None


def save_cache(cache_key, query, books, response, model):
    conn = get_conn()

    conn.execute("""
    INSERT OR REPLACE INTO llm_cache
    (cache_key, query, books, response, model, created_at)
    VALUES (?,?,?,?,?,?)
    """, (
        cache_key,
        query,
        json.dumps(books),
        response.content if hasattr(response, "content") else str(response),
        model,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()


def normalize_books(books):
    """Ensure books is always list[dict]."""

    if isinstance(books, pd.DataFrame):
        return books.to_dict(orient="records")

    if isinstance(books, str):
        try:
            return json.loads(books)
        except Exception:
            raise ValueError("books is string but not valid JSON")

    if isinstance(books, list):
        return books

    raise TypeError(f"Unsupported books type: {type(books)}")


def cached_llm(model_name):
    def decorator(func):
        def wrapper(query: str, books, llm, *args, **kwargs):
            nor_books = normalize_books(books)
            book_titles = [
                b.get("title", "") for b in nor_books
            ]

            cache_key = make_cache_key(
                query,
                book_titles,
                model_name
            )

            cached = get_cache(cache_key)

            if cached:
                return {
                    "content": cached,
                    "cached": True
                }

            result = func(query, books, llm, *args, **kwargs)

            save_cache(
                cache_key,
                query,
                book_titles,
                result,
                model_name
            )

            return {
                "content": result.content if hasattr(result, "content") else str(result),
                "cached": False
            }

        return wrapper

    return decorator
