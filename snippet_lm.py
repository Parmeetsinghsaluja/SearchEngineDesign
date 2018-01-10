# This file defines the SnippetLM class that implements all language model
# relevant functions for snippet generation
#
# NOTE / WARNING : Whereever I mention "document" I mean the corpus file and
#                  never the raw document file

from docid_mapper      import DocIDMapper
from corpus_rw         import CorpusRW
from index             import Index
from global_statistics import GlobalStatistics, GSFILE
from stopping          import Stopping
from text_processing   import is_numeric

import os
import math

## Globals #####################################################################

# Consider only the top RQ ranked documents to be relevant to the query terms
# This is used in estimating the relevance language model
RQ = 10

# This factor is the weightage given to the background model
LAMBDA=0.10

# Max extra significant words
MAX_EXTRA_SIG_WORDS = 10

## Snippet LM class ############################################################

class SnippetLM:

    # Path to an indexstore that hosts the index that was used to rank the
    indexstore   = None
    # Path to stopfile
    stopfile     = None

    # inverted index
    invidx       = None

    # global statistics
    global_stats = None

    # document ID mapper
    docid_map    = None

    # reset
    def reset(self):
        self.indexstore   = None
        self.stopfile     = None
        self.invidx       = None
        self.global_stats = None
        self.docid_map    = None

    # constructor
    def __init__(self, indexstore_, stopfile_ = ""):

        self.reset()

        # assert that the indexstore exists
        assert (os.path.exists(indexstore_))
        # assert that stopfile if given exists
        assert (stopfile_ == "" or os.path.exists(stopfile_))

        # set indexstore and stopfile
        self.indexstore = indexstore_
        # set stopfile
        self.stopfile   = stopfile_

        # create index
        self.invidx     = Index(self.indexstore)

        # create global statistics
        self.global_stats = GlobalStatistics(os.path.join(self.indexstore, GSFILE))

        # create a docid mapper
        self.docid_map = DocIDMapper().read(self.indexstore)

    ##
    # Given a string, word, that must have been indexed and
    #       the document id, docid, of the document of interest, and
    # Return the probability of the word appearing in the document
    def p_word_given_document(self, word, docid):

        assert (self.invidx.contains_term(word))

        # get the document's posting for the word
        word_docid_posting = self.invidx.document_posting(word, docid)

        # we need the following,
        # 1. frequency of the word in the document
        # 2. total number of words in the document
        # 3. frequency of the word in the corpus (background model)
        # 4. total number of words in the corpus (background model)

        # 1. frequency of the word in the document
        f_w_d  = 0 if word_docid_posting is None else word_docid_posting.tf

        # 2. total number of words in the document
        dl = self.global_stats.document_length(docid)

        # 3. frequency of the word in the corpus
        f_w_c = self.invidx.corpus_frequency(word)

        # 4. total number of words in the corpus
        cl = self.global_stats.get_N()

        # sanity check
        assert (dl    > 0)
        assert (cl    > 0)
        assert (f_w_c > 0) # cos we know that the index contains the term

        p = (float(1.0 - LAMBDA) * (float(f_w_d) / float(dl))) + \
                  (float(LAMBDA) * (float(f_w_c) / float(cl)))

        return p

    ## Weighing terms ##########################################################

    ##
    # Given: a list of words,
    #        a list of query terms
    #        a list of ranked documents
    # Returns a list of tuple where each tuple is in format (word, score)
    #
    # Formula:
    # weight/score word W according to the following formula
    #               .--                              --.
    #               |                 n                |
    #       SUM     | log(P(W|D)) +  SUM log(P(qi|D))  |
    #   D belongs R |                i=1               |
    #               '--                              --'
    #
    # where D represents a document, R represents the relevant set (this is
    # approximated to be the top RQ ranked documents), qi represents the ith query term
    #
    def score_words_by_relevance(self, words, query_terms, ranked_docs):

        # initialize return tuple
        word_score_tuple = []

        # filter query terms that appear in the inverted index
        query_terms = filter(lambda qt: self.invidx.contains_term(qt), query_terms)

        # We know what all relevant documents are. and we know all the query terms
        # We can straight away calculate the
        #   n
        #  SUM log(P(qi|D)),  for all the top RQ documents
        #  i=1
        #
        p_q_d_dict = {}
        for i in range(0, min(RQ, len(ranked_docs))):

            # get docid
            docid = ranked_docs[i].docid

            # Compute all P(qi|D)
            p_qi_d = map(lambda q: self.p_word_given_document(q, docid), query_terms)
            # Sum all log(P(qi|D))
            p_q_d = reduce(lambda x, y: x + math.log(y), p_qi_d)

            # record score
            p_q_d_dict[docid] = p_q_d

        # Compute log(P(W|D)) and add it to second part of the sum in the formula.
        # Computed above for all words
        for w in words:

            w_score = 0

            # for all top RQ documents
            for i in range(0, min(RQ, len(ranked_docs))):

                # get document id of the ith document
                docid = ranked_docs[i].docid

                # Get prob. of the word given document (left term in formula)
                p_w_d = math.log(self.p_word_given_document(w, docid))

                w_score = w_score + float(p_w_d) + float(p_q_d_dict[docid])

            # record score
            word_score_tuple.append((w, w_score))

        # penalize commonly occuring terms through out the corpus
        #norm_word_score_tuple = []
        #for wst in word_score_tuple:
        #    # word
        #    word = wst[0]
        #    # find inverse document frequency
        #    word_df = len(self.invidx.postings(word))
        #    word_idf = 1.0/float(word_df)
        #    # since the scores are negative, do a 1 - word_icf
        #    norm_word_score_tuple.append((wst[0], wst[1] * word_df))

        #assert (len(norm_word_score_tuple) == len(words))

        #return norm_word_score_tuple
        return word_score_tuple

    ## General utils ###########################################################

    ##
    # Given a list of top ranked documents, ranked_docs
    #       an integer n,
    #       path to the indexstore used to rank the documents
    # Returns, the SET of words in the top n ranked documents
    #
    def wordset_in_topN(self, ranked_docs, n):

        # Input check
        assert (n >= 0)

        # set of words in relevant set
        words = []

        # Get set of words in each of the top n documents
        for i in range(0, min(len(ranked_docs), n)):

            # get document ID of the ith ranked document
            docid = ranked_docs[i].docid

            # get path to the ith ranked document/corpusfile
            cfpath = DocIDMapper().corpusfpath(docid, self.docid_map)

            # get contents of the ith ranked document
            dcontents = CorpusRW().corpus_content(cfpath)

            # split content of the document into words
            words = words + dcontents.split(" ")

        # return a set of words
        return set(words)

    ## Significant words (snippet generation) ##################################

    ##
    # Given a list of query terms, query_terms, and
    #       a list of ranked documents (DocRankTREC), and
    # Returns a list of significant words
    #
    def significant_words(self, query_terms, ranked_docs = []):

        # do we even have anything to do ?
        if (query_terms == []):
            # nothing to do
            return query_terms

        if (ranked_docs == []):
            # nothing to do
            return query_terms

        # we have everything to do!!

        # get set of words in relavant documents
        words = self.wordset_in_topN(ranked_docs, RQ)

        # stop words in wordset
        if (self.stopfile != ""):
            words_text = " ".join(words)
            words_text = Stopping(self.stopfile).stop(words_text)
            words      = set(words_text.split(" "))

        # filter words that are all numbers; we dont want to focus on numbers
        words = filter(lambda w: not is_numeric(w), words)

        # compute a list of tuples where the first term in the tuple is the word
        # and the second term in the tuple is the weight
        # weight words as per relevance model
        word_weight_tuples = self.score_words_by_relevance(words, query_terms, ranked_docs)

        # sort weighted words by their scores; Highest first
        word_weight_tuples.sort(key=lambda t: t[1], reverse=True)

        # Initialize return sig_words
        sig_words = []

        # all query words are definitely significant
        for qt in query_terms:
            sig_words.append(qt)

        # get top MAX_EXTRA_SIG_WORDS words, that are not query words, from
        # word_weight_tuples
        for wwt in word_weight_tuples:

            # have we added enough ??
            if (len(sig_words) - len(query_terms) > MAX_EXTRA_SIG_WORDS):
                break

            # weighted word
            w = wwt[0]
            # check if the word is already added. could be a query word that we
            # added already
            if (w not in sig_words):
                sig_words.append(w)

        return sig_words
