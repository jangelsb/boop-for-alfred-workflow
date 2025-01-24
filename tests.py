import subprocess
import os
import urllib.parse
from process_url import process


def validate_output(query, input_tags, input_url_scheme, expected_tags):
    """Validates the output of the script against expected values."""

    url, matched_tags = process(query=query, tags=input_tags, url_scheme=input_url_scheme)
    decoded_url = urllib.parse.unquote(url)
    tags = decoded_url.split('tags=')[-1]
    
    # Validate
    assert matched_tags == expected_tags, f"Expected tags {expected_tags}, but got {matched_tags}"

# Test cases
if __name__ == "__main__":
    input_tags = """
    work 📁:
      - work
      - ios
      - pr
      - lee

    review 👀:
      - pr
      - doc
      - review

    Card 💡:
      - create card
      - create a card

    Important 🔺:
      - '!!'
    """
    input_url_scheme = "sorted://x-callback-url/add?title=[title]&date=[today]&tags=[tags]"

    test_cases = [
        {
            "query": "Lee is working on iOS development.",
            "expected_tags": ["work 📁"],
        },
        {
            "query": "This PR needs to be reviewed.",
            "expected_tags": ["work 📁", "review 👀"],
        },
        {
            "query": "Create a card for this task.",
            "expected_tags": ["Card 💡"],
        },
        {
            "query": "This is very important !!",
            "expected_tags": ["Important 🔺"],
        },
        {
            "query": "Visit https://example.com for more info.",
            "expected_tags": [],
        },
        {
            "query": "Lee is working on a file",
            "expected_tags": ["work 📁"],
        },
        {
            "query": "Lee's file is working",
            "expected_tags": ["work 📁"],
        },
        {
            "query": "I need to flee to the store",
            "expected_tags": [],
        },
        {
            "query": "I need to flee to the store https://www.ios.org",
            "expected_tags": [],
        }
    ]

    for case in test_cases:
        validate_output(case["query"], input_tags, input_url_scheme, case["expected_tags"])
