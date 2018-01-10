# This python program, takes in a file containing document ranking strings (in
# TREC format), the queryfile and indexstore which were used to compute
# the rankings, and prints the document snippets as per the results

from docrank_trec import DocRankTREC, resultfile_to_docranks
from query        import queries
from snippet      import get_snippets

import os
import argparse
from   argparse import RawTextHelpFormatter

## Globals #####################################################################

# Print to the terminal what the program is doing
# This is set by input to the program
verbose = False

# Prompt for user input when displaying snippets
# This is set by input to the program
interactive = False

## Help strings ################################################################

program_help = '''
    gen_snippet.py translates a bunch of TREC format result strings to document
    snippets corresponding to each result string

    Argument 1: resultfile - Path to the result find containing resultstrings
                             corresponding to ranked documents. The file should
                             contain result strings according to the TREC format
                             which is as follows,
                             "query_id Q0 doc_id rank score system_name"

    Argument 2: queryfile  - Path to the queryfile that was used to generate the
                             result file.

    Argument 3: indexstore - Path to the folder where the index is stored. Use
                             the same indexstore that was used in ranking the
                             documents for queries in the queryfile, and
                             subsequently generating the result file

    Argument 4: stopfile   - Path to any stopfile. This helps in generating
                             good snippets but is entirely optional

    Argument 5: snippetfile - Path to a file where to write snippets of all results.
                              (optional)

    Argument 6: interactive - Prompts the user for options when displaying
                              results

    Argument 7: verbose    - Print to the terminal, the progress of the program.
                             This is optional. Turned off by default

    EXAMPLE:

        python gen_snippet.py --resultfile=./cacm.result.bm25 --queryfile=queries.txt --indexstore=cacm.index --resultfile=./cacm.result.bm25  --stopfile=cacm/common_words --snippetfile=./snippets.bm25 --verbose

    '''

resultfile_help = '''
    Path to the result find containing resultstrings corresponding to ranked
    documents. The file should contain result strings according to the TREC
    format which is as follows,
     "query_id Q0 doc_id rank score system_name"
    '''

queryfile_help = '''
    Path to the queryfile that was used to generate the result file.
    '''

indexstore_help = '''
    Path to the folder where the index is stored. Use the same indexstore that
    was used in ranking the documents for queries in the queryfile, and
    subsequently generating the result file
    '''

stopfile_help = '''
    Path to any stopfile. This helps in generating good snippets but is optional
    '''

snippetfile_help = '''
    Path to a file where to write the snippets of all files
    '''

interactive_help = '''
    Prompts the user for options when displaying results. optional.
    Turned off by default
    '''

verbose_help = '''
    Print to the terminal, the progress of the program. This is optional.
    Turned off by default
    '''

## Setup argument parser ######################################################

argparser = argparse.ArgumentParser(description = program_help,
                                    formatter_class = RawTextHelpFormatter)

argparser.add_argument("--resultfile",
                       metavar  = "rf",
                       required = True,
                       type     = str,
                       help     = resultfile_help)

argparser.add_argument("--queryfile",
                       metavar  = "qf",
                       required = True,
                       type     = str,
                       help     = queryfile_help)

argparser.add_argument("--indexstore",
                       metavar  = "is",
                       required = True,
                       type     = str,
                       help     = indexstore_help)

argparser.add_argument("--stopfile",
                       metavar  = "sf",
                       default  = "",
                       type     = str,
                       help     = stopfile_help)

argparser.add_argument("--snippetfile",
                       metavar = "o",
                       default = "",
                       type    = str,
                       help    = snippetfile_help)

argparser.add_argument("--interactive",
                       dest    = "interactive",
                       action  = 'store_true',
                       default = False,
                       help    = interactive_help)

argparser.add_argument("--verbose",
                       dest     = 'verbose',
                       action   = 'store_true',
                       default  = False,
                       help     = verbose_help)

## Display snippets ############################################################

