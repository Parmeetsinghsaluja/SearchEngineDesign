# This prorgram processes the queries in an input file and generates an output
# file in the format "queryidSPACEqueryNEWLINE"

from stopping        import Stopping
from query           import Query, cacm_queries
from text_processing import process_text

import os
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
    Given a cacm queries file, process the queries in the cacm file, store the
    queries in another file in the following format,
     "queryidSPACEqueryNEWLINE"

    This program takes 4 arguments,

    Argument 1 : ipqueryfile : Path to the cacm query file

    Argument 2 : opqueryfile : Path to a file where the output query file must
                               be stored

    Argument 3 : stopfile    : Path to the stopfile. The query will be stopped
                               using the words in the stopfile. [optional]
                               The words in the stopfile must be delimited using
                               STOPFILE_DELIMITER (in stopping.py)

    Argument 4 : verbose     : Print to the terminal, what the program is doing

    Examples:

        python query_processing.py --ipqueryfile=./cacm/cacm.query.txt --opqueryfile=./queries.txt --stopfile=./cacm/common_words --verbose
    '''

ipqueryfile_help = '''
    Path to the cacm query file
    '''

opqueryfile_help = '''
    Path to a file where the output query file must be stored
    '''

stopfile_help = '''
    Path to the stopfile. The query will be stopped using the words in the
    stopfile. [optional]
    The words in the stopfile must be delimited using STOPFILE_DELIMITER (in stopping.py)
    '''

verbose_help = '''
    Print to the terminal, what the program is doing
    '''

## Setup argparse ##############################################################

argparser = argparse.ArgumentParser(description = program_help,
                                    formatter_class = RawTextHelpFormatter)

argparser.add_argument("--ipqueryfile",
                       metavar  = "iq",
                       required = True,
                       type     = str,
                       help     = ipqueryfile_help)

argparser.add_argument("--opqueryfile",
                       metavar  = "oq",
                       required = True,
                       type     = str,
                       help     = opqueryfile_help)

argparser.add_argument("--stopfile",
                       metavar = "s",
                       default = "",
                       type    = str,
                       help    = stopfile_help)

argparser.add_argument("--verbose",
                       dest    = 'verbose',
                       action  = 'store_true',
                       help    = verbose_help)

## Process Queries #############################################################

# Given the path to an input cacm query file
#       the path to where the processes output query file should be stored
#       the path to a stoplist file (optional)
# Process the queries and store the queies in the opqueryfile in the format
# "queryidSPACEqueryNEWLINE"
def process_queries(ipqueryfile, opqueryfile, stopfile = ""):

    # parse input query file and get a list of Query
    queries = cacm_queries(ipqueryfile)

    # process queries
    queries = map(lambda q: Query(q.qid, process_text(q.querystr, stopfile)), queries)

    # store queries to output query file
    assert (not os.path.exists(opqueryfile))

    # write queries to file
    with open(opqueryfile, "w+") as qf:

        for q in queries:
            qf.write(str(q.qid) + " " + q.querystr + "\n")


## Main ########################################################################

## Get arguments
args = vars(argparser.parse_args())

## Inputs
ipqueryfile = args['ipqueryfile']
opqueryfile = args['opqueryfile']
stopfile    = args['stopfile']
verbose            = args['verbose']

## Input check
if (not os.path.exists(ipqueryfile)):
    print "FATAL: Cannot find ipqueryfile ", ipqueryfile
    exit(-1)
if (stopfile != "" and (not os.path.exists(stopfile))):
    print "FATAL: Cannot find stopfile", stopfile
    exit(-1)

## Output exists already ? remove if yes
if (os.path.exists(opqueryfile)):
    print "WARNING: Removing existing opqueryfile ", opqueryfile
    exit(-1)

# get to work
process_queries(ipqueryfile, opqueryfile, stopfile)
