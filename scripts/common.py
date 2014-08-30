#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import settings
import os, sys, logging, codecs


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
    # If filename_prefix is not set, use author
    filename_prefix	= settings.filename_prefix if settings.filename_prefix else author 
    
    # If filename is not set from command line parameters, use settings
    if not filename:
        if settings.corpus_subdir:
            filename = os.path.join(corpus_dir, corpus_subdir, filename_prefix+filename_addon)
        else:
            filename = os.path.join(corpus_dir, author, filename_prefix+filename_addon)

    # Try opening the file
    try:
        f = codecs.open(filename, 'rb','utf8')
        s = f.read()
    except IOError as err:
        print('Cannot open {}'.format(err))
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        f.close()

        logging.info('String succesfully read')
        return(s)
