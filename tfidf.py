# This file implements the tf.idf retreival model

from index             import Index
from query             import Query
from result_set        import Result, ResultSet, DocumentScore
from global_statistics import GlobalStatistics

import math
import os

## TF.IDF ######################################################################

class TFIDF:

    ## Global statistics
    ## refer to global_statistics.py. it provides may global statistics get functions
    global_stats = None

    ## Inverted index
    invidx       = None

    # tf.idf parameters
    # lambda ?

    ## Constructor
    # Given an indexstore where the index file is stored by (indexer.py)
    #       and a global statistics file path
    #
    # Initializes the tf.idf model
    #
    def __init__(self, indexstore, gsfile):

        # reset
        self.reset()

        # Is there an index store?
        if (not os.path.exists(indexstore)):
            print "FATAL: Indexstore doesnot exists, cannot initialize TFIDF"
            return

        # Get index
        self.invidx = Index(indexstore)

        # Get global statistics
        self.global_stats = GlobalStatistics(gsfile)

        # Initialize parameters
        # lambda

    # Reset
    def reset(self):

        ## Global statistics
        self.global_stats = None

        ## Inverted index
        self.invidx       = None

        ## Initialize parameters
        # lambda = ?

    ##
    # GIVEN : a list of Query (from query.py)
    # RETURNS: a list of ResultSet where the first resultset in the list
    #          corresponds to the first query in the input list and so on
    #
    def search(self, queries):

        # resultsets
        results = []

        # for every query
        for query in queries:
            # search query in index
            resultset = self.search_query(self.invidx, query)
            # store result
            results.append(resultset)

        return results

    ##
    # GIVEN : a Query (from query.py)
    # RETURNS: a ResultSet (from result_set.py) that contains information about
    #          what documents in the index matched the query and their corresponding
    #          document scores with other information
    #
    def search_query(self, invidx, query):

        # TODO: For now we know that query terms are split by spaces.
        #       going forward generalize this
        query_terms = query.querystr.split(" ")

        # filter query terms not appearing in index
        query_terms = filter(lambda qt: invidx.contains_term(qt), query_terms)

        # Create a query-termfreqency dictionary. This will remove duplicate
        query_tf_dict = self.termfrequency(query_terms)

        # Get a dictionary of related invlists with key value pairs (term, postings)
        # This is in essence a mini-index
        mini_index    = self.invidx.minindex(query_terms)

        # Get set of related documents
        docids        = self.invidx.docids_with_terms(set(query_terms))

        # List of document scores (DocumentScore from result_set.py)
        docscores     = []

        # Score every document in set
        for docid in docids:

            doc_tfidf_score = 0

            # Score document for every query term
            for qt in query_tf_dict:

                # calculate tf-idf score
                doc_tfidf_score = doc_tfidf_score + \
                                 self.tfidf_term_score(mini_index, docid, qt)

            docscores.append(DocumentScore(docid, doc_tfidf_score, "TFIDF"))

        # Sort doc scores based on score from highest to lowest
        docscores = sorted(docscores, key = lambda x: x.score, reverse=True)

        # return result set
        return ResultSet(query, docscores)

    # GIVEN a dictionary of (term, inverted list), mini_index and
    #       a document id, docid
    #       a query term, qt
    # RETURNS the tf-idf score for the document with respect to the query term
    #
    def tfidf_term_score (self, mini_index, docid, qterm):

        # input sanity check
        assert (docid >= 0)
        assert (mini_index.get(qterm) is not None)

        # Get frequency of term in document
        doctf  = self.document_tf (qterm, docid, mini_index)
        if (doctf == 0):
            # Query term does not appear in document. skip
            return 0

        # Get document frequency variables
        nqt     = float(len(mini_index.get(qterm)))               

        # Variable sanity check
        assert (nqt  > 0)

        term_score = float(doctf * (1/nqt))

        return term_score


    # GIVEN a list of term
    # RETURNS a dictionary of key value pairs (term, termfreqency)
    #
    def termfrequency(self, terms):

        # initialize return dict
        tf_dict = {}

        for t in terms:
            # Not seen this query term ever ?
            if (tf_dict.get(t) is None):
                tf_dict[t] = 1

            else:
                tf_dict[t] = tf_dict.get(t) + 1

        return tf_dict

    # GIVEN a term, document id and a mini_index that contains an entry for the
    #       term
    # RETURNS: the frequency of the term in the document as stored in the
    #          mini_index.
    def document_tf(self, term, docid, mini_index):

        # Sanity check
        assert (mini_index.get(term) is not None)
        assert (docid >= 0)

        # Get inverted_list / postings of the term
        term_postings = mini_index.get(term)

        # Get index of the posting of document docid
        docposting_idx = self.posting_idx(term_postings, docid)
        # document posting not found. The term does not appear in the document
        if (docposting_idx == -1):
            return 0

        # Term does appear in the document
        # Sanity check
        assert (docposting_idx >= 0 and docposting_idx < len(term_postings))
        assert (term_postings[docposting_idx].docid >= 0)
        assert (term_postings[docposting_idx].tf     > 0)

        # return frequency
        return float(term_postings[docposting_idx].tf)

    # given a list postings sorted by docid, a docid,
    # returns the term frequency in the posting.
    # if no such posting exists, then return -1
    def posting_idx(self, postings, docid):

        assert (isinstance(docid, int))

        # the postings list is sorted. lets binary search
        left  = 0
        right = len(postings) - 1

        while(left <= right):

            mid = (left + right) / 2

            if (postings[mid].docid == docid):
                return mid

            if (postings[mid].docid < docid):
                left = mid + 1

            if (postings[mid].docid > docid):
                right = mid - 1

        return -1