##
# GIVEN : a queryfile, containing space separated queries, and
#         a dictionary of (key, value) pair of (queryid, ranked_snippet_list)
#         a boolean value, indicating if the display should be interactive
# Display snippets to the terminal
#
def display(queryfile, qid_snippets_dict, interactive = True):

    # convert queryfile into a list of queries
    query_lst  = queries(queryfile)

    # For every query, print snippets
    for q in query_lst:

        # Print query
        print "================================================================"
        print "Query : ", q.querystr

        # Get queries snippets
        q_snippets = qid_snippets_dict[q.qid]

        # Print snippets
        for q_snippet in q_snippets:

            # Mark separation
            print "----------------------------------------------------------------"

            print q_snippet

            # Mark separation
            print "----------------------------------------------------------------"

            # Ask for user input for continuing display
            if (q_snippets.index(q_snippet) % 5 == 4 and interactive):
                # Prompt user
                print "Press : c to continue                           \n" + \
                      "        n to print results for next query       \n" + \
                      "        f to print all snippets for all queries \n" + \
                      "        e to exit"

                userinput = raw_input("Please enter choice : ")

                if (userinput == "c"):
                    # print next set of snippets for this query
                    continue
                elif (userinput == "n"):
                    # print results for next query
                    break
                elif (userinput == "f"):
                    # stop prompting the user and keep printing results
                    prompt = False
                    continue
                elif (userinput == "e"):
                    # exit result print
                    return
                else:
                    print "Unrecognized user input; continuing as if \"c\" pressed "
                    # print next set of snippets for this query
                    continue

##
# GIVEN : a queryfile, containing space separated queries, and
#         a dictionary of (key, value) pair of (queryid, ranked_snippet_list)
#         the path to a file, where to write the snippets
# Print snippets to file
#
def print_snippets_to_file(queryfile, qid_snippets_dict, snippetfile):

    # make sure that the snippet file does not exists
    assert (not os.path.exists(snippetfile))

    # convert queryfile into a list of queries
    query_lst  = queries(queryfile)

    # open output snippet file
    snippet_f = open(snippetfile, "w+")

    # For every query, print snippets
    for q in query_lst:

        # Print query to output file
        snippet_f.write("================================================================\n")
        snippet_f.write("Query : " + q.querystr + "\n")

        # Get queries snippets
        q_snippets = qid_snippets_dict[q.qid]

        # Print snippets
        for q_snippet in q_snippets:

            # Mark separation
            snippet_f.write("----------------------------------------------------------------\n")

            snippet_f.write(q_snippet)

            # Mark separation
            snippet_f.write("----------------------------------------------------------------\n")

    snippet_f.close()

##
# Given the path to a file containing TREC Eval resultstrings for multiple queries
#       the path to a file containing the acutual queries, that correspond to the
#       resultfile
#       an indexstore, where the index used process the queries is present,
#       an optional stopfile
# Returns a dictionary of (key, value) (queryid, ranked snippet list) pairs
#
def get_snippet_dict(resultfile, queryfile, indexstore, stopfile = ""):

    # get list of queries
    query_lst = queries(queryfile)

    # transform contents of resultfile into list of DocRankTRECs
    docranks = resultfile_to_docranks(resultfile)

    return get_snippets(query_lst, docranks, indexstore, stopfile)

## Main ########################################################################

## Get arguments
args = vars(argparser.parse_args())

## Inputs
resultfile  = args['resultfile']
queryfile   = args['queryfile']
indexstore  = args['indexstore']
stopfile    = args['stopfile']
snippetfile = args['snippetfile']
interactive = args['interactive']
verbose     = args['verbose']

## Input check
if (not os.path.exists(resultfile)):
    print "FATAL: Cannot find resultfile, ",resultfile
    exit(-1)
if (not os.path.exists(queryfile)):
    print "FATAL: Cannot find queryfile, ", queryfile
    exit (-1)
if (not os.path.exists(indexstore)):
    print "FATAL: Cannot find indexstore, ", indexstore
    exit (-1)
if (stopfile != "" and (not os.path.exists(stopfile))):
    print "FATAL: Cannot find stopfile, ", stopfile
    exit(-1)

## Snippet output file check
if (snippetfile != "" and os.path.exists(snippetfile)):
    # Remove existing snippet file
    print "WARNING: Deleting existing snippetfile"
    os.remove(snippetfile)

# get to work !

# Get a dictionary of (key, value) of (queryid, ranked list of snippets)
qid_snippets_dict = get_snippet_dict(resultfile, queryfile, indexstore, stopfile)

# display snippets to the terminal
if interactive:
    display(queryfile, qid_snippets_dict, interactive)

# print snippets to file
if (snippetfile != ""):
    print_snippets_to_file(queryfile, qid_snippets_dict, snippetfile)
