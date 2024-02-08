# dedup

Simple python script to get rid of duplicated files.

## Installation

Requirements:
- ⚠️ Python 3.10+
- Bash

Install python:
> Use any way to get modern python, you used to. I use [mise](https://github.com/jdx/mise) to manage python versions.

Download repository with script:
```bash
git clone github.com/bulatenkom/dedup
cd dedup
```

Setup virtualenv (skip if you are going to use global python and pip).
```bash
python -m venv .venv
source .venv/bin/activate

# check that venv activated correctly
# both following commands should print paths directed to python/pip in .venv
which pip
which python
```

Install dependencies
```bash
pip install -r requirements
```

## Usage

```bash
python dedup.py --help
```

```bash
usage: dedup [-h] [--filename-distance FILENAME_DISTANCE]
             [--filesize-threshold FILESIZE_THRESHOLD] [--suffix SUFFIX] [--skip-confirmation]
             [--debug]
             filepath

execute python script to remove file duplicates in specified directory

positional arguments:
  filepath              path to directory against which program will be executed

options:
  -h, --help            show this help message and exit
  --filename-distance FILENAME_DISTANCE
                        specify threshold [0..N] for filename diff (0 - exact comparison)
  --filesize-threshold FILESIZE_THRESHOLD
                        specify threshold [0..N bytes] for file size equality (0 - exact
                        comparison)
  --suffix SUFFIX       filter input files by suffix (e.g. `.mp3`, `.wav`)
  --skip-confirmation   skip delete-confirmation
  --debug               enable debug logs

Please leave feedback in case of any bug. :-)
```

**Real case scenario**. Suppose end-user want to get rid of duplicate mp3 files in its music library. And duplicates can have similar names or similar file size.
To accomplish the task, using **dedup**, you can make a following command:
```bash
python dedup.py --filename-distance=1 --suffix=.mp3 ~/Music/music-library/
```
Here:
* **--filename-distance** - threshold for filename diff using [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance#:~:text=Informally%2C%20the%20Levenshtein%20distance%20between,considered%20this%20distance%20in%201965.)
* **--suffix** - filter input files by suffix (e.g. `.mp3`, `.wav`)

Produced output by **dedup**:
```makefile
FILE:
/home/bulatenkom/Music/music-library/077 - Phonky Trap.mp3 None
/home/bulatenkom/Music/music-library/078 - Phonky Trap.mp3 1

FILE:
/home/bulatenkom/Music/music-library/062 - Beggin'.mp3 None
/home/bulatenkom/Music/music-library/061 - Beggin'.mp3 1

Found 122 duplicates to be deleted. Proceed? (y/n): 
```

A **dedup** groups similar files and prints to standard output.
In last message user asked about starting/terminating of deduplication process.
If user enters "n", then program exits.
If user enters "y" or "yes", then all found duplicates will be deleted, except ones containing "None" in line (see standard output above clearly to spot "None" in lines)
In this conext "None" means original file, that will be preserved after deduplication.

Let's enter "y" and see output:
```bash
Found 122 duplicates to be deleted. Proceed? (y/n): y
Removing duplicates...
Done
```

That's it.

## Features nice to have, that you can implement on your own

- recursive search
- backing up removable files
- glob filter
- redirect STDOUT to separate file
- progress-bar
- alternative options to spot a similar files

## Dependencies / Credits

- [Jellyfish](https://github.com/jamesturk/jellyfish) - MIT

---
<div style="text-align: right">MIT</div>