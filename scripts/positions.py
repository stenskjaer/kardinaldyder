import settings
import os

def init_file(filename):
    """
    Open file and load content into string.
    Set other initial vars
    """

    # Load vars from settings
    corpus_dir 		= settings.corpus_dir
    corpus_subdir 	= settings.corpus_subdir
    author 		= settings.author
    filename_addon	= settings.filename_addon

    if not filename:
        if settings.corpus_subdir:
            filename = os.path.join(corpus_dir, corpus_subdir, author, filename_addon)
        else:
            filename = os.path.join(corpus_dir, author, author, filename_addon)
