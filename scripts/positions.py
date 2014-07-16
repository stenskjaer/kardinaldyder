#!/usr/bin/python
# -*- coding: utf-8 -*-

import settings
import os, sys

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
    
    if not filename:
        if settings.corpus_subdir:
            filename = os.path.join(corpus_dir, corpus_subdir, author, filename_prefix+filename_addon)
        else:
            filename = os.path.join(corpus_dir, author, filename_prefix+filename_addon)

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
    
def main():
    """ Main function

    Initiate argument parser
    """


    
    open_file()
    

if __name__ == "__main__":
    main()
