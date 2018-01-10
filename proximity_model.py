# This file implements a retrieval model that prioritizes proximity search. It
# focuses on acheiving 2 things,
# 1. Terms should appear in the matching document in the same order as the query
# 2. Allow a maximum proximity of three terms, that is, adjacent query terms can
#    be separated by no more than 3 terms in the matching document. Documents
#    with terms appearing closer to each other are deemed better matches.

from index             import Index
from query             import Query
from result_set        import Result, ResultSet, DocumentScore
from global_statistics import GlobalStatistics
from bm25              import BM25

import os

## Globals #####################################################################

# Adjacent query terms must appear within this window
PROXIMITY_WINDOW = 5

## Proximity Term score ########################################################

# ProximityTermScore class that records scores of a term at a particular position
class ProximityTermScore:

    # Term
    term            = ""
    # position
    pos             = -1
    # base score
    base_score      = 0
    # proximity score
    proximity_score = 0

    # reset
    def reset(self):
        self.term            = ""
        self.pos             = -1
        self.base_score      = 0
        self.proximity_score = 0

    # Constructor
    def __init__(self, term_, pos_, base_score_, proximity_score_):

        # reset
        self.term            = term_
        self.pos             = pos_
        self.base_score      = base_score_
        self.proximity_score = proximity_score_

## Proximity model #############################################################

