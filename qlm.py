# This file implements the query likelihood retreival model

from index             import Index
from query             import Query
from result_set        import Result, ResultSet, DocumentScore
from global_statistics import GlobalStatistics

import math
import os

## Query likelihood model ######################################################

class QLM:

    ## Global statistics
    ## refer to global_statistics.py. it provides may global statistics get functions
    global_stats = None

    ## Inverted index
    invidx       = None

    # Query likelihood model parameter
    l = 0.35

    ## Constructor
    # Given an indexstore where the index file is stored by (indexer.py)
    #       and a global statistics file path
    #
    # Initializes the Query likelihood model
    #
    def __init__(self, indexstore, gsfile,l_=0.35):

        # reset
        self.reset()

        # Is there an index store?
        if (not os.path.exists(indexstore)):
            print "FATAL: Indexstore doesnot exists, cannot initialize QLM"
            return

        # Get index
        self.invidx = Index(indexstore)

        # Get global statistics
        self.global_stats = GlobalStatistics(gsfile)

        # Initialize parameters
        self.l=l_

    # Reset
    def reset(self):

        ## Global statistics
        self.global_stats = None

        ## Inverted index
        self.invidx       = None

        ## Initialize parameters
        self.l=0.35

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
    #          what documents in the index matched the query.
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

            doc_qlm_score = 0

            # Score document for every query term
            for qt in query_tf_dict:

                # query term frequency
                qtf = query_tf_dict.get(qt)
                # calculate bm25 score
                doc_qlm_score = doc_qlm_score + self.qlm_term_score(mini_index, docid, qt, qtf,self.l)
            docscores.append(DocumentScore(docid, doc_qlm_score, "QLM"))

        # Sort doc scores based on score from highest to lowest
        docscores = sorted(docscores, key = lambda x: x.score, reverse=True)

        # return result set
        return ResultSet(query, docscores)

    def qlm_term_score (self, mini_index, docid, qterm, qtf,l):
        # input sanity check
        assert (docid >= 0)
        assert (mini_index.get(qterm) is not None)
        assert (qtf > 0)

        # Get frequency of term in document
        doctf  = self.document_tf(qterm, docid, mini_index)
        # Get frequency of term in document
        collecf  = self.collection_tf(qterm, mini_index)
        if (collecf == 0):
            # Query term does not appear in document. skip
            return 0

        # Get all variables
        dl      = self.global_stats.document_length(docid) # doc length
        cl      = self.global_stats.get_corpussize()      #  collection size
        score =  float((1-l)* float(float(doctf)/ float(dl)) + float(l) * float(float(collecf)/float(cl)))
        return math.log(score)



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
        return term_postings[docposting_idx].tf

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

    def collection_tf(self,term,mini_index):
        term_postings = mini_index.get(term)
        i=0
        frequency=0
        while (i< len(term_postings)):
            frequency= frequency + term_postings[i].tf
            i=i+1
        return frequency
