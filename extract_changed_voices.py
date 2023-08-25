from collections import defaultdict
import os
import subprocess
import json

class ProcessSettings():
    def __init__(self, chapter_name, chapter_path, before_voices_sha, after_voices_sha) -> None:
        self.chapter_name = chapter_name
        self.chapter_path = chapter_path
        self.before_voices_sha = before_voices_sha
        self.after_voices_sha = after_voices_sha


def process_chapter(conf: ProcessSettings):
    diff_filename = 'temp_raw_diff.diff'
    diff_path = os.path.abspath(diff_filename)

    if os.path.exists(diff_path):
        os.remove(diff_path)

    try:
        args = ['git', 'diff', f'{conf.before_voices_sha}..{conf.after_voices_sha}', f'--output={diff_path}']
        subprocess.check_call(args, cwd=conf.chapter_path)
    except Exception as e:
        print("----------------------------------------------------------")
        print(f"Error running script for chapter {conf.chapter}. Are you sure:")
        print("- git is installed")
        print("- the chapter/SHA references are correct")
        print("- this script is in the root of the git repo")
        print("- the git repo is up to date?")
        print("----------------------------------------------------------")
        exit(-1)

    with open(diff_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    last_line = None
    line_replacements_per_file = defaultdict(list)
    current_file = None

    for line in lines:
        if line.startswith('+++'):
            current_file = line[6:]

        if last_line == None:
            last_line = line
            continue

        if last_line.startswith('-') and last_line.lstrip('-').strip().lower().startswith('modplayvoicels'):
            if line.startswith('+') and line.lstrip('+').strip().lower().startswith('modplayvoicels'):
                if current_file is None:
                    raise Exception("Current file is unknown!")

                line_replacements_per_file[current_file].append((last_line[1:].rstrip(), line[1:].rstrip()))

        last_line = line

    return line_replacements_per_file

# Chapter name should match prefix of most scripts inside Update folder
settings_list = [
    ProcessSettings('onik', 'C:/drojf/large_projects/umineko/HIGURASHI_REPOS/1 onikakushi', "bd2a98735890d10c365de93e9b16f71d59af662b", "72a2f10bdd0d9f4559c7345b783611cc649b4775"),
    ProcessSettings('wata', 'C:/drojf/large_projects/umineko/HIGURASHI_REPOS/2 watanagashi', "c88e8b898e8876515986fd0784f67d1b920bb6b2", "729fa6a2e0a99b1ad8b9dabf8e23c1c8a98b90e2"),
    ProcessSettings('tata', 'C:/drojf/large_projects/umineko/HIGURASHI_REPOS/3 tatarigoroshi', "f4a894daa9f5c5353bbb65b916d6a897f1e615f5", "d9670d2b751c04164afccf7d269b05da38e50151"),
    ProcessSettings('hima', 'C:/drojf/large_projects/umineko/HIGURASHI_REPOS/4 himatsubushi', "2a060413500634ef3e19ef21c148658caa0b6914", "94787c4280be455d21f9e0ca27fb9d5fadd636b1"),
    ProcessSettings('_meak', 'C:/drojf/large_projects/umineko/HIGURASHI_REPOS/5 meakashi', "38516d0dae8b0786e6ab8777ec86c3ab6a7659ea", "ce5073b6bf137729ddc5e15ac67a96138bef9c0f")
]

# Process each chapter, and collect as replacements per-chapter
chapter_to_replacements_list = {}
for conf in settings_list:
    replacements = process_chapter(conf)
    chapter_to_replacements_list[conf.chapter_name] = replacements

    total_replacements = 0
    for filename, file_replacements in replacements.items():
        total_replacements += len(file_replacements)

    print(f"Chapter {conf.chapter_name} had {len(replacements)} files with {total_replacements} replacements at {conf.chapter_path} from {conf.before_voices_sha[0:6]}... to {conf.after_voices_sha[0:6]}...")

# Save all chapters replacements as json file
with open('origin_replacements.json', 'w', encoding='utf-8') as f:
    json.dump(chapter_to_replacements_list, f, ensure_ascii=False, indent=4)
