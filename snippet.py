# This file implements a snippet class that generates snippets for ranked
# documents

from docrank_trec    import DocRankTREC
from query           import Query
from cacm_parser     import is_cacm_doc, cacm_content
from docid_mapper    import DocIDMapper
from text_processing import process_text, clean_extraneous_whitespace
from snippet_lm      import SnippetLM

import os
import re
import sys

## Globals #####################################################################

# Number of words in snippet
NSNIPPETWORDS = 50

## Snippet class ###############################################################

class Snippet:

    # ranked_results represented by a list of DocRankTREC
    ranked_docs     = []
    # query for which the documents were ranked
    query           = None

    # Inverted index store that was used to rank the documents
    indexstore      = None

    # stopfile to stop queries before matching with document for snippet gen
    stopfile        = None

    # Snippet language model utilites
    snippet_lm      = None

    # reset
    def reset(self):
        # initialize class variables
        self.ranked_docs     = []
        self.query           = None
        self.indexstore      = None
        self.stopfile        = None
        self.snippet_lm      = None

    # Constructor
    def __init__(self, ranked_docs_, query_, indexstore_, stopfile_, snippet_lm_):

        #reset
        self.reset()

        # assert inputs
        assert (query_ is not None)
        assert (os.path.exists(indexstore_))
        assert (stopfile_ == "" or os.path.exists(stopfile_))

        # Initialize results, query and invidx and stopfile
        self.ranked_docs = ranked_docs_
        self.query       = query_
        self.indexstore  = indexstore_
        self.stopfile    = stopfile_
        self.snippet_lm  = snippet_lm_

        # assert that all rankings are about the supplied query
        assert (all(map(lambda drt: drt.qid == self.query.qid, self.ranked_docs)))

    # Return a dictionary, keyed by document ID and whose value is a snippet
    # string
    def snippets(self):

        # intialize return dict (keyed by docid and value is snippet string)
        doc_snippets = {}

        # get list of docids for which we have to generate a snippet
        docids = map(lambda rd: rd.docid, self.ranked_docs)

        # get processed and stopped query string
        querystr = process_text(self.query.querystr, self.stopfile)

        # get queryterms
        query_words = querystr.split(" ")

        # get signigicant words from a relevance language model, considering the
        # the top ranked documents
        sig_words = self.snippet_lm.significant_words(query_words, self.ranked_docs)
        #sig_words = query_words

        #print "------------------ QUERY REFINED --------------------------"
        #print "Query - ", querystr
        #print query_words
        #print sig_words
        #print "-----------------------------------------------------------"

        # get docid map; maps docid to corpusfile and the document file
        docid_map = DocIDMapper().read(self.indexstore)

        # for each document
        for docid in docids:

            # document of id docid
            docfpath = DocIDMapper().docfpath(docid, docid_map)

            # get doc sentences
            doc_sentences = self.sentences(docfpath)

            # we want our sentences to be separated by just spaces
            doc_sentences = map(lambda s: clean_extraneous_whitespace(s), doc_sentences)

            # get significant segments of sentences
            doc_segments  = map(lambda s: self.sig_segment(s, sig_words), doc_sentences)

            # text process document segments
            pdoc_segments = map(lambda s: process_text(s), doc_segments)

            # score segments
            doc_segment_scores = map(lambda seg: self.segment_score(seg, sig_words), pdoc_segments)

            # we got all information, lets generate the snippet
            snippet_str = self.snippet(os.path.basename(docfpath), doc_segments, doc_segment_scores)

            # highlight query terms in snippet
            snippet_str = self.highlight(query_words, snippet_str)

            # store snippet
            doc_snippets[docid] = snippet_str

        return doc_snippets

    # Given a path to an indexed document
    # Return a list of sentences in the document.
    def sentences(self, docfpath):

        # get contents of the document
        dcontents = cacm_content(docfpath)

        # split doc into multiple paragraphs
        paragraphs = re.split("\n\n", dcontents)

        # sentences
        ret_sentences = []

        # for each paragraph
        for paragraph in paragraphs:
            # split paragraph into sentences
            # hypothesize that a whitespace after a period the marks end of a sentence
            ret_sentences = ret_sentences + re.split('\.\s', paragraph)

        # return sentences
        return ret_sentences

    # Given a raw document sentence, and a list of significant words
    # Return the largest segment of the sentence bounded by significant words
    def sig_segment(self, sentence, sig_words):

        # break sentence into words
        words = sentence.split(" ")

        # start and end segment index marker
        start_seg = -1
        end_seg   = -1

        # find index of the first appearance of a significant word
        for idx in range(0, len(words)):
            # text process this word to compare with query
            pword = process_text(words[idx])

            # is it a significant word ?
            if (pword in sig_words):
                start_seg = idx
                break

        # find index of the last appearance of a significant word
        for idx in range(len(words) - 1, -1, -1):
            # text process this word to compare with query
            pword = process_text(words[idx])

            if (pword in sig_words):
                end_seg = idx
                break

        assert (start_seg <= end_seg)

        # no significant words in the sentence ?
        if (start_seg == -1 and end_seg == -1):
            return ""

        # always include a couple of words on either sides of the segment
        # for context
        start_seg = 0 if start_seg - 3 < 0 else start_seg - 3
        return " ".join(words[start_seg : end_seg + 4])

    # Given a sentence segment bounded by query terms, and a list of significant
    # words
    # Returns the score for the document according to Luhns paper
    #         "The Automatic Creation of Literature Abstracts"
    def segment_score(self, segment, sig_words):

        # empty segment ?
        if (segment == ""):
            return 0

        # split segment into words
        seg_words = segment.split(" ")

        # count how many words are significant in segment
        sig_word_count = len(filter(lambda w: w in sig_words, seg_words))

        # total number of words in the segment
        seg_words_count = len(seg_words)

        # return score
        return float(float(sig_word_count * sig_word_count) / float(seg_words_count))

    # Given a list of raw document segments, and
    #       a list of corresponding scores of each document segment
    # Returns a snippet of the document
    def snippet(self, docname, segments, scores):

        # assert all lists have same lenght
        assert (len(segments)  == len(scores))

        # macros for sane access of score/snippet tuple made up of
        # (segment index, document segment, document segment score)
        SEGIDX      = 0
        DOCSEG      = 1
        DOCSEGSCORE = 2

        # create a list of tuples of
        # (segment index, document segment, document segment score)
        score_tuples = []
        for sidx in range(0, len(segments)):
            score_tuples.append((sidx, segments[sidx], scores[sidx]))

        # sort score tuples by document score; highest score first
        score_tuples.sort(key=lambda t: t[DOCSEGSCORE], reverse=True)

        # snippet tuples; get top score tuples that should be a part of snippet
        snippet_tuples   = []
        words_in_snippet = 0

        for score_tuple in score_tuples:

            if (words_in_snippet > NSNIPPETWORDS):
                # We have enough sentence segments to generate snippet
                break
            else:

                if score_tuple[DOCSEGSCORE] == 0.0:
                    # dont even bother
                    continue

                # This tuples goes into the snippet
                snippet_tuples.append(score_tuple)
                # Update running count of words in snippet; add segment length
                # to words_in_snippet
                words_in_segment = len(score_tuple[DOCSEG].split(" "))
                words_in_snippet = words_in_snippet + words_in_segment

        # Cool! got snippet tuples. we want to display snippet sentences in the
        # order of appearance in the document
        # sort tuples by sentence idx
        snippet_tuples.sort(key=lambda t: t[SEGIDX])

        # construct snippet string
        snippet_str = ""
        for snippet_tuple in snippet_tuples:
            snippet_str = snippet_str + snippet_tuple[DOCSEG] + " ... "

        # cherry on top. add docname
        snippet_str = docname + "\n" + snippet_str.strip() + "\n"

        # return snippet string
        return snippet_str


    # Given a list of significant words and a text string, promote to uppercase,
    # all case-insensitive appearances of the significant words
    def highlight(self, sig_words, text):

        # split text into words
        words = text.split(" ")

        # highlight
        for widx in range(0, len(words)):
            # process word at index widx
            pword = process_text(words[widx])
            # is the word a significant word ?
            if pword in sig_words:
                # fold to uppercase
                words[widx] = words[widx].upper()

        # join and return
        return (" ").join(words)

