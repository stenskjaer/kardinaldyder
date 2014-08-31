#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unicodedata
import os, sys, argparse, codecs, subprocess, shutil
import settings

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

        return(s)

def file_list(question):
    """Determine whether input is file or directory and load content
    into list.

    Keyword Arguments: question -- string that is either a file or
    directory.

    """

    if os.path.isdir(question):
        file_list = []
        for dirname, dirnames, filenames in os.walk(question):
            for filename in filenames:
                file_list.append(os.path.join(dirname, filename))
        return(file_list)
    elif os.path.isfile(question):
        return([question])
    else:
        print('This is odd -- you didn\'t input neither a file nor a dir.'
              'I quit!')



def strip_accents(string):
    """Remove accents from string of greek characters.

    Keyword Arguments: string -- unicode encoded string

    """

    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')    



def main():
    """Main function. 

    Initiate argument parser and run appropriate
    functions.
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Pre-process text files for ')
    parser.add_argument('input',
                        help='The folder or file to be parsed.')
    parser.add_argument('output', nargs='?',
                        help='The folder where the processed corpus files will be stored. If none is given, the file will be placed in the current working directory.',
                        default=os.getcwd())
    parser.add_argument('--beta-code', '-b',
                        help='Is the file in beta-code? In that case it should be converted. Requires tlgu. Default = False',
                        action='store_true')
    parser.add_argument('--print', '-p',
                        help='Output the result to shell? Default = False.',
                        action='store_true')
    parser.add_argument('--acccents', '-a',
                        help='Strip accents. Default = False.',
                        action='store_true')
    parser.add_argument('--whitespace', '-w',
                        help='Remove excessive whitespace. Default = False.',
                        action='store_true')
    parser.add_argument('--linebreaks', '-i',
                        help='Remove all linebreaks. Default = False.',
                        action='store_true')
    parser.add_argument('--merge-files', '-m',
                        help='Merge the files into one corpus-file. Default = False.',
                        action='store_true')
    parser.add_argument('--log', '-l',
                        help='Set the log level (output to shell). Default = INFO.',
                        default='INFO')

    # Parse command line arguments
    args = parser.parse_args()

    # Process the file(s)
    process_files(args)

if __name__ == "__main__":
    main()