class ProximityModel:

    ## Global statistics
    global_stats = None

    ## Inverted index
    invidx       = None

    ## proximity window
    window       = PROXIMITY_WINDOW

    # base model. The base model should expose a function to score
    # query terms individually
    base_model  = None

    # reset
    def reset(self):
        self.global_stats = None
        self.invidx       = None
        self.window       = PROXIMITY_WINDOW
        self.base_model   = None

    # Constructor
    def __init__(self, indexstore, gsfile, window_ = PROXIMITY_WINDOW):

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

        # Set parameters
        self.window =  window_

        # Initialize base_model. our base model is BM25
        self.base_model = BM25(indexstore, gsfile)

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

        # Idea is that, every query term has a base_score and a proximity score
        # The base score is the term score from the base model.
        # Proximity score of a term at a particular position, depends on what
        # terms it is close to

        query_terms = query.querystr.split(" ")

        # Get a minindex that contains all available inverted lists of terms that
        # appear in the query
        mini_index = self.minindex(query)

        # Get set of related documents
        docids     = self.invidx.docids_with_terms(set(query_terms))

        # Initialize document score list
        docscores = []

        for docid in docids:

            # Get base scores for each query term for this docid. This base score
            # would tell us the importance of each query term
            qt_base_score_dict = self.base_scores(query_terms, docid, mini_index)

            # We have query terms as there are keys in the mini_index
            # But since we are mainly worried about proximity search, a query
            # term appearing at position X (e.g. 3) is very different from a
            # query term that appears at a position Y (e.g. 55) in the same
            # document. Because a query term appearing at position X need not be
            # surrounded by the same term like in position Y. query term scores
            # are very position dependent

            # Initialize position dependent term score dictionary
            pos_tscore_dict = self.init_proximity_term_scores(mini_index, docid)

            # Add base_scores for every term's ProximityTermScore that appears
            # in pos_tscore_dict
            for pos in pos_tscore_dict:
                # get ProximityTermScore for term at this position
                pts = pos_tscore_dict[pos]
                # assert initial scores
                assert (pts.base_score      == 0)
                assert (pts.proximity_score == 0)
                # update pts with term base score
                pts.base_score = qt_base_score_dict[pts.term]
                # add pts back to pos_tscore_dict
                pos_tscore_dict[pos] = pts

            # compute proximity scores for terms at all postions in pos_tscore_dict
            pos_tscore_dict = self.score_for_proximity(pos_tscore_dict, query)

            # add up all the basescores and proximity scores of all terms to be
            # the score for this document
            doc_proximity_model_score = 0
            for pos in pos_tscore_dict:
                # Get this ProximityTermScore
                pts = pos_tscore_dict.get(pos)
                # get total score
                total_term_score = pts.base_score + pts.proximity_score
                # update doc_proximity_model_score
                doc_proximity_model_score = doc_proximity_model_score + total_term_score

            # Debugger
            #if (query.qid == 65 and docid == 3205):
            #    print "docscore ", doc_proximity_model_score
            #    print "query    ", query.querystr
            #    slist = []
            #    for pos in pos_tscore_dict:
            #        # get ProximityTermScore for term at this position
            #        pts = pos_tscore_dict[pos]
            #        s =  " * %0.4d %-*s %0.4f %0.4f \n" % (pts.pos, 15, pts.term, pts.base_score, pts.proximity_score)
            #        slist.append(s)
            #    slist.sort()

            #    for s in slist:
            #        print s

            docscores.append(DocumentScore(docid, doc_proximity_model_score, "PROXIMITY"))

        # Sort doc scores based on score from highest to lowest
        docscores = sorted(docscores, key = lambda x: x.score, reverse=True)

        # return result set
        return ResultSet(query, docscores)

    # Given a Query (query.py)
    # return a dictionary of (key, value) pairs of (terms, invertedlist) of all
    # query terms that appears in self.invidx (the big index)
    def minindex(self, query):

        # get unique query terms
        query_terms = list(self.query_terms_set(query))

        # filter all query terms that appear in the self.invidx
        query_terms = filter(lambda qt: self.invidx.contains_term(qt), query_terms)

        # return mini index
        return self.invidx.minindex(query_terms)

    # Given a list of all query_terms, and
    #       the id of a document, docid, and a
    #       a dictionary of (term, invertedlist) values for all the query terms,
    #       that appear in self.invidx
    # Returns a dictionary of (key, value) pairs of (query_term, base_score)
    def base_scores(self, query_terms, docid, mini_index):

        # get frequencies of all terms in the query as a dict
        qtf_dict = self.termfrequency(query_terms)

        # initialize base score dictionary
        base_score_dict = {}

        for query_term in set(query_terms):

            # assert that we got this query term's termfrequency
            assert (qtf_dict.get(query_term) is not None)

            # get base score
            base_score = 0
            if (mini_index.get(query_term) is not None):
                base_score = self.base_model.bm25_term_score(mini_index,
                                                             docid,
                                                             query_term,
                                                             qtf_dict[query_term])
            # record score in base_score_dict
            base_score_dict[query_term] = float(base_score)

        return base_score_dict

    # Given a dictionary of (key, value), (position, ProximityTermScore) with
    #       only base scores computed on every ProximityTermScore value, and
    #       a Query (query.py)
    # Return a dictionary, just like the original but with proximity scores
    #        computed to the ProximityTermScore value
    def score_for_proximity(self, pos_tscore_dict, query):

        # get all query terms
        query_terms = query.querystr.split(" ")

        # compute list of terms to the left of each term in query_terms
        # we say "list of terms", as, if there are duplicates of a term, say X,
        # in query_terms we will have to account for all the terms occuring
        # next to all occurances of X
        query_adjterm_dict = {}
        # init empty list values for all query terms
        for qt in query_terms:
            query_adjterm_dict[qt] = []
        # fill up adjacent terms
        for qtidx in range(0, len(query_terms) - 1):
            # query term
            qt = query_terms[qtidx]
            # adjacent query term
            adj_qt = query_terms[qtidx + 1]
            # add adj term
            query_adjterm_dict[qt] = query_adjterm_dict[qt] + [adj_qt]

        # get all positions in pos_tscore_dict
        positions = []
        for pos in pos_tscore_dict:
            positions.append(pos)

        # sort positions .. we want to go from left to right
        positions.sort()

        # for every position in pos_tscore_dict
        for pos in positions:

            # get term in this position
            term = pos_tscore_dict[pos].term

            # get term's basescore
            base_score = pos_tscore_dict[pos].base_score

            # get term's proximity score
            proximity_score = pos_tscore_dict[pos].proximity_score

            # pre proximity score; This is the term's proximity score based on
            # its proximity of all query terms appearing before this term
            pre_proximity_score = pos_tscore_dict[pos].proximity_score

            # for all adjacent terms in the query to this term
            for qtadj in query_adjterm_dict.get(term):

                offset = self.term_offset_in_window(pos_tscore_dict, pos, qtadj)

                if (offset == -1):
                    # adjterm not found in window
                    continue

                # assert that we have a term at pos + offset
                assert (pos_tscore_dict.get(pos + offset) is not None)

                # get the adjacent term's ProximityTermScore
                adj_pts = pos_tscore_dict.get(pos + offset)

                # REWARD
                # the smaller the offset the closer the adj term is and a term's
                # proximity score is directly proportional to its base score and
                # its neighbour's base score and the distance between them
                proximity_score = proximity_score                 + \
                                  (self.window - offset)          * \
                                  base_score * adj_pts.base_score

                # update adjacent term's proximity score
                adj_pts.proximity_score = adj_pts.proximity_score             + \
                                          pre_proximity_score                 + \
                                          (self.window - offset)              * \
                                          base_score * adj_pts.base_score
                pos_tscore_dict[pos + offset] = adj_pts

            # if proximity score is 0. this means this terms has no adj
            # query terms in its neighbourhood.. this is bad. penalize the term
            if (proximity_score == 0):
                # PENALIZE
                proximity_score = proximity_score - (self.window * base_score)

            # Update proximity score of the term at this pos
            term_pts = pos_tscore_dict[pos]
            term_pts.proximity_score = proximity_score
            pos_tscore_dict[pos] = term_pts

        return pos_tscore_dict

    # Given a dictionary of (key, value) pairs of (position, ProximityTermScore) and
    #       a position, pos, and
    #       a term,
    #       return the offset of the term in a window of PROXIMITY_WINDOW starting
    #       from pos
    #       if the term does not appear in the window, return -1
    def term_offset_in_window(self, pos_tscore_dict, pos, term):

        # iterate over window
        for i in range(pos, pos + self.window):

            # no query term at i
            if (pos_tscore_dict.get(i) is None):
                continue

            # get query term at i
            qt = pos_tscore_dict.get(i).term

            # didnt find our term yet
            if (qt != term):
                continue
            else:
                # found term
                return i - pos

        # didn't find term
        return -1


    # Given a dictionary of (key, value) pairs of (term, invertedlist)
    # return a dictionary of (key, value) pairs of (position, ProximityTermScore)
    # for all the terms keyed in mini_index that appear in document docid
    def init_proximity_term_scores(self, mini_index, docid):

        # return dict
        pos_tscore_dict = {}

        # for every term in mini index
        for term in mini_index:

            # get postings of that term
            postings = mini_index.get(term)

            # get index of posting that belongs to docid
            p_idx = self.posting_idx(postings, docid)

            if (p_idx == -1):
                # term does not appear in the document
                continue

            # term does appear in the document; get the posting
            posting = postings[p_idx]

            # assert posting sanity
            assert (posting.tf == len(posting.positions))

            # get positions that the term appears in
            positions = posting.positions

            # for each position the term appears in, create an entry in the
            # pos_tscore_dict dictionary
            for position in positions:
                assert (pos_tscore_dict.get(position) == None)
                # record the term, its position, and 0 base and proximity scores
                pos_tscore_dict[position] = ProximityTermScore(term, position, 0, 0)

        return pos_tscore_dict

    # Given a Query, query
    # returns a set of query terms
    def query_terms_set(self, query):

        # get query string
        querystr = query.querystr

        # split query string into query terms
        query_terms = querystr.split(" ")

        # remove duplicates from the query_terms
        query_terms = set(query_terms)

        return query_terms

    # GIVEN a list of term
    # RETURNS a dictionary of key value pairs (term, termfreqency)
    #
    def termfrequency(self, terms):

        # create a dictionary of (key, vaue), (term, frequency)
        tf_dict = {}
        for term in terms:
            # not added this term's frequency yet ??
            if tf_dict.get(term) is None:
                # add frequency
                tf_dict[term] = terms.count(term)

        return tf_dict


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

