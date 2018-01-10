# This file contains a class that represents a TREC result string

import os

## DocRankTREC #################################################################

class DocRankTREC:

    # query id
    qid = None
    # ranked document id
    docid   = None
    # rank of the document of id docid
    rank    = None
    # score of the ranked document
    score   = None
    # name of the system used in ranking
    system  = None

    # reset
    def reset(self):
        # reset all state variables
        self.qid = None
        self.docid   = None
        self.rank    = None
        self.score   = None
        self.system  = None

    # Constructor
    # Given a TREC result string, parse it and populate self's state variables
    def __init__(self, trec_result_str):

        # trec result string is of the following format
        # "query_id Q0 doc_id rank score system_name"

        # parse trec result to populate this
        trec_result_parts = trec_result_str.split(" ")

        # set state variables
        self.qid     = int(trec_result_parts[0])
        #self.Q0     = trec_result_parts[1]
        self.docid   = int(trec_result_parts[2])
        self.rank    = int(trec_result_parts[3])
        self.score   = float(trec_result_parts[4])
        self.system  = trec_result_parts[5]

    # print this object
    def print_docranktrec(self):
        print str(self.qid), " ", str(self.docid), " ", str(self.rank), " ", \
              str(self.score), " ", self.system

## Utilities ###################################################################

##
# Given a resultfile that contains "\n" separated strings, where each line
#       corresponds to a resultstring in TREC Eval format
# Returns a list of DocRankTREC objects, where every resultstring in the input
#         file is represented by one DocRankTREC object in the output list
def resultfile_to_docranks(resultfile):

    # Input check
    assert (os.path.exists(resultfile))

    # get resultstrings from resultfile
    resultstrings = []
    with open(resultfile, "r") as f:
        resultstrings = f.readlines()

    # get a list of docranks
    docranks = []
    for resultstring in resultstrings:
        docranks.append(DocRankTREC(resultstring))

    return docranks

################################################################################
