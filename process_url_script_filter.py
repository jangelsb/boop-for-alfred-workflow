import sys
import json
import os
import yaml
import urllib.parse
import re
from datetime import datetime
from process_url import process

class URLScheme:
    def __init__(self, title, urlScheme, url=None, icon=None):
        self.title = title
        self.urlScheme = urlScheme
        self.url = url
        self.icon = icon


class ResultItem:
    def __init__(self, title, arg, subtitle='', autocomplete=None, location=None, valid=True, mods=None, text=None, uid=None, icon_path=None, type=None, quicklookurl=None, should_skip_smart_sort=None):
        self.uid = uid if uid else title
        self.title = title
        self.arg = arg
        self.subtitle = subtitle
        self.autocomplete = autocomplete 
        self.valid = valid
        self.mods = mods if mods else {}
        self.text = text
        self.icon_path = icon_path
        self.type = type
        self.quicklookurl = quicklookurl
        self.should_skip_smart_sort = should_skip_smart_sort

    def to_dict(self):
        item_dict = {
            "uid": self.uid if self.should_skip_smart_sort is None or self.should_skip_smart_sort is False else None,
            "title": self.title,
            "arg": self.arg,
            "subtitle": self.subtitle,
            "autocomplete": self.autocomplete,
            "valid": self.valid,
            "type": self.type if self.type else "default",
            "quicklookurl": self.quicklookurl
        }
        if self.mods:
            item_dict["mods"] = {mod.key.value: mod.to_dict()[mod.key.value] for mod in self.mods if mod.key is not None}
        if self.text:
            item_dict["text"] = self.text.to_dict()
        if self.icon_path:
            item_dict["icon"] = {
                "path": self.icon_path
            }

        if self.should_skip_smart_sort:
            item_dict["skipknowledge"] = True

        return {k: v for k, v in item_dict.items() if v is not None}


def generate_list_from_yaml(yaml_string):
    def entry_processor(entry):
        title = entry['title']
        url = entry['url']
        icon = entry.get('icon', None)

        return URLScheme(title=title, urlScheme=url, icon=icon)

    try:
        yaml_data = yaml.safe_load(yaml_string)
        return [entry_processor(entry) for entry in yaml_data]
    except yaml.YAMLError as e:
        # print(f"YAML error: {e}")
        return []
    except Exception as e:
        # print(f"An error occurred: {e}")
        return []


def main(query):
    input_url_scheme_list = os.getenv('input_url_scheme_list')
    input_tags = os.getenv('input_tags')

    url_items = generate_list_from_yaml(input_url_scheme_list)

    matched_tags = None
    for item in url_items:
        url, tags = process(query=query, tags=input_tags, url_scheme=item.urlScheme)
        item.url = url
        matched_tags = tags
        

    output = {"items": []}

    output['items'] += [ResultItem(title=item.title, arg=item.url, icon_path=item.icon).to_dict() for item in url_items]

    found_tags_item = ResultItem(title=f"Tags", arg=None, subtitle=f"{matched_tags}", icon_path="tag.png", valid=False, should_skip_smart_sort=True)

    output['items'] += [found_tags_item.to_dict()]

        
    sys.stdout.write(json.dumps(output))


if __name__ == "__main__":
    main(sys.argv[1])