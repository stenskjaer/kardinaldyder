#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unicodedata
import os, sys, argparse, codecs, subprocess, shutil
import settings

def open_file(filename, encoding='utf8'):
    """
    Open file and load content into string.
    
    Returns the content as decoded string.
    """

    # Try opening the file
    try:
        f = codecs.open(filename, 'rb', encoding)
        s = f.read()
    except IOError as err:
        print('Cannot open {}'.format(err))
    except:
        print("Unexpected error:", sys.exc_info()[0])
    else:
        f.close()

        return(s)

def content_of_files(question, beta_conversion=False):
    """Determine whether input is file or directory and load content
    into list.
    If enabled, convert beta code via tlgu

    Keyword Arguments: question -- string that is either a file or
    directory.

    """

    # Create the list
    content_list = []

    # If its a dir, I assume it is unicode (folders with beta-encoding
    # are not acepted). Intended to be a folder with output of the
    # tlgu script
    if os.path.isdir(question):
        for dirname, dirnames, filenames in os.walk(question):
            for filename in filenames:
                content_list.append(open_file(os.path.join(dirname, filename)))
        
    # If it is a file, it can either be unicode or beta-code. If
    # cmd-line argument for beta-conversion is true, the convert and
    # return a list, else the list is just the single file.
    elif os.path.isfile(question):
        if beta_conversion is True:
            print('Beta conversion enabled and starting now.')
            content_list = beta_code_convert(question)
        else:
            print('Reading content of single file')
            content_list = [open_file(question)]

    else:
        sys.exit('Specified file or directory does not exist. '
                 'Closing.')

    return(content_list)

def beta_code_convert(file):
    """Convert input var content from beta-code to unicode. Calls the
    tlgu program (see http://tlgu.carmen.gr/). 

    Keyword Arguments:
    content -- string in beta-code encoding
    """

    # Create temp folder for the processing and load content into file
    tempdir_name = 'temp/'
    if not os.path.exists(tempdir_name):
        os.makedirs(tempdir_name)

    # Check if tlgu is on system and convert
    if subprocess.call(['type', 'tlgu']) is 0:
        print('Found tlgu in PATH... Processing')
        subprocess.call(['tlgu', '-W', file, '%soutput' %tempdir_name])
        print('tlgu done with {0}'.format(file))

    elif subprocess.call(['type', './tlgu']) is 0:
        print('Found tlgu in current working dir... Processing')
        subprocess.call(['./tlgu', '-WC', file, '%soutput' %tempdir_name])
        print('tlgu done with {0}'.format(file))

    else:
        sys.exit('tlgu not installed or in current directory. I quit.\n'
                 'Download tlgu from http://tlgu.carmen.gr/, follow '
                 'the installation instructions and put it in your '
                 'PATH or in the currenct working directory of this '
                 'script.')

    # output into var
    output = content_of_files(tempdir_name)

    # remove temp dir
    shutil.rmtree(tempdir_name)
    
    # return output
    return(output)

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
    parser.add_argument('--betacode', '-b',
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
    parser.add_argument('--merge', '-m',
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
