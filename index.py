# This file holds classes that define the various components of an inverted
# index and the inverted index itself

import os
from   corpus_rw   import is_corpus_file
from   cacm_parser import is_cacm_doc

## Globals #####################################################################

# Default index file name
INDEXFILE = "index.idx"

## Term ########################################################################

# a term is a string that is the key in the inverted index dictionary

## Posting #####################################################################

# document IDs and other related information like,
#   i. term frequency in the document
#  ii. proximity information etc
class Posting:

    # Document ID; A valid document ID is always non negative
    docid     = -1
    # Frequency of the term in the document. a valid tf is always non negative
    tf        = -1
    # Positions that the term appears in the document; Must be sorted; Always !!
    positions = []
    # any other information goes here

    # constructor
    def __init__(self, docid_, tf_, positions_):

        self.reset()

        assert (tf_ > 0)
        assert (positions_ is not None)
        assert (positions_ != [])

        self.docid     = docid_
        self.tf        = tf_
        self.positions = positions_

    # reset
    def reset(self):
        self.docid     = -1
        self.tf        = -1
        self.positions = []

    # returns the state of this positing object as a string
    def posting_as_string(self):
        return (str(self.docid) + ":" + str(self.tf))

## Index #######################################################################

# Inverted Index
# A dictionary of key value pairs where,
# the key is Term.t, and
# value is a list of posting
class Index:

    # index store. Where index and global statistics is stored
    indexstore = ""

    # path to the index file. Usually it is just os.path.join(indexstore, INDEXFILE)
    indexfile = ""

    # dictionary to hold key value pairs of terms and posting dictionary
    idxdict = {}

    # constructor
    def __init__(self, indexstore):

        # reset
        self.reset()

        # Set index variables
        self.indexstore = indexstore
        self.indexfile  = os.path.join(indexstore, INDEXFILE)

        # Already existing index ?
        if (os.path.exists(self.indexfile)):
            self.populate()

        # Indexfile does not exist. Does the indexstore exist ? if not create one
        if (not os.path.exists(indexstore)):
            os.makedirs(indexstore)

        return

    # reset
    def reset(self):
        self.indexstore = ""
        self.indexfile  = ""
        self.idxdict    = {}

    ## Predicates ##############################################################

    # given a string, that is an index term,
    # true if and only if this index has that term
    def contains_term(self, t):
        return (self.idxdict.get(t) is not None)

    ## Term/Posting access/search methods ######################################

    # given a string, that is an index term,
    # returns the list of posting mapped to the term
    def postings(self, t):
        assert (self.idxdict.get(t) is not None)
        return self.idxdict[t]

    # given a string, that is a term, and a document id
    # returns the posting of the document if present in the term's posting list
    # returns None otherwise
    def document_posting(self, t, docid):

        assert (isinstance(docid, int))
        assert (self.contains_term(t))

        postings = self.idxdict[t]

        pidx = self.posting_idx(postings, docid)

        if pidx == -1:
            return None
        else:
            return postings[pidx]

    # given a list postings sorted by docid and a docid,
    # returns the index of the posting of the docid
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

    ## Insert methods ##########################################################

    # given a string, that is a term and a posting p
    # add the posting to the term's posting list in the index
    # preseve sorted order every where.
    def insert_posting(self, t, p):

        assert (self.contains_term(t))

        postings = self.idxdict[t]

        insert_idx = 0

        # search for the index of a posting of docid just smaller than p
        # search from the end. the indexer is likely to add documents in the
        # increasing order of the document id
        for pidx in range(len(postings) - 1, -1, -1):
            if postings[pidx].docid < p.docid:
                insert_idx = pidx + 1
                break

        postings.insert(insert_idx, p)

        # update index
        self.idxdict[t] = postings

    # given a string, term, the term's position in the document and a document ID
    # add the document ID as a posting to the term in the index
    def update(self, t, tpos, docid):

        assert(isinstance(docid, int))
        assert(tpos >= 0)

        if (not self.contains_term(t)):
            self.idxdict[t] = []

        dposting = self.document_posting(t, docid)

        if (dposting is not None):
            # posting for this docid already exists
            postings        = self.idxdict[t]
            # posting index
            pidx            = self.posting_idx(postings, docid)
            # update postings
            postings[pidx]  = Posting(docid,                         \
                                      postings[pidx].tf + 1,         \
                                      postings[pidx].positions + [tpos])
            # update index
            self.idxdict[t] = postings
        else:
            # docid does not have a posting for that term
            self.insert_posting(t, Posting(docid, 1, [tpos]))

        return

    ## Statistics ##############################################################

    # Given an indexed term t, returns the frequency of the term in the corpus
    def corpus_frequency(self, term):
        assert (self.contains_term(term))
        return reduce(lambda tf, p: tf + p.tf, self.postings(term), 0)

    # Returns the term frequencies of all the terms in the index in a dictionary
    def term_frequencies(self):

        tf_table = {}

        # For every term in the index
        for t in self.idxdict:
            # Sum how may times the term appears in every posting
            tf = reduce((lambda tf, p: tf + p.tf), self.idxdict[t], 0)
            # record term frequency in the table
            tf_table[t] = tf

        return tf_table

    # returns the document frequencies of all the terms in the index in a dict
    def document_frequencies(self):

        df_table = {}

        # For every term in the index
        for t in self.idxdict:
            # get a list of all docid
            docids = map(lambda p: p.docid, self.idxdict[t])
            # record the documents in the table
            df_table[t] = docids

        return df_table

    ## Sanity check methods ####################################################

    # Sanity check the index
    def sanity_check(self):

        for term in self.idxdict:
            postings = self.idxdict[term]

            for i in range(0, len(postings) - 1):
                assert(postings[i].docid >= 0)
                assert(postings[i].docid < postings[i+1].docid)
                assert(postings[i].tf > 0)
                assert(postings[i].positions == sorted(postings[i].positions))
                assert(len(postings[i].positions) == postings[i].tf)

    ## Index read/write methods ################################################

    # populate the index with the contents of the indexfile
    def populate(self):

        # assert the file exists
        assert (os.path.exists(self.indexfile))

        with open(self.indexfile, "r") as f:
            idxf_lines = f.readlines()

        for line in idxf_lines:

            assert (line.strip() != "")
            assert ('|' in line)
            assert (line.strip() != "" and '|' in line)
            line_parts = line.split('|')

            # the line must have 2 parts. a term and a posting info
            assert(len(line_parts) == 2)

            term        = line_parts[0]
            postinginfo = line_parts[1]

            # A postinginfo is delimited into many parts by comma. The format
            # of each part is as follows,
            # docid tf tpos1 tpos2 tpos3 ... tpostf
            posting_strings = postinginfo.split(',')

            # create an empty entry of the term
            self.idxdict[term] = []

            # convert each posting string into a Posting
            for posting_string in posting_strings:

                # split posting string into parts
                posting_parts = posting_string.strip().split(" ")

                # first part of posting is docid
                docid = int(posting_parts[0])
                # second part is tf
                tf    = int(posting_parts[1])
                # all other parts are term positions
                assert (len(posting_parts) == tf + 2)

                # list of term positions in sorted order
                positions = []
                for part in posting_parts[2:]:
                    positions.append(int(part))

                # lets add this posting
                postings = self.idxdict[term]
                postings.append(Posting(docid, tf, positions))
                self.idxdict[term] = postings

        self.sanity_check()

    # store index to file
    def store(self):

        assert (not os.path.exists(self.indexfile))

        self.sanity_check()

        idxf = open(self.indexfile, "w+")

        # Get sorted index
        idx_sorted = sorted(self.idxdict.items(), key = lambda x: x[0])

        for term_posting in idx_sorted:
            # get term
            s = term_posting[0] + "|"
            # get all postings of that term
            for p in term_posting[1]:
                s = s + str(p.docid) + " " + str(p.tf) + " "
                # add position information
                for pos in p.positions:
                    s = s + str(pos) + " "
                # demarcate postings by comma
                s = s + ", "

            # TODO: PLEASE FIND A BETTER WAY !
            # remove the last ", "
            s = s[:-2] + ' ' + s[-1:]

            # strip
            s = s.strip()
            # add a newline so that it does not look horrendoes in the index file
            s = s + "\n"

            idxf.write(s)

        idxf.close()

    # store term frequencies in the input file, tffile
    def store_term_frequencies(self, tffile):

        assert (not os.path.exists(tffile))

        tf_table = self.term_frequencies()

        # Sort term frequency table by the values/frequencies
        tf_table_sorted = sorted(tf_table.items(), key=lambda x: x[1], reverse=True)

        # Map every tf tuple to a string
        tf_table_sorted_strs = map(lambda tf: tf[0] + " - " + str(tf[1]), tf_table_sorted)

        # Join all tf strings
        tf_table_str = "\n".join(tf_table_sorted_strs)

        # Write tf to file
        with open(tffile, "w+") as f:
            f.write(tf_table_str)

    # store document frequencies in the input file, dffile
    def store_document_frequencies(self, dffile):

        assert (not os.path.exists(dffile))

        df_table = self.document_frequencies()

        # Sort document frequency by the keys/terms
        df_table_sorted = sorted(df_table.items(), key=lambda x: x[0])

        # Map every df tuple to a string
        df_table_sorted_strs = map(lambda df: df[0]             + " " + \
                                              str(tuple(df[1])) + " " + \
                                              str(len(df[1]))   + "\n", \
                                   df_table_sorted)

        # Join all df strings
        df_table_str = "\n".join(df_table_sorted_strs)

        with open(dffile, "w+") as f:
            f.write(df_table_str)

    # print the index
    def print_index(self):

        self.sanity_check()

        print "------------------------------ INDEX ---------------------------"

        for term in self.idxdict:
            s = term + " - "
            postings = self.idxdict[term]
            for p in postings:
                s  = s + p.posting_as_string() + " "
            print s

        print "----------------------------------------------------------------"

    ## Miscellaneous ###########################################################

    # GIVEN a list of terms
    # RETURNS a dictionary of key value pairs of (term, invlist)
    #
    def minindex(self, terms):

        # initialize return dict
        midx = {}

        for t in terms:
            # Term not seen yet
            if (midx.get(t) is None):
                midx[t] = self.postings(t)

        return midx

    # GIVEN a list of terms
    # RETURNS a set of documents that contain the term
    #
    def docids_with_terms(self, terms):

        # Create empty document set
        docids = set()

        # Convert the list of terms to a set to deduplicate
        terms = set(terms)

        # filter terms not appearing in the index
        terms = filter(lambda t: self.contains_term(t), terms)

        # for each term in terms
        for t in terms:

            # for each posting in term postings
            for posting in self.postings(t):

                # get docid
                docid = posting.docid
                assert (docid >= 0)

                docids.add(docid)

        return docids

    def term(self):
        return self.idxdict.keys()

