## This program takes in the indexstore created by indexer.py and a cacm query
#  as argument and retrieves document IDs in the index that are determined to be
#  relevant to the query

from global_statistics import GSFILE
from query             import queries
from result_set        import ResultSet
from bm25              import BM25
from qlm               import QLM
from tfidf             import TFIDF
from proximity_model   import ProximityModel
from bm25_relvence     import BM25_R

import argparse
import os
from   argparse import RawTextHelpFormatter

## Globals #####################################################################
# Print to terminal about what the program is doing
# this is set by input to the program
verbose = False

## Help strings ################################################################

program_help = '''

    searcher.py takes in as argument, the path to the indexstore created by
    indexer.py and a query file and prints to the terminal a list of results
    describing documents that are determined to be relevant by the retreival model
    of user choice

    Argument 1: indexstore - Path to the folder, where the index is created by
                             indexer.py. This is the output folder of indexer.py

    Argument 2: queryfile  - Path to query file

    Argument 3: model      - Retrieval model to use
                             "bm25" to use BM25 retreival model (bm25.py)
                             "tfidf" to use the tfidf model (tfidf.py)
                             "qlm"   to use the QLM model (qlm.py)
                             "prf" to run PRF (./bm25_relvence.py)
                             "proximity" to use the proximity model (proximity_model.py)

    Argument 4: resultfile - Path to resultfile to store TREC format result
                             strings. If the resultfile already exists, it is
                             deleted. This argument is optional.

    Argument 5: desc       - A description of the run. This carries the same meaning as
                             the last term in Trec Eval strings.

    Argument 6: verbose    - Print progress of the program to stdout.
                             This argument is optional

    EXAMPLES:

        # Search using bm25
        python searcher.py --indexstore=./cacm.index --queryfile=queries.txt --model=bm25 --resultfile=results.bm25.txt  --verbose
        # Search using proximity model
        python searcher.py --indexstore=./cacm.index --queryfile=queries.txt --model=proximity --resultfile=results.bm25.txt  --verbose
  '''

indexstore_help = '''
    Path to the folder, where the index is created by indexer.py. This is
    the output folder of indexer.py
    '''

queryfile_help = '''
    Path to file containing queries
    '''

model_help = '''
    Retrieval model to use
        "bm25" to use BM25 retreival model (bm25.py)
        "proximity" to use the proximity model (proximity_model.py)
    '''

resultfile_help = '''
    Path to a file to store the TREC format result strings. If a result file
    already exists, it is deleted. This argument is optional
    '''

desc_help = '''
    A description of the run. This carries the same meaning as the last term in
    Trec Eval strings.
    '''

verbose_help = '''
    Print progress of the program to stdout. This argument is optional
    '''

## Setup argument parser #######################################################

argparser = argparse.ArgumentParser(description = program_help,
                                    formatter_class = RawTextHelpFormatter)

argparser.add_argument("--indexstore",
                       metavar  = "is",
                       required = True,
                       type     = str,
                       help     = indexstore_help)

argparser.add_argument("--queryfile",
                       metavar  = "qf",
                       required = True,
                       type     = str,
                       help     = queryfile_help)

argparser.add_argument("--model",
                       metavar  = "m",
                       required = True,
                       type     = str,
                       help     = model_help)

argparser.add_argument("--resultfile",
                       metavar  = "rf",
                       type     = str,
                       default  = "",
                       help     = resultfile_help)

argparser.add_argument("--desc",
                       metavar  = "d",
                       type     = str,
                       default  = "",
                       help     = desc_help)

argparser.add_argument("--verbose",
                       dest     = 'verbose',
                       action   = 'store_true',
                       help     = verbose_help)

## Utilities ###################################################################

##
# GIVEN: a list of ResultSet
# Print the results to stdout
#
def print_resultsets(resultsets):

    print "+++++++++++++++++++++++++++++ RESULT SETS ++++++++++++++++++++++++++"

    for resultset in resultsets:
        resultset.print_resultset()

    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

##
# GIVEN: a list of ResultSet, resultsets, and path to a non-existant file,
#        resultfile and a description of what the result is. e.g. "STOPPED_STEMMED"
# Prints results to the file
def print_to_resultfile(resultsets, resultfile, desc = ""):

    # make sure there is no spaces in description
    desc = desc.replace(" ", "_")

    # open result file
    with open(resultfile, "w+") as rf:
        # for every result set
        for resultset in resultsets:
            # get result string
            resultstrings = resultset.trec_result_strings()
            # for every result string
            for resultstring in resultstrings:
                # write result string
                rf.write(resultstring + "_" + desc + "\n")

## Search ######################################################################

##
# GIVEN: an index store, (output of wiki_indexer.py), and
#        a queryfile with lines of space separated queryid and query, and
#        a string representing a retrieval model to use,
#           "bm25" - Use BM25 (bm25.py)
#           "proximity" - Use proximity model (proximity_model.py)
#
# RETURNS: a list of ResultSet (from result_set.py) where each result set
#          contains information about documents determined to be relevant for
#          a query
#
def search(indexstore, queryfile, model):

    # queries in queryfile -> list of Query (from query.py)
    query_lst = queries(queryfile)

    # wiki_indexer.py creates a global statistics file inside indexstore. Assert
    # that we have it
    assert (os.path.exists(os.path.join(indexstore, GSFILE)))

    # assert that model is recognized
    assert (model == "bm25"     or \
            model == "tfidf"    or \
            model == "qlm"      or \
            model == "prf"      or \
            model == "proximity")

    # retrieval model
    rm = None

    if (model == "bm25"):
        # Setup BM25
        rm = BM25(indexstore, os.path.join(indexstore, GSFILE))

    elif (model == "tfidf"):
        # Setup tfidf
        rm = TFIDF(indexstore, os.path.join(indexstore, GSFILE))

    elif(model == "qlm"):
        # Setup QLM
        rm = QLM(indexstore, os.path.join(indexstore, GSFILE))

    elif(model == "prf"):
        # Setup bm25_rel
        rm = BM25_R(indexstore, os.path.join(indexstore, GSFILE))

    elif (model == "proximity"):
        # Set up proximity model
        rm = ProximityModel(indexstore, os.path.join(indexstore, GSFILE))

    # search using retrieval model
    return rm.search(query_lst)

## Main ########################################################################

## Get arguments
args = vars(argparser.parse_args())

## Inputs
indexstore = args['indexstore']
queryfile  = args['queryfile']
model      = args['model']
resultfile = args['resultfile']
desc       = args['desc']
verbose    = args['verbose']

## Input check
if (not os.path.exists(indexstore)):
    print "FATAL: Cannot find indexstore, ", indexstore
    exit (-1)
if (not os.path.exists(queryfile)):
    print "FATAL: Cannot find queryfile, ", queryfile
    exit (-1)
# Do we recognize the retrieval model
if (model != "bm25"     and \
    model != "tfidf"    and \
    model != "qlm"      and \
    model != "prf"      and \
    model != "proximity"):

    print model
    print "FATAL: Unrecognized retrieval model"
    exit(-1)
# if a resultfile already exists. delete it
if (resultfile != "" and os.path.exists(resultfile)):
    print "WARNING: Deleting existing resultfile"
    os.remove(resultfile)

# Get list of resultset. 1 resultset for 1 query
resultsets = search(indexstore, queryfile, model)

# Print results to resultfile
if resultfile != "":
    print_to_resultfile(resultsets, resultfile, desc)
