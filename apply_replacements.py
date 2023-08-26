# Read all chapters replacements as json file
import json
import os
from pathlib import Path

def get_chapter_replacements_per_file():
    for chapter_fingerprint, chapter_replacements_by_file in origin_replacements.items():

        for file in os.listdir('Update'):
            if file.lower().startswith(chapter_fingerprint):
                print(f"Detected fingerprint {chapter_fingerprint} at file {file}")
                return chapter_replacements_by_file

    raise Exception("Couldn't determine chapter!")


with open('origin_replacements.json', 'r', encoding='utf-8') as f:
    origin_replacements = json.load(f)

# Check that the 07th-mod script folder exists (hopefully we are inside a git repository)
if not os.path.exists('Update'):
    raise Exception("No Update folder found - Check this script is being run from inside a git repository")

# Determine which chapter is being updated, and extract the replacements for this chapter from the JSON file
replacements_per_file = get_chapter_replacements_per_file()

replace_fail = 0
replace_success = 0

for file_to_replace, replacements in replacements_per_file.items():
    print(f"Processing {file_to_replace}...", end='')

    # Read in the file on a line-by-line basis
    with open(file_to_replace, 'r', encoding='utf-8') as f:
        script_lines = f.readlines()

    per_file_success = 0

    # This is extremely inefficient but we will only run this script once per translation
    for (original_line, replacement_line) in replacements:

        # Make each replacement once
        replacement_made = False
        for i in range(0, len(script_lines)):
            temp_line = script_lines[i]

            if temp_line.startswith(original_line):
                script_lines[i] = replacement_line + '\n'
                replacement_made = True
                break

        # Collect statistics for debugging
        if replacement_made:
            per_file_success += 1
            replace_success += 1
        else:
            print(f"\t{file_to_replace}: Failed to replace {original_line.strip()} -> {replacement_line.strip()}")
            replace_fail += 1

    print(f'{per_file_success}/{len(replacements)}')

    # Write out modified file
    out_file_path = Path('UpdateWithOrigin').joinpath(*Path(file_to_replace).parts[1:])
    Path(out_file_path).parent.mkdir(exist_ok=True, parents=True)
    with open(out_file_path, 'w', encoding='utf-8') as f:
        f.writelines(script_lines)

print(f"SUMMARY: Replaced {replace_success}/{(replace_success + replace_fail)}")
