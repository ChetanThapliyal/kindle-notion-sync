from kindle_scraper import get_highlights
from query_notion_database import (
    get_pageid_for_title,
    get_list_of_paragraphs_for_page_with_title,
    append_items_to_page,
    create_page,
)
import os

def validate_env_vars():
    email = os.environ.get("AMAZON_EMAIL")
    password = os.environ.get("AMAZON_PASSWORD")

    if not email or not password:
        raise ValueError("Amazon email and password must be set as environment variables")

    return email, password

def update_book_highlights_in_notion(email, password):
    book_highlights = get_highlights(email, password)

    for title in book_highlights:
        pageid = get_pageid_for_title(title)
        data = book_highlights[title]
        author = data["author"]
        highlights = data["highlights"]

        if pageid is None:
            create_page(title, author, highlights)
        else:
            notes = get_list_of_paragraphs_for_page_with_title(title)
            new_notes = [note for note in highlights if note not in notes]
            append_items_to_page(title, new_notes)

if __name__ == "__main__":
    email, password = validate_env_vars()
    update_book_highlights_in_notion(email, password)
