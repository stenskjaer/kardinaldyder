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
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


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
        print('Read %s' % filename)
        f.close()
        return(s)

def set_filename(filename=False):
    """ Defines the filename of the tex output file and create dir if necessary.

    Keyword Arguments:
    filename -- Optional input file.
    """

    directory = settings.output_folder
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not filename:
        return os.path.join(directory, settings.output_name + settings.output_addon + '.tex')
    else:
        return filename

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

def create_occurrence_lists(terms, exceptions, string):
    """ Take lists of occurrences and exceptions as strings and search
    the string. Remove exceptions and nest lists according to search term. 

    Keyword Arguments:
    terms      -- List containing strings of search terms
    exceptions -- List containing strings of exceptions
    string     -- The string to be searched.
    """

    occurrences = []
    for terms, exceptions in zip(terms, exceptions):
        # Tokenize the strings
        needles = tokenize_string(terms)
        exception_list = tokenize_string(exceptions)
        log.debug('Tokenized needles: {}'.format(needles))
        log.debug('Tokenized exceptions: {}'.format(exception_list))

        # Position words and exceptions
        needle_positions = position_words(needles, string)
        exception_positions = position_words(exception_list, string)
        log.debug('Needle positions: {}'.format(needle_positions))
        log.debug('Exception positions: {}'.format(exception_positions))

        # Remove the exceptions and put into list
        occurrences.append(remove_exceptions(needle_positions,
                                             exception_positions))

    log.debug('List of occurrences: {}'.format(occurrences))
    return occurrences

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

    return [word for word in string.split(', ')]

def book_separators(string):
    """ Recursive search for book starts and return list of tuples
    containing start position and content of result. 

    Keyword Arguments:
    string -- input string

    """
    
    pattern = "(\[[0-9]{1,2}\]\s\{.*?\})"
    matches = recursive_search(pattern, string)
    return [(match.start(), match.group()) for match in matches]

def relative_positions(positions, string):
    """ Create list with positions relative to diagram size and granularity. Used in output rendition.
    Keyword Arguments:
    positions   -- result of position_words, list of absolute positions
    width       -- width-factor of relative size
    granularity -- (default 4). Detail level of relative locations
    """

    # Set vars
    string_length = len(string)
    width	= settings.width_factor
    granularity = settings.granularity

    return [round(position[0] / string_length * width, granularity) for position in positions]

def calculations(occurrences, string):
    """ Perform statistical calculations on contant. Return dictionary
    of keys and values. 
    Keyword Arguments:
    string -- The content string
    """
    # word_count
    pattern = re.compile(r'[^\{]\b[^\s]+\b', re.UNICODE) # Matches space separated unities excluding {enclosed blocks}
    word_count = len(re.findall(pattern, string))
    
    # List of observed distances between occurences
    observed_distances = []
    for i, val in enumerate(occurrences):
        if i is 0:
            observed_distances.append(val[0])
            log.debug('Occurrence {0} distance: '.format(i))
        else:
            observed_distances.append(val[0] - occurrences[i-1][0])
            log.debug('Occurrence {0} distance: '.format(i))
    observed_distances.append(len(string) - occurrences[-1][0])

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
        'word_count' : word_count,
        'mean' : expected_distance,
        'std_dev' : standard_deviation,
        'var_coef' : var_coefficient
    }
    
    return results

def separate_terms(terms):
    """ Sort names, terms and exceptions into separate lists
    Keyword Arguments:
    terms -- content of settings.terms correctly formatted.
    """

    names = [term[0] for term in terms]
    tokens = [term[1] for term in terms]
    exceptions = [term[2] for term in terms]

    return names, tokens, exceptions

def prepare_data(occurrences_list, names, string):
    """ Parse the (possibly nested) list of occurrences
    Keyword Arguments:
    occurences -- output of the occurences function
    string     -- 
    """
    # Calculate relative positions of books
    books = relative_positions(book_separators(string), string)
    
    bars = []
    for occurrences, name in zip(occurrences_list, names):
        # Get variation coefficient from calculations output
        var_coef = calculations(occurrences, string).get('var_coef')

        # Calculate relative positions of occurences
        occurrences = relative_positions(occurrences, string)

        # Finish the dictionary
        bars.append(dict(
            occurrences = occurrences,
            var = round(var_coef, 2),
            name = name,
        ))


    return bars, books

def render_tex(output_argument,
               output_filename,
               diagram_variables,
               bar_variables,
               book_variables): 
    """ Render diagram grid in tex format.

    Keyword Arguments:
    output_arguments  -- The argument passed from command line.
    diagram_variables -- Variables setting up the diagram, from settings. 
    bar_variables     -- The data governing the individual bars in diagram.
    book_variables    -- The data governing the location of book marks.
    """
    
    from jinja2 import Environment, FileSystemLoader

    env = Environment(
        loader=FileSystemLoader('templates'),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template('diagram.tex')
    
    output = template.render(
        diagram=diagram_variables,
        bars=bar_variables,
        books=book_variables,
    )

    print(output_filename)
    if output_argument == str('file'):
        with open(output_filename, 'wt') as f:
            f.write(output)
    elif output_argument == str('both'):
        with open(output_filename, 'wt') as f:
            f.write(output)
        print(output)
    elif output_argument == str('shell'):
        print(output)
    else:
        logging.ERROR('Invalid output argument given. Cannot render output.')

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

    parser.add_argument('--tex', '-t',
                        help='Create output to LaTeX file with TikZ formatted diagram. Choose whether it goes to shell, file or both. Default = shell.',
                        action='store',
                        choices=['shell', 'file', 'both'],
                        default='shell')

    args = parser.parse_args()

    string = open_file(args.file)

    names, terms, exceptions = separate_terms(settings.terms)

    occurrences = create_occurrence_lists(terms, exceptions, string)

    output_data = prepare_data(occurrences, names, string)

    render_tex(args.tex,
               set_filename(args.output),
               settings.diagram_variables,
               *output_data)

    
    
if __name__ == "__main__":
    main()
