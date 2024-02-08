from dataclasses import dataclass
import logging
import os
import jellyfish
import pathlib
import argparse


parser = argparse.ArgumentParser(
    prog='dedup',
    description='execute python script to remove file duplicates in specified directory',
    epilog='Please leave feedback in case of any bug. :-)'
)

parser.add_argument('filepath', help='path to directory against which program will be executed', type=str)
parser.add_argument('--filename-distance', help='specify threshold [0..N] for filename diff (0 - exact comparison)', type=int, default=0)
parser.add_argument('--filesize-threshold', help='specify threshold [0..N bytes] for file size equality (0 - exact comparison)', type=int, default=0)
parser.add_argument('--suffix', help='filter input files by suffix (e.g. `.mp3`, `.wav`)', type=str, default=None)
parser.add_argument('--skip-confirmation', help='skip delete-confirmation', action='store_const', const=True)
parser.add_argument('--debug', help='enable debug logs', action='store_const', const=True)

args = parser.parse_args()

if not os.path.isabs(args.filepath):
    args.filepath = os.path.abspath(os.path.join(os.getcwd(), args.filepath))

FILEPATH = pathlib.Path(args.filepath)
FILENAME_DISTANCE = args.filename_distance
FILESIZE_THRESHOLD = args.filesize_threshold
SKIP_CONFIRMATION = args.skip_confirmation
SUFFIX_FILTER = args.suffix
DEBUG = args.debug

if DEBUG:
    print(args)

@dataclass
class Match:
    path: pathlib.Path
    dist: int | None

def suffix_filter(f: pathlib.Path):
    if SUFFIX_FILTER:
        return f.suffix == SUFFIX_FILTER
    return True
original_seq = [f for f in FILEPATH.iterdir() if f.is_file() and suffix_filter(f)]
total_files = len(original_seq)

groups = dict()

selected = []

loop1_iter = 0
loop2_iter = 0
for f1 in original_seq.copy():
    loop1_iter += 1
    try:
        original_seq.remove(f1)
        selected.append(f1)
        groups[f1] = [Match(f1, None)]
    except ValueError:
        continue
    for f2 in original_seq.copy():
        loop2_iter += 1
        if abs(f1.stat().st_size - f2.stat().st_size) > FILESIZE_THRESHOLD:
            continue
        dist = jellyfish.levenshtein_distance(f1.stem, f2.stem)
        if dist <= FILENAME_DISTANCE:  
            selected.append(f2)
            groups[f1].append(Match(f2, dist))
            original_seq.remove(f2)

def print_file_matchtes(_list: list[Match]):
    for m in _list:
        print(f'{m.path} {m.dist}')

dup_groups = []

for k,v in groups.items():
    if len(v) == 1:
        continue
    print('FILE:')
    print_file_matchtes(v)
    dup_groups.append(v)
    print()

total_duplicates = len(selected) - len(groups)

if DEBUG:
    print(f'SELECTED: {len(selected)}')
    print(f'UNIQUE_FILES: {len(groups)}')
    print(f'DUPLICATES: {total_duplicates}')
    print(f'TOTAL_FILES {total_files}')
    print(f'LOOP1_ITER: {loop1_iter}')
    print(f'LOOP2_ITER: {loop2_iter}')
    print()

if len(selected) != total_files:
    logging.error('Unexpected result during search. Total files differ from selected count.')
    logging.error('Highly chance there is a bug in selection algo. Fix bug and try again...')
    exit(1)

if total_duplicates == 0:
    print(f'Found {total_duplicates} duplicates.')
    exit()

if SKIP_CONFIRMATION:
    proceed = 'y'
else:
    proceed = input(f'Found {total_duplicates} duplicates to be deleted. Proceed? (y/n): ')

if proceed == 'y' or proceed == 'yes':
    print('Removing duplicates...')
    for g in dup_groups:
        for dup in g[1:]:
            dup.path.unlink()
    print('Done')
else:
    exit()