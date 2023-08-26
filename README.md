# 07th-mod-port-origin-voices

Scripts to port some higurashi origin voices from our main mod scripts to translated scripts

## NOTE

This script only ports simple changes (when a voice file has been replaced). Other changes, including addition of a new voice file where there was none previously, will not be ported.

## Usage

1. Put the `apply_replacements.py` and `origin_replacements.json` in the root of the 07th-mod git repository (next to the `Update` folder)
2. Run the `apply_replacements.py` with no arguments (need Python 3). The chapter should be detected automatically
3. Check the output of the script to see if everything was replaced, or some replacements were not made.
    - If many replacements were not made, it might be that the voice lines in your version of the script were modified. But if it's just a couply you can fix manually.
4. The output will appear in the folder `UpdateWithOrigin`. Only the files which were attempted to be modified will be output (if nothing was modified, the script probably tried to modify it).
5. Make sure to double check the changes are correct by diffing the `Update` and `UpdateWithOrigin` folder, and checking this against the full git changes for the mainline english version of the mod.
