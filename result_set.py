## This file defines a class that is the return type of all retrieval models

from query import Query

## Result ######################################################################

# Data store that represents the result of a single document
class Result:

    # Query (from query.py) used for which the document is scored
    query = None
    # Document ID
    docid = 0
    # Rank of the document
    rank = -1
    # Score of the document
    score = 0
    # model used to score document
    model = ""

    # Constructor
    def __init__(self, query_, docid_, rank_, score_, model_):

        # reset
        self.reset()

        self.query = query_
        self.docid = docid_
        self.rank  = rank_
        self.score = score_
        self.model = model_

    # Reset
    def reset(self):

        self.query = None
        self.docid = 0
        self.rank  = -1
        self.score = 0
        self.model = ""


    # return result as string (TREC format)
    def trec_result_string(self):
        return str(self.query.qid) + " " + "Q0" + " " + str(self.docid) +  \
               " " + str(self.rank) + " " + str(self.score) + " " + self.model

    # print result
    def print_result(self):
        print self.trec_result_string()


## ResultSet ###################################################################

# Data store that represents the result set for a query
class ResultSet:

    # Query used to search the index
    query   = None

    # List of results ranked in from 0 to N
    results = []

    # Constructor
    def __init__(self, query_, docscores_, maxrank = 100):

        # Reset
        self.reset()

        # Set query
        self.query   = query_

        # From documen score list. get a list of ranked Result
        docscores_ranked = sorted(docscores_, key = lambda x: x.score, reverse=True)

        for idx in range(0, min(len(docscores_ranked), maxrank)):

            # get docscore
            docscore = docscores_ranked[idx]

            # document rank
            rank = idx + 1

            # docscore -> Result
            self.results.append(Result(query_, docscore.docid, rank, docscore.score, docscore.model))

    # Reset
    def reset(self):
        self.query   = None
        self.results = []

    # Print result set
    def print_resultset(self):

        print "----------------------------------------------------------------"

        print "Query : ", self.query.querystr

        for result in self.results:
            result.print_result()

        print "----------------------------------------------------------------"

    # return results in result set as list of strings (TREC format)
    def trec_result_strings(self):

        # initialize return list to empty
        result_strings = []

        # get result strings
        for result in self.results:
            result_strings.append(result.trec_result_string())

        return result_strings

## DocumentScore ###############################################################

# Data store that represents the score of a document identified by the docid
class DocumentScore:

    # Document ID
    docid = -1
    # Document score
    score = None
    # Retrieval model used to score the documents
    model = ""

    # Constructor
    def __init__(self, docid_, score_, model_):

        # Reset
        self.reset()

        # Initialize class
        self.docid = docid_
        self.score = score_
        self.model = model_

    # Reset
    def reset(self):

        self.docid = -1
        self.score = None
        self.model = ""


################################################################################
