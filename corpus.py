# Generate a clean, text processed corpus

from text_processing import process_text
from cacm_parser     import is_cacm_doc, cacm_docid, cacm_content
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

    corpus.py builds a clean corpus folder, given a folder containing documents
    to be cleaned

    Argument 1: docstore    - Path to the folder containing documents

    Argument 2: corpusstore - Output folder name where the corpus files are to
                              be stored. In case some other folder exists of the
                              same name, then it is deleted.

    Argument 3: stopfile    - Path to the stoplist file. Every term in the stoplist
                              must be separated by the STOPFILE_DELIMITER (in stopping.py)

    Argument 4: verbose     - Print progress of the program to the stdout. This
                              argument is optional.

    EXAMPLES:

        # default execution, with casefolding and punctuation handling
        python corpus.py --docstore="./cacm/cacm_corpus" --corpusstore="./corpusstore --stopfile=./cacm/common_words --verbose"

    '''

docstore_help = '''
    Path to the folder containing the documents to be made into corpus'''

corpusstore_help = '''
    Output folder name where the corpus files are to be stored. In case some
    other folder exists of the same name, then it is deleted. '''

stopfile_help = '''
    Path to the stoplist file. Every word in the stoplist must be separated by
    the STOPFILE_DELIMITER (refer to text_processing.py)
    '''

verbose_help = '''
    Print progress of the program to the stdout. This argument is optional.
    '''

## Setup argument parser #######################################################

argparser = argparse.ArgumentParser(description = program_help,
                                    formatter_class = RawTextHelpFormatter)

argparser.add_argument("--docstore",
                       metavar  = "ds",
                       required = True,
                       type     = str,
                       help     = docstore_help)

argparser.add_argument("--corpusstore",
                       metavar  = "o",
                       required = True,
                       type     = str,
                       help     = corpusstore_help)

argparser.add_argument("--stopfile",
                       metavar = "s",
                       default = "",
                       type    = str,
                       help    = stopfile_help)

argparser.add_argument("--verbose",
                       dest    = 'verbose',
                       action  = 'store_true',
                       help    = verbose_help)

## Utitilies ###################################################################

# Prints text only if verbose flag is on
def print_verbose(txt):
    if verbose:
        print txt

## Main functions ##############################################################

# GIVEN paths to where cacm documents, to clean up, are stored and
#       where to store the generated cleaned up corpus from the cacm documents, and
#       the path to the stopfile (optional)
# Generate one corpus file for each cacm document document
def corpus(docstore,
           corpusstore,
           stopfile    = "",
           casefold    = True,
           handle_punc = True):

    # get all files in docstore
    cacm_docs = filter(lambda f: is_cacm_doc(f), os.listdir(docstore))

    # Sort cacm_docs by file name
    cacm_docs.sort()

    for doc in cacm_docs:

        print_verbose("doc -> corpus ( "            + \
                      str(cacm_docs.index(doc) + 1) + \
                      "/"                           + \
                      str(len(cacm_docs))           + \
                      " ) : "                       + \
                      doc)

        d_path = os.path.join(docstore, doc)

        assert(os.path.exists(d_path))

        # get the content of the cacm document
        content = cacm_content(d_path)

        # process text (punctuations and casefolding) and by default remove all
        # extraneous spaces
        content = process_text(content, stopfile)

        # Get apt corpus file name
        corpus_fname = corpus_filename(doc);

        # create the corpus and store it
        CorpusRW().store_corpus(content, corpus_fname, corpusstore)

    # Create a docID mapper
    docid_map = {}

    # Create a documentID and file path map and store it
    for doc in cacm_docs:

        # Get document path
        d_path = os.path.join(docstore, doc)

        # Get docid
        d_docid = cacm_docid(doc)

        # Get corpus file name.
        corpus_fname = corpus_filename(doc);
        # Get corpus file path
        c_path       = os.path.join(corpusstore, corpus_fname)

        # Record map
        docid_map[d_docid] = (c_path, d_path)

    # Write docid map
    DocIDMapper().store(corpusstore, docid_map)

## Main ########################################################################

## Get arguments
args = vars(argparser.parse_args())

## Inputs
docstore           = args['docstore']
corpusstore        = args['corpusstore']
stopfile           = args['stopfile']
verbose            = args['verbose']

# Check if docstore is present
if (not os.path.isdir(docstore)):
    print "FATAL: Cannot find ", docstore,
    exit(-1)

# Check if stopfile, if given, is present
if (stopfile != "" and (not os.path.exists(stopfile))):
    print "FATAL: Cannot find stopfile ", stopfile
    exit(-1)

# Check corpusstore
if (os.path.exists(corpusstore)):
    print "WARNING: Deleting existing corpusstore"
    shutil.rmtree(corpusstore)
# Create corpusstore
os.makedirs(corpusstore)

# Get to work now !! :D :D
corpus(docstore, corpusstore, stopfile)
