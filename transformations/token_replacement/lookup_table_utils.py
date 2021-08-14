import os
import random
import gzip
import lzma
import json

from Levenshtein import distance as levenshtein_distance

from typing import List, Union

"""
Lookup table handling utilities.
"""

def get_token_replacement(input_token, lookup, max_dist):
    """
    Gets a replacement for an input token sampled from a given lookup table.
    Samples uniformly among all candidates available for an input token.
    Accepts additional filtering criteria based on the maximum edit distance 
    between the original and the candidate token.
    """
    candidates = lookup[input_token]

    if max_dist >= 0:
        candidates = [c for c in candidates \
            if levenshtein_distance(input_token, c) <= max_dist]

    if len(candidates) == 0:
        return input_token

    idx = random.randint(0, len(candidates) - 1)
    replacement_token = candidates[idx]
        
    return replacement_token


def load_lookup(files: Union[str, List[str]]) -> bool:
    """
    Loads a lookup table with replacement candidates from a file 
        (or every file in a list of files).        
    """
    if isinstance(files, str):
        lut = _load_lookup_from_file(files)
        return lut

    elif isinstance(files, list) or isinstance(files, tuple):
        lut = dict()

        for fn in files:
            lut_part = _load_lookup_from_file(fn)
                
            # merge dictionaries
            for key, value in lut_part.items():
                if key not in lut:
                    lut[key] = value
                else:
                    lut[key] += value                        
            
        return lut
    else:
        return {}

    
def _load_lookup_from_file(file_name: str):
    """
    Loads a lookup table with replacement candidates from a given file.
    """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, f"{file_name}")

    basename, ext = os.path.splitext(file_name)

    assert ext in [".gz", ".xz", ".json"], \
            f"File extension not supported '{ext}'"

    if ext == ".xz":
        with lzma.open(file_path, 'r') as f:
            typos = json.loads(f.read().decode('utf-8'))
    elif ext == ".gz":
        with gzip.open(file_path, 'r') as f:
            typos = json.loads(f.read().decode('utf-8'))
    elif ext == ".json":
        with open(file_path, 'r') as f:
            typos = json.load(f)
    else:
        typos = {}

    return typos

