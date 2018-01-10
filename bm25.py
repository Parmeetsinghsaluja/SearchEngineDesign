##This file implements the BM25 retrieval model

from index             import Index
from query             import Query
from result_set        import Result, ResultSet, DocumentScore
from global_statistics import GlobalStatistics

import math
import os

## BM25 ########################################################################

class BM25:

    ## Global statistics
    global_stats = None

    ## Inverted index
    invidx       = None

    ## BM25 parameters
    k1 = 1.2
    k2 = 100
    b  = 0.75

    ## Constructor
    # Given an indexstore where the index file is stored by (indexer.py)
    #       and a global statistics file path
    #
    # Initializes the bm25 algorithm
    #
    def __init__(self, indexstore, gsfile, k1_ = 1.2, k2_ = 100, b_ = 0.75):

        # reset
        self.reset()

        # Is there an index store?
        if (not os.path.exists(indexstore)):
            print "FATAL: Indexstore doesnot exists, cannot initialize BM25"
            return

        # Get index
        self.invidx = Index(indexstore)

        # Get global statistics
        self.global_stats = GlobalStatistics(gsfile)

        # Set BM25 parameters
        self.k1 = k1_
        self.k2 = k2_
        self.b  = b_

    # Reset
    def reset(self):

        ## Global statistics
        self.global_stats = None

        ## Inverted index
        self.invidx       = None

        ## BM25 parameters
        self.k1 = 1.2
        self.k2 = 100
        self.b  = 0.75

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

            doc_bm25_score = 0

            # Score document for every query term
            for qt in query_tf_dict:

                # query term frequency
                qtf = query_tf_dict.get(qt)

                # calculate bm25 score
                doc_bm25_score = doc_bm25_score + \
                                 self.bm25_term_score(mini_index, docid, qt, qtf)

            docscores.append(DocumentScore(docid, doc_bm25_score, "BM25"))

        # Sort doc scores based on score from highest to lowest
        docscores = sorted(docscores, key = lambda x: x.score, reverse=True)

        # return result set
        return ResultSet(query, docscores)


    # GIVEN a dictionary of (term, inverted list), mini_index and
    #       a document id, docid
    #       a query term, qt
    #       the frequency of the query term in the query, qtf
    # RETURNS the bm25 score for the document with respect to the query term
    #
    def bm25_term_score (self, mini_index, docid, qterm, qtf):

        # input sanity check
        assert (docid >= 0)
        assert (mini_index.get(qterm) is not None)
        assert (qtf > 0)

        # Get frequency of term in document
        doctf  = self.document_tf (qterm, docid, mini_index)
        if (doctf == 0):
            # Query term does not appear in document. skip
            return 0

        # The BM25 model's query term scoring formula is made of 3 parts
        #
        #  1. log of Binary Independence Model score
        #  2. Term frequency weight score
        #  3. Query term frequency weight score
        #
        # These three scores are multiplied to realize the final score
        # of the document for this query term

        # Get all variables
        dl      = self.global_stats.document_length(docid) # doc length
        avdl    = self.global_stats.get_avdl()             # avg. doc length
        N       = self.global_stats.get_N()                # total docs in corpus
        nqt     = len(mini_index.get(qterm))               # #docs with qt (ni)

        # Variable sanity check
        assert (nqt  > 0)
        assert (dl   > 0)
        assert (avdl > 0)
        assert (N    > 0)
        assert (nqt  > 0)

        term_bimscore = self.bimscore(N, nqt)

        term_tfscore  = self.tfscore(doctf, dl, avdl, self.k1, self.b)

        term_qfscore  = self.qfscore(qtf, self.k2)

        term_score = term_bimscore * term_tfscore * term_qfscore

        return term_score

    # GIVEN: The total number of documents in corpus, N and
    #        The number of documents containing the term of interest
    # RETURNS: The score of the document as per Binary Independece Model
    # NOTE : The function assumes that there is no relevance information
    #        available and hence requires only 2 input arguments
    def bimscore (self, N, nt):

        idflike_score = float(float(N) - float(nt) + 0.5) / float(float(nt) + 0.5)

        return math.log(idflike_score)

    # GIVEN: the frequency of a query term in a document of interest, tf,
    #        the length of the document of interest, dl
    #        the average length of documents in a corpus, avdl,
    #        the BM25 parameter k1 and
    #        the BM25 parameter b
    # RETURNS: the score for the document term frequency component in BM25 formula
    #
    def tfscore (self, doctf, dl, avdl, k1, b):

        # Compute BM25 parameters K from other BM25 params k1 and b
        K = float(k1) * ((1.0 - float(b)) + \
                         (float(b) * (float(dl) / float(avdl))))

        return float(((float(k1) + 1.0) * float(doctf)) / \
                      (float(K)         + float(doctf)))

    # GIVEN: the frequency of the query term in the query and
    #        the BM25 parameter k2
    # RETURNS: the score for the query term frequency component in BM25 formula
    #
    def qfscore (self, qtf, k2):

        return float((float(k2) + 1.0) * float(qtf) / \
                     (float(k2)        + float(qtf)))

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
    # returns the posting that belongs to document docid.
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
