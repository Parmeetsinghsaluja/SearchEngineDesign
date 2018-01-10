# Generate a clean, text processed corpus

from corpus_rw       import CorpusRW, corpus_filename
from docid_mapper    import DocIDMapper

import os.path
import shutil
import argparse
import sys
from argparse import RawTextHelpFormatter

## Globals #####################################################################

# Print to terminal about what the program is doing
# this is set by input to the program
verbose = False

## Help strings ################################################################

program_help = '''

    corpus_stem.py builds a clean corpus folder, given a path to cacm_stem.txt file

    Argument 1: cacmstemfile - Path to cacm_stem.txt

    Argument 2: corpusstore - Output folder name where the corpus files are to
                              be stored. In case some other folder exists of the
                              same name, then it is deleted.

    Argument 3: verbose     - Print progress of the program to the stdout. This
                              argument is optional.

    EXAMPLES:

        python corpus.py --cacmstemfile="./cacm/cacm_stem.txt" --corpusstore="./corpusstore --verbose"

    '''

cacmstemfile_help = '''
    Path to cacm_stem.txt
    '''

corpusstore_help = '''
    Output folder name where the corpus files are to be stored. In case some
    other folder exists of the same name, then it is deleted. '''

verbose_help = '''
    Print progress of the program to the stdout. This argument is optional.
    '''

## Setup argument parser #######################################################

argparser = argparse.ArgumentParser(description = program_help,
                                    formatter_class = RawTextHelpFormatter)

argparser.add_argument("--cacmstemfile",
                       metavar  = "csf",
                       required = True,
                       type     = str,
                       help     = cacmstemfile_help)

argparser.add_argument("--corpusstore",
                       metavar  = "o",
                       required = True,
                       type     = str,
                       help     = corpusstore_help)

argparser.add_argument("--verbose",
                       dest    = 'verbose',
                       action  = 'store_true',
                       help    = verbose_help)

## Utitilies ###################################################################

# Prints text only if verbose flag is on
def print_verbose(txt):
    if verbose:
        print txt

# Get the document IDs of cacm files from cacm_stem.txt
def document_nums (cacmstemfile):

    assert (os.path.exists(cacmstemfile))

    docids = []

    # read cacm lines
    lines = []
    with open(cacmstemfile, "r") as csf:
        lines = csf.readlines()

    # scan every line and extract docid, if that line is talking about docid
    for line in lines:

        # strip line
        line = line.strip()

        # docid lines start with '#'
        if (line.startswith("#")):
            docids.append(int(line.split('#')[1]))

    # return docids
    return docids

# Given the path to a cacm_stem.txt file and a document id
# return the contents associated with the document number as mentioned in the
# cacm_stem.txt file
def document_content(cacmstemfile, docno):

    assert (os.path.exists(cacmstemfile))

    # read the stem file into lines
    lines = []
    with open(cacmstemfile, "r") as csf:
        lines = csf.readlines()

    # Markers in cacm_stem.txt. that bound the required document's content
    doc_start_marker = "# " + str(docno + 0)
    doc_end_marker   = "# " + str(docno + 1)

    # add line to contents only if this is true
    add_content_line = False

    content_lines = []

    # scan every line and add all lines right after #docno to #docno + 1 to
    # conten. Example, if we are searching for docid 2's content, add all lines
    # right after "#2" and untill "#3"
    for line in lines:

        # strip line
        line = line.strip().encode('ascii', 'ignore')

        if (line == doc_end_marker):
            add_content_line = False

        if (add_content_line):
            content_lines.append(line)

        if (line == doc_start_marker):
            add_content_line = True

    # return content
    return " \n".join(content_lines)

# Given path to the cacm_stem.txt file,
# Returns a dictionary keyed by document ids and whose values is the content
# string of the corresponding document
def document_contents(cacmstemfile):

    assert (os.path.exists(cacmstemfile))

    doccontents = {}

    # read cacmstemfile contents into lines
    lines = []
    with open(cacmstemfile, "r") as f:
        lines = f.readlines()

    # current docid
    docid = -1

    for line in lines:
        # clean line
        line = line.strip()

        # does the line mention docid ?
        if (line.startswith("#")):
            # update current docid;
            docid = int(line.split('#')[1])

            # initialize contents for this docid
            doccontents[docid] = ""

        if not line.startswith("#"):
            assert (docid != -1)
            assert (doccontents.get(docid) is not None)
            doccontents[docid] = doccontents[docid] + " \n " + line

    return doccontents

## Main functions ##############################################################

# GIVEN path the cacm_stem.txt and
#       where to store the generated cleaned up corpus
# Generate one corpus file for each cacm stemmed document as mentioned in the
# cacm_stem.txt
def corpus(cacmstemfile, corpusstore):

    assert (os.path.exists(cacmstemfile))

    # get doc contents, dictionary
    doccontents = document_contents(cacmstemfile)

    # for each document number, generate a corpus file
    for docid in doccontents:

        # fake document name
        docname = "CACM_" + str(docid)

        print_verbose("doc -> corpus ( "    + \
                      str(docid)            + \
                      "/"                   + \
                      str(len(doccontents)) + \
                      " ) : "               + \
                      docname)

        # get content of the document
        content = doccontents[docid]

        # Make sure we have only " " to separate words
        words = content.split(' ')
        words = map(lambda w: w.strip(), words)
        words = filter(lambda w: w != "", words)

        # rebuild content from words
        content = " ".join(words)

        # get a corpusfile name from a descriptive document name
        corpus_fname = corpus_filename(docname)

        # create the corpus and store it
        CorpusRW().store_corpus(content, corpus_fname, corpusstore)

    # Create a docID mapper
    docid_map = {}

    # Create a documentID and file path map and store it
    for docid in doccontents:

        # Get document path; This is cacmstemfile
        d_path = cacmstemfile

        # fake document name
        docname = "CACM_" + str(docid)

        # Get corpus file name.
        corpus_fname = corpus_filename(docname);

        # Get corpus file path
        c_path       = os.path.join(corpusstore, corpus_fname)

        # Record map
        docid_map[docid] = (c_path, d_path)

    # Write docid map
    DocIDMapper().store(corpusstore, docid_map)

## Main ########################################################################

## Get arguments
args = vars(argparser.parse_args())

## Inputs
cacmstemfile = args['cacmstemfile']
corpusstore  = args['corpusstore']
verbose      = args['verbose']

# Check if cacmstemfile is present
if (not os.path.exists(cacmstemfile)):
    print "FATAL: Cannot find ", cacmstemfile
    exit(-1)

# Check corpusstore
if (os.path.exists(corpusstore)):
    print "WARNING: Deleting existing corpusstore"
    shutil.rmtree(corpusstore)
# Create corpusstore
os.makedirs(corpusstore)

# Get to work now !! :D :D
corpus(cacmstemfile, corpusstore)