## Tests #######################################################################

# tests for posting_idx
def test_postingidx():

    plst1 = [Posting(0)]
    plst2 = [Posting(0), Posting(1)]
    plst3 = [Posting(0), Posting(1), Posting(2)]
    plst4 = [Posting(0), Posting(1), Posting(2), Posting(3)]
    plst5 = [Posting(0), Posting(1), Posting(2), Posting(3), Posting(4)]
    plst6 = [Posting(0), Posting(1), Posting(2), Posting(3), Posting(4), Posting(5)]

    idx = Index()

    assert (idx.posting_idx(plst1, 0) == 0)
    assert (idx.posting_idx(plst2, 0) == 0)
    assert (idx.posting_idx(plst3, 0) == 0)
    assert (idx.posting_idx(plst4, 0) == 0)
    assert (idx.posting_idx(plst5, 0) == 0)
    assert (idx.posting_idx(plst6, 0) == 0)
    assert (idx.posting_idx(plst2, 1) == 1)
    assert (idx.posting_idx(plst3, 1) == 1)
    assert (idx.posting_idx(plst4, 1) == 1)
    assert (idx.posting_idx(plst5, 1) == 1)
    assert (idx.posting_idx(plst6, 1) == 1)
    assert (idx.posting_idx(plst3, 2) == 2)
    assert (idx.posting_idx(plst4, 2) == 2)
    assert (idx.posting_idx(plst5, 2) == 2)
    assert (idx.posting_idx(plst6, 2) == 2)
    assert (idx.posting_idx(plst4, 3) == 3)
    assert (idx.posting_idx(plst5, 3) == 3)
    assert (idx.posting_idx(plst6, 3) == 3)
    assert (idx.posting_idx(plst5, 4) == 4)
    assert (idx.posting_idx(plst6, 4) == 4)
    assert (idx.posting_idx(plst6, 5) == 5)

    assert (idx.posting_idx(plst1, 89) == -1)
    assert (idx.posting_idx(plst2, 89) == -1)
    assert (idx.posting_idx(plst3, 89) == -1)
    assert (idx.posting_idx(plst4, 89) == -1)
    assert (idx.posting_idx(plst5, 89) == -1)
    assert (idx.posting_idx(plst6, 89) == -1)

    assert (idx.posting_idx(plst1, -3) == -1)
    assert (idx.posting_idx(plst2, -3) == -1)
    assert (idx.posting_idx(plst3, -3) == -1)
    assert (idx.posting_idx(plst4, -3) == -1)
    assert (idx.posting_idx(plst5, -3) == -1)
    assert (idx.posting_idx(plst6, -3) == -1)

    print "Binary search on index pass"
