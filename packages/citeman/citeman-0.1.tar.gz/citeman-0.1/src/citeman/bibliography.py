import os
from bibtexparser.entrypoint import parse_file, write_file
from bibtexparser.library import Library

def setup():
    bib = 'bibliography.bib'
    if not os.path.exists(bib):
        # Create the file if it doesn't exist
        with open(bib, 'a') as file:
            pass
        return Library()

    # Read the file into a library object
    return parse_file(bib)
    
def write(library):
    bib = 'bibliography.bib'
    write_file(bib, library)