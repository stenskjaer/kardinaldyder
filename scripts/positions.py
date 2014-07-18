#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import division
import settings
import os
import sys
import argparse
import string
import re
import codecs
import math


def open_file(filename=False):
    """
    Open file and load content into string.
    
    Returns the content as decoded string.
    """

    # Load vars from settings
    corpus_dir 		= settings.corpus_dir
    corpus_subdir 	= settings.corpus_subdir
    author 		= settings.author
    filename_addon	= settings.filename_addon
    filename_prefix	= settings.filename_prefix if settings.filename_prefix else author # If filename_prefix is not set, use author
    
    # If filename is not set from command line parameters, use settings
    if not filename:
        if settings.corpus_subdir:
            filename = os.path.join(corpus_dir, corpus_subdir, author, filename_prefix+filename_addon)
        else:
            filename = os.path.join(corpus_dir, author, filename_prefix+filename_addon)

    # Try opening the file
    try:
        f = codecs.open(filename, 'rb','utf8')
        s = f.read()
    except IOError:
        print('cannot open', arg)
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        print(filename, 'has', len(s), 'chars')
        f.close()
        return(s)

def position_words(needles, haystack):
    """
    Position search terms in list with nested list of begin and end of word.
    
    Keyword Arguments:
    needle   -- search term
    haystack -- string to be searched

    """
    results = []
    for needle in needles:
        pattern = r'[^\]](\b%s\w+)' % needle.strip() # exclude ] + (boundary, needle until end of word)
        matches = recursive_search(pattern, haystack)
        for match in matches:
            word = match.group(1)          # exclude leading space with group(1)
            results.append([
                match.start(),             # word start
                match.start() + len(word), # word end 
                word                       # the word
            ]) 

    return sorted(results, key=lambda group: group[0]) 

def recursive_search(needle, haystack):
    """ Perform recursive search of items from list. Returns list of positions.
    Keyword Arguments:
    needle   -- 
    haystack -- 
    """

    pattern = re.compile(needle, re.UNICODE)                        # Use needle and rest until first non-word char
    results = re.finditer(pattern, haystack)                        # Regex iteration on string

    return results


def remove_exceptions(positions, exceptions):
    """
    Find all duplicate positions between exceptions and positions and
    pop from exceptions.

    Keyword Arguments:
    positions  -- list of positions of search terms
    exceptions -- list of positions of exceptions to be removed
    """
    
    return [position for position in positions if position not in exceptions]

def tokenize_string(string):
    """ Converts comma separated string to list. Decoded to utf-8.
    Keyword Arguments:
    string -- input string with tokens separated by commas
    """

    return [word for word in string.split(',')]

def book_separators(string):
    """ Recursive search for book starts and return list of tuples
    containing start position and content of result. 

    Keyword Arguments:
    string -- input string

    """
    
    pattern = "(\[[0-9]{1,2}\]\s\{.*?\})"
    matches = recursive_search(pattern, string)
    return [(match.start(), match.group()) for match in matches]


def relative_positions(positions, width, string_length, granularity=4):
    """ Create list with positions relative to diagram size and granularity. Used in output rendition.
    Keyword Arguments:
    positions   -- result of position_words, list of absolute positions
    width       -- width-factor of relative size
    granularity -- (default 4). Detail level of relative locations
    """

    return [round(position[0] / string_length * width, granularity) for position in positions]

def calculations(string):
    """ Perform statistical calculations on contant. Return dictionary of keys and values.
    Keyword Arguments:
    string -- The content string
    """


    # word_count
    pattern = re.compile(r'[^\{]\b[^\s]+\b', re.UNICODE) # Matches space separated unities excluding {enclosed blocks}
    word_count = len(re.findall(pattern, string))

    # Load terms and exceptions into list, decoded
    tokens = tokenize_string(settings.terms)
    exceptions = tokenize_string(settings.exceptions)

    # Absolute positions
    positions = remove_exceptions(
        position_words(tokens, string),
        position_words(exceptions, string))

    # List of observed distances between occurences
    observed_distances = []
    for i, val in enumerate(positions):
        if i is 0:
            observed_distances.append(val[0])
        else:
            observed_distances.append(val[0] - positions[i-1][0])
    observed_distances.append(len(string) - positions[-1][0])

    # Count of relevant occurences (counting instances of distance)
    count = len(observed_distances)

    # Mean (= expected distance)
    expected_distance = len(string) / count

    # Observation mean: The mean of alle observed distances. sum(obs_dist) / count
    # Needed for variance and variation coefficient
    observation_mean = sum(observed_distances) / count

    # Variance
    obs_minus_mean = [pow(observation - expected_distance, 2) for observation in observed_distances]
    variance = sum(obs_minus_mean) / count 

    # Standard deviation
    standard_deviation = math.sqrt(variance)

    # Variation coefficient (normalized standard deviation)
    var_coefficient = standard_deviation / observation_mean

    results = {
        'Word count' : word_count,
        'Mean (expected distance)' : expected_distance,
        'Standard deviation' : standard_deviation,
        'Variation coefficient' : var_coefficient
    }
    
    return results

def render_output(string):
    """ Render output with Jinja2
    
    """
    
    from jinja2 import Environment, FileSystemLoader

    env = Environment(loader=FileSystemLoader('templates'))
    tex_template = env.get_template('test.tex')
    output_from_parsed_template = tex_template.render(stat_list=calculations(string))
    print(output_from_parsed_template)

    # save
    with open(os.path.join('templates', 'new_file.tex'), 'wt') as f:
        f.write(output_from_parsed_template)

def main():
    """ Main function

    Initiate argument parser
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Position occurences of search word in file and produce latex output. Default settings in settings.py-file')
    parser.add_argument('file', nargs='?',
                        help='Optional. The file to be parsed. If none is given, the settings-file is used.')
    parser.add_argument('--stats', '-s',
                        help='Calculate and output statistics.',
                        action='store_true',
                        default=False)
    parser.add_argument('--plot', '-p',
                        help='Output scatter plot bar with vertical bars.',
                        action='store_true',
                        default=False)
    parser.add_argument('--diagram', '-d',
                        help='Output whole diagram grid and surrounding table.',
                        action='store_true',
                        default=False)
    parser.add_argument('--passages', '-a',
                        help='Output passages with context.',
                        action='store_true',
                        default=False)
    parser.add_argument('--full', '-f',
                        help='Enable all features in output',
                        action='store_true',
                        default=False)
    
    args = parser.parse_args()

    string = open_file(args.file)

    book_separations = book_separators(string)

    calculations(string)

    render_output(string)

if __name__ == "__main__":
    main()
