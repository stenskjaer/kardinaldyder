#!/usr/bin/python
# -*- coding: utf-8 -*-

import settings
import os
import sys
import argparse
import string
import re


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
        f = open(filename)
        s = f.read()
    except IOError as e:
        print "I/O error ({0}): {1}".format(e.errno, e.strerror)
    except:
        print "Unexpected error:", sys.exc_info()[0]

    s = s.decode('utf-8')
    # Return the string
    return s

def position_words(needles, haystack):
    """
    Position search terms in list with nested list of begin and end of word.
    
    Keyword Arguments:
    needle   -- search term
    haystack -- string to be searched

    """
    results = []
    for needle in needles:
        matches = recursive_search(needle, haystack)
        for match in matches:
            word = match.group(0)
            results.append([
                match.start(),                                      
                match.start() + len(word),
                word.encode('utf-8')
            ]) 


    return results

def recursive_search(needle, haystack):
    """ Perform recursive search of items from list. Returns list of positions.
    Keyword Arguments:
    needle   -- 
    haystack -- 
    """

    pattern = re.compile(needle + '\w+', re.UNICODE)                # Use needle and rest until first non-word char
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

    return [word.decode('utf-8') for word in string.split(',')]

def main():
    """ Main function

    Initiate argument parser
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Position occurences of search word in file and produce latex output. Default settings in settings.py-file')
    parser.add_argument('file', nargs='?',
                        help='Optional. The file to be parsed. If none is given, the settings-file is used.')
    parser.add_argument('--compilation', '-c',
                        help='Compile the produced .tex-files? Boolean. Default = False',
                        action='store_true',
                        default=False)
    args = parser.parse_args()

    # Load terms and exceptions into list, decoded
    tokens = tokenize_string(settings.terms)
    exceptions = tokenize_string(settings.exceptions)
    
    positions = position_words(tokens, open_file(args.file))
    exceptions = position_words(exceptions, open_file(args.file)) 

    print exceptions

    # Need to make list of exceptions too.
    positions = remove_exceptions(positions, exceptions)

    print positions

if __name__ == "__main__":
    main()
