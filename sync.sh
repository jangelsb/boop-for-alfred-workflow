#!/bin/bash

WORKFLOW_FOLDER="$boop_path"

FILES_TO_PUSH=("process_url.py" "process_url_script_filter.py")

# copy these files to the WORKFLOW_FOLDER
for FILE in "${FILES_TO_PUSH[@]}"; do
  cp "$FILE" "$WORKFLOW_FOLDER"
done


FILES_TO_PULL=("info.plist" "prefs.plist")
# copy these files to or from the WORKFLOW_FOLDER

# if `--push` then all will be pushed
if [[ "$1" == "--push" ]]; then
  for FILE in "${FILES_TO_PULL[@]}"; do
    cp "$FILE" "$WORKFLOW_FOLDER"
  done
else
  for FILE in "${FILES_TO_PULL[@]}"; do
    cp "$WORKFLOW_FOLDER/$FILE" .
  done
fi