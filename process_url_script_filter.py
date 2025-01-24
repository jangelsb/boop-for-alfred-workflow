import sys
import json
import os


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


def get_js_files(directory):
    # Get all `.js` files in the specified directory, one level deep
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f)) and f.endswith(".js")
    ]


def main(query):
    scripts_directory = "./scripts"
    output = {"items": [], "variables": {}}

    # Get all .js files in the scripts directory
    js_files = get_js_files(scripts_directory)

    # Create ResultItems for each .js file that matches the query
    for js_file in js_files:
        title = os.path.basename(js_file)  # File name only
        if query.lower() in title.lower():  # Case-insensitive query filtering
            arg = js_file  # Full path
            result_item = ResultItem(title=title, arg=arg)
            output["items"].append(result_item.to_dict())

    # Add the input query to variables
    output["variables"]["query"] = query

    # Output the JSON for Alfred
    sys.stdout.write(json.dumps(output, indent=4))


if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    main(query)
