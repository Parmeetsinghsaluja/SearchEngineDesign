# This file contains functions to parse the cacm corpus

import os
from bs4 import BeautifulSoup

## Globals #####################################################################

CACM_FILE_PREFIX = "CACM"
CACM_FILE_SUFFIX = ".html"

################################################################################

# Give the name of a file
# Returns true iff the file is a CACM document file
def is_cacm_doc(fname):

    return fname.startswith(CACM_FILE_PREFIX) and fname.endswith(CACM_FILE_SUFFIX);

# Given the name of a cacm filename of format CACM-XXXX.html
# Returns the documentID from the file name
def cacm_docid(cacm_fname):

    # hyphen split
    hyphen_parts = cacm_fname.split("-")

    # must be 2 hyphen parts
    assert (len(hyphen_parts) == 2)
    # assert first part is "CACM"
    assert (hyphen_parts[0] == "CACM")

    # split second part by "."
    dot_parts = hyphen_parts[1].split(".")

    # there must be 2 parts
    assert (len(dot_parts) == 2)
    assert (dot_parts[1] == "html")

    # return the first dot part as int
    return int(dot_parts[0])


# Given the path to a cacm document
# Returns the content of the cacm document
def cacm_content(fpath):

    assert (os.path.exists(fpath))
    assert (is_cacm_doc(os.path.basename(fpath)))

    # soup the html cacm doc
    with open(fpath, "r") as cacmf:
        soup = BeautifulSoup(cacmf, 'html.parser')

    # get only the contents of <pre> tag
    pres  = soup.find_all('pre')
    assert (len(pres) == 1)

    # return content of pre
    return pres[0].text.encode('ascii', 'ignore')

################################################################################