## Snippet generation functions ################################################

##
# GIVEN: a list of Query (in query.py), query_lst, and
#        a list of docrank objects, describing the ranking the ranking for all
#        queries in the, query_lst,
#        the path to where the index used in the search is stored
#        the path to a stopfile (optional) and
# Returns a dictionary of (key, value) (queryid, ranked snippet list) pairs
#
def get_snippets(query_lst, docranks, indexstore, stopfile = ""):

    # input check
    assert (os.path.exists(indexstore))
    assert (stopfile == "" or os.path.exists(stopfile))

    # return dictionary
    qid_snippets_dict = {}

    # TODO: Creating a language model here is UGLY !! Make this better
    # We are using a language model to generate snippets
    snippet_lm = SnippetLM(indexstore, stopfile)

    # For every query, print snippets
    for q in query_lst:

        # get docranks, that about this query only
        q_docranks = filter(lambda drt: drt.qid == q.qid, docranks)

        # Takes way too long to generate snippets... Print progress to terminal
        print "\rGenerating snippets for query ID %d" % q.qid, 
        sys.stdout.flush()

        # Get a dictionary of key-value (docid, snippet string)
        doc_snippets = Snippet(q_docranks, q, indexstore, stopfile, snippet_lm).snippets()

        # ordered snippet list
        snippet_lst = []

        for docrank in q_docranks:

            # get docid that this result string is talking about
            docid = docrank.docid

            # Make sure we have a snippet for this document
            assert (doc_snippets.get(docid) is not None)
            # add document's snippet to list
            snippet_lst.append(doc_snippets[docid])

        # update qid_snippets_dict
        qid_snippets_dict[q.qid] = snippet_lst

    return qid_snippets_dict

##
# GIVEN: a list of Query (in query.py), query_lst, and
#        a list of docrank objects, describing the ranking the ranking for all
#        queries in the, query_lst,
#        the path to where the index used in the search is stored
#        the path to a stopfile (optional) and
#        a boolean value specifying if the result display should be interactive
# Displays snippets of the ranked document
#
def display_snippets(query_lst,
                     docranks,
                     indexstore,
                     stopfile = "",
                     interactive = False):

    # input check
    assert (os.path.exists(indexstore))
    assert (stopfile == "" or os.path.exists(stopfile))

    # For every query, print snippets
    for q in query_lst:

        # get docranks, that about this query only
        q_docranks = filter(lambda drt: drt.qid == q.qid, docranks)

        # Get a dictionary of key-value (docid, snippet string)
        doc_snippets = Snippet(q_docranks, q, indexstore, stopfile).snippets()

        # Print query
        print "================================================================"
        print "Query : ", q.querystr

        # Print snippets
        for docrank in q_docranks:

            # get docid that this result string is talking about
            docid = docrank.docid

            # Mark separation
            print "----------------------------------------------------------------"

            # Make sure we have a snippet for this document
            assert (doc_snippets.get(docid) is not None)
            # print document's snippet
            print doc_snippets[docid]

            # Mark separation
            print "----------------------------------------------------------------"

            # Ask for user input for continuing display
            if (q_docranks.index(docrank) % 5 == 4 and interactive):
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

