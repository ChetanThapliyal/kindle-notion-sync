from notion_client import Client
import os

database_ID = os.environ.get("database_ID")
secret_Key = os.environ.get("secret_Key")

# Initialize the Notion client
notion = Client(auth=secret_Key)

def validate_env_vars():
    if not database_ID or not secret_Key:
        raise ValueError("Database ID and secret key must be set as environment variables")

    return database_ID, secret_Key

def get_pageid_for_title(title):
    response = notion.databases.query(
        database_id=database_ID,
        filter={
            "property": "Title",
            "rich_text": {
                "equals": title
            }
        }
    )

    if len(response['results']) == 0:
        return None

    page_id = response['results'][0]['id']
    return page_id

def get_list_of_paragraphs_for_page_with_title(title):
    page_id = get_pageid_for_title(title)

    response = notion.blocks.children.list(block_id=page_id)

    paragraphs = []
    for item in response['results']:
        if 'quote' in item.keys():
            for words in item['quote']['rich_text']:
                stringer = (words['plain_text'], "highlight")
        elif 'callout' in item.keys():
            for words in item['callout']['rich_text']:
                stringer = (words['plain_text'], "note")

        paragraphs.append(stringer)

    return paragraphs

def append_items_to_page(title, items):
    page_id = get_pageid_for_title(title)

    children_list = []
    for item in items:
        if item[1] == "highlight":
            children_list.append(
                {
                    "type": "quote",
                    "quote": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content":item[0],
                            },
                        }],
                        "color": "default"
                    }
                }
            )
        else:
            children_list.append(
                {
                    "type": "callout",
                    "callout": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content":item[0],
                            },
                        }],
                        "icon": {
                            "emoji": "⭐"
                        },
                        "color": "default"
                    }
                }
            )

    notion.blocks.children.append(block_id=page_id, children=children_list)

def create_page(title, author, paragraph_list):
    children_list = []
    for text in paragraph_list:
        if text[1] == "highlight":
            children_list.append(
                {
                    "type": "quote",
                    "quote": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content":text[0],
                            },
                        }],
                        "color": "default"
                    }
                }
            )
        else:
            children_list.append(
                {
                    "type": "callout",
                    "callout": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content":text[0],
                            },
                        }],
                        "icon": {
                            "emoji": "⭐"
                        },
                        "color": "default"
                    }
                }
            )

    notion.pages.create(
        parent={"database_id": database_ID},
        properties={
            "Title": {
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Author": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": author
                        }
                    },
                ]
            }
        },
        children=children_list
    )