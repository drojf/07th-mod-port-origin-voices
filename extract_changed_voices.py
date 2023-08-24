import subprocess


diff_file = 'temp_raw_diff.diff'

# Meakashi
chapter = 'meakashi'
before_voices_sha = "38516d0dae8b0786e6ab8777ec86c3ab6a7659ea"
after_voices_sha = "ce5073b6bf137729ddc5e15ac67a96138bef9c0f"

print(f"Tracing from {before_voices_sha} to {after_voices_sha}")

try:
    raw_diff_bytes = subprocess.check_output(['git', 'diff', f'{before_voices_sha}..{after_voices_sha}', f'--output={diff_file}'])
except Exception as e:
    print("----------------------------------------------------------")
    print(f"Error running script for chapter {chapter}. Are you sure:")
    print("- git is installed")
    print("- the chapter/SHA references are correct")
    print("- this script is in the root of the git repo")
    print("- the git repo is up to date?")
    print("----------------------------------------------------------")
    exit(-1)

with open(diff_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

last_line = None
line_pairs = []

for line in lines:
    if last_line == None:
        last_line = line
        continue

    if last_line.startswith('-') and last_line.lstrip('-').strip().lower().startswith('modplayvoicels'):
        if line.startswith('+') and line.lstrip('+').strip().lower().startswith('modplayvoicels'):
            line_pairs.append((last_line, line))

    last_line = line


for (last_line, line) in line_pairs:
    print("Got change pair:")
    print(last_line.strip())
    print(line.strip())


print(f"Got {len(line_pairs)} pairs")