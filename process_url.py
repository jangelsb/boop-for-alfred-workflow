import yaml
import os
import sys
import urllib.parse
import re
from datetime import datetime

def parse_tags(input_tags):
    """Parses the YAML string into a dictionary."""
    try:
        return yaml.safe_load(input_tags)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return {}

def remove_urls(query):
    """Removes URLs from the query."""
    url_pattern = r'https?://\S+|www\.\S+'
    return re.sub(url_pattern, '', query)

def get_matching_tags(query, tags_dict):
    """Finds the tags that match any of the keywords in the query."""
    query_lower = query.lower()
    matched_tags = []

    for tag, keywords in tags_dict.items():
        for keyword in keywords:
            # Match keywords as whole words or followed by punctuation

            # print("----")
            # print(keyword)
            # print(query_lower)
            word_pattern = rf'(^|\s|\b){re.escape(keyword)}(\b|\s|$)'
            if re.search(word_pattern, query_lower):
                matched_tags.append(tag)
                break

    return matched_tags

def process(query, tags, url_scheme):
    # Remove URLs from the query
    query_without_urls = remove_urls(query)

    # Parse the tags into a dictionary
    tags_dict = parse_tags(tags)

    # Find the matching tags for the query
    matched_tags = get_matching_tags(query_without_urls, tags_dict)

    # Replace placeholders in the URL
    tags_string = ",".join(matched_tags)
    today_date = datetime.now().strftime("%Y-%m-%d")
    url = url_scheme.replace("[query]", urllib.parse.quote(query)).replace("[tags]", urllib.parse.quote(tags_string)).replace("[today]", today_date)
        
    return url, matched_tags


if __name__ == "__main__":
    process(sys.argv[1])
    
