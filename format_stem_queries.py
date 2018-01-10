# This prorgram given the cacm stemmed queries in file cacm_stem.query.txt,
# format and store the queries in another file in following format,
#  "queryidSPACEqueryNEWLINE"

import os
import argparse
from argparse import RawTextHelpFormatter

## Globals #####################################################################

# Print to terminal about what the program is doing
# this is set by input to the program
verbose = False

## Help strings ################################################################

program_help = '''
    Given a cacm stemmed queries file (cacm_stem.query.txt), format and store
    the  queries in another file in the following format,
     "queryidSPACEqueryNEWLINE"

    This program takes 4 arguments,

    Argument 1 : ipqueryfile : Path to the cacm_stem.query.txt

    Argument 2 : opqueryfile : Path to a file where the output query file must
                               be stored

    Argument 3 : verbose     : Print to the terminal, what the program is doing

    Examples:

        python query_processing_stemmed.py --ipqueryfile=./cacm/cacm_stem.query.txt --opqueryfile=./queries.stem.txt --verbose
    '''

ipqueryfile_help = '''
    Path to the cacm query file (cacm_stem.query.txt)
    '''

opqueryfile_help = '''
    Path to a file where the output query file must be stored
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

argparser.add_argument("--verbose",
                       dest    = 'verbose',
                       action  = 'store_true',
                       help    = verbose_help)

## Process Queries #############################################################

# Given the path to an input cacm query file (cacm_stem.query.txt)
#       the path to where the processes output query file should be stored
# Reformat the queries in cacm_stem.query.txt and store the queies in the
# opqueryfile in the format "queryidSPACEqueryNEWLINE"
def format_queries(ipqueryfile, opqueryfile):

    assert (os.path.exists(ipqueryfile))

    queries = []

    # Read the ipqueryfile into lines
    lines = []
    with open(ipqueryfile) as qf:
        lines = qf.readlines()

    assert (not os.path.exists(opqueryfile))

    # Write queries to the output query file
    with open(opqueryfile, "w+") as qf:
        for line in lines:
            qf.write(str(lines.index(line) + 1) + " " + line.strip() + "\n")

## Main ########################################################################

## Get arguments
args = vars(argparser.parse_args())

## Inputs
ipqueryfile = args['ipqueryfile']
opqueryfile = args['opqueryfile']
verbose            = args['verbose']

## Input check
if (not os.path.exists(ipqueryfile)):
    print "FATAL: Cannot find ipqueryfile ", ipqueryfile
    exit(-1)

## Output exists already ? remove if yes
if (os.path.exists(opqueryfile)):
    print "WARNING: Removing existing opqueryfile ", opqueryfile
    os.remove(opqueryfile)

# get to work
format_queries(ipqueryfile, opqueryfile)
