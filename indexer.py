# This program creates an inverted index from the folder containing corpus files

from text_processing   import word_ngrams
from global_statistics import GlobalStatistics, GSFILE
from index             import *
from corpus_rw         import is_corpus_file, CorpusRW
from docid_mapper      import DocIDMapper

import argparse
from   argparse import RawTextHelpFormatter
import os
import shutil

## Globals #####################################################################
# Print to terminal about what the program is doing
# this is set by input to the program
verbose = False

## Help strings ################################################################

program_help = '''

    indexer.py constructs an index file (.idx) that indexes the terms in
    all corpus files in a folder (corpusstore)

    Argument 1: corpusstore - Folder where the corpus files are stored

    Argument 2: indexstore  - Folder where the output index file along with
                              other information such as global statistics is
                              stored

    Argument 3: ngrams      - Number of ngrams to index. Defaults to 1

    Argument 4: verbose     - Print progress of the program to the stdout.
                              This argument is optional.

    EXAMPLES:

        python indexer.py --corpusstore=./cacm.corpus --indexstore=cacm.index --ngrams=1 --verbose
    '''

corpusstore_help = '''
    Folder where the corpus files are stored
    '''

indexstore_help = '''
    Folder where the output index file along with other information such as
    global statistics is stored
    '''

ngrams_help = '''
    Number of ngrams to index. defaults to 1
    '''

verbose_help = '''
    Print progress of the program to the stdout. This argument is optional.
    '''
## Setup argument parser #######################################################

argparser = argparse.ArgumentParser(description = program_help,
                                    formatter_class = RawTextHelpFormatter)

argparser.add_argument("--corpusstore",
                       metavar  = "cs",
                       required = True,
                       type     = str,
                       help     = corpusstore_help)

argparser.add_argument("--indexstore",
                       metavar  = "o",
                       required = True,
                       type     = str,
                       help     = indexstore_help)

argparser.add_argument("--ngrams",
                       metavar = "n",
                       default = 1,
                       type    = int,
                       help    = ngrams_help)

argparser.add_argument("--verbose",
                       dest    = 'verbose',
                       action  = 'store_true',
                       help    = verbose_help)

## Utilities ##################################################################

# String -> Print output to terminal
# Given a string, print it to terminal if verbose is set in input arguments
def print_verbose(s):
    if verbose:
        print (s)

# Store global statistics
# Given the path to a folder where to store the global stats information and
#       the #terms per document dictionary whose (key, value) pair is
#       (docid, #terms in doc)
#
# Store all global statistics information to the global statistics file
#
def store_global_stats(indexstore, terms_per_document):

    # Total number of docs indexed
    N = len(terms_per_document)

    # Corpus size
    cs = reduce(lambda cs, doc_tf: cs + doc_tf[1], \
                terms_per_document.items(),        \
                0)

    # Corpus size is the sum of all document lenghts. avdl is cs/N
    # Average doclength
    avdl = (float(cs) / float(N))

    # doclengths is nothing be terms_per_document

    # create global stats
    gs = GlobalStatistics(os.path.join(indexstore, GSFILE))
    # load global stats
    gs.load(N, cs, avdl, terms_per_document)
    # store stats
    gs.write()

    return

## Indexer functions ###########################################################

# given a folder where corpus files are stored (created by corpus.py),
#       a folder where the constructed index should be stored,
#       the number of words consisting a term,
# then create the output index file
def indexer(corpusstore, indexstore, n):

    # create an empty index
    invidx = Index(indexstore)

    # global statistics information
    terms_per_document = {}

    # docid mapper; Maps documentID to a
    # tuple of (cacm_corpus_file_path, cacm_document_path)
    docid_map = DocIDMapper().read(corpusstore)

    for docid in docid_map:

        # Path to the corpus file of this document id
        corpusfpath = DocIDMapper().corpusfpath(docid, docid_map)

        print_verbose("Adding document" + " (" +  str(docid) + "/" + \
                     str(len(docid_map)) + ") " + corpusfpath + \
                      " to index")

        # get corpus file
        content = CorpusRW().corpus_content(corpusfpath)

        # assert that content of the corpus file has no whitespace other than '\n'
        assert(all(map(lambda w: w.strip() == w, content.split(" "))))

        # get word ngrams
        terms = word_ngrams(content, n)

        # assert word ngrams
        assert(all(map(lambda ng: len(ng.split(" ")) == n, terms)))

        # store global statistic, terms_per_document
        terms_per_document[docid] = len(terms)

        # store terms
        for posidx in range(0, len(terms)):
            # term and term position
            term = terms[posidx]
            tpos = posidx
            invidx.update(term, tpos, docid)

    # store index to a file inside corpusstore
    invidx.store()

    # Copy the document map file from corpusstore to indexstore
    DocIDMapper().copy_docidmapper(corpusstore, indexstore)

    # store global statistics
    store_global_stats(indexstore, terms_per_document)

    print "\nSuccess : Index created - ", indexstore


## Main ########################################################################

## Get arguments
args = vars(argparser.parse_args())

## Inputs
corpusstore = args['corpusstore']
indexstore  = args['indexstore']
ngrams      = args['ngrams']
verbose     = args['verbose']

## Input check
if (not os.path.exists(corpusstore)):
    print ("FATAL: Cannot find file ", corpusstore)
    exit(-1)
if (ngrams <= 0):
    print ("FATAL: ngrams should be > 0")
    exit(-1)

## Delete any indexstore previously present
if (os.path.exists(indexstore)):
    print ("DELETING EXISTING INDEXSTORE  ", indexstore)
    shutil.rmtree(indexstore)

# Create index
indexer(corpusstore, indexstore, ngrams)

# print the index
#Index(indexfile).print_index()
