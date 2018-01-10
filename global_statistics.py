## This file provides a global statistics class that facilitates reading and
#  writing global statistics data

import os

## Globals ####################################################################

# String prefixes used to identify unique information in the global statistics
# file

# Prefix to identify total #documents indexed
NID = "N"
# Prefix to identify vocabulary size information
VSID = "VOCABSIZE"
# Prefix to identify corpus size information
CORPUSSIZEID = "CORPUSSIZE"
# Prefix to idenitfy average document length information
AVDLID = "AVDL"
# Prefix to identify document length information
DLID   = "DL"

# Global statistics file name. Any program storing global statistics should
# the in file of name GSFILE
GSFILE  = "global.stat"

## Global Statistics ###########################################################

class GlobalStatistics :

    # Global statistics file path
    gsfile          = ""

    # Total number of documents indexed
    N               = 0
    # Corpus size
    corpus_size     = 0
    # Average document length
    avdl            = 0
    # document lengths of all the documents indexed
    # This is a dictionary of docid and corresponding doc lengths
    doc_lengths     = None

    def __init__(self, gsfile):

        # Reset
        self.reset()

        self.gsfile = gsfile

        # read all information from gsfile
        if (os.path.exists(gsfile)):
            self.read()

    # Deletes all existing statistics
    def reset(self):
        self.gsfile          = ""
        self.N               = 0
        self.corpus_size     = 0
        self.avdl            = 0
        self.doc_lengths     = {}

    # Given : The number of documents indexed, N
    #         The size of the corpus indexed, corpus_size
    #         The avergage lengths of documents indexed, avdl
    #         The document lengths of all documents indexed, doc_lengths
    # Store all information in this global statistics

    def load(self, N, corpus_size, avdl, doc_lengths):

        # load information
        self.N           = N
        self.corpus_size = corpus_size
        self.avdl        = avdl
        self.doc_lengths = doc_lengths

    # Write all global statistics information to self.gsfile file
    def write(self):

        gsf = open(self.gsfile, "w+")

        # write all data to the gs file

        # write N
        gsf.write(NID          + " , " + str(self.N)          + "\n")

        # write corpus size
        gsf.write(CORPUSSIZEID + " , " + str(self.corpus_size) + "\n")

        # write average document length
        gsf.write(AVDLID       + " , " + str(self.avdl)        + "\n")

        # write list of document lengths
        for docid, dl in self.doc_lengths.items():
            gsf.write(DLID + " , " + str(docid) + " , " + str(dl) + "\n")

        # close file
        gsf.close()

    # Read all global statistics information from self.gsfile
    def read(self):

        # Make sure the global statistics file exists
        assert (os.path.exists(self.gsfile));

        gsf = open(self.gsfile, "r")

        # reset all existing statistics
        self.reset()

        # read all information
        for line in gsf.readlines():

            if (line.startswith(NID)):
                # The line informs the total #docs indexed
                self.N = int(self.get_value_csv(line, 1))

            elif (line.startswith(CORPUSSIZEID)):
                # The line informs the size of corupus indexed
                self.corpus_size = int(self.get_value_csv(line, 1))

            elif (line.startswith(AVDLID)):
                # The line informs the average doc length
                self.avdl = float(self.get_value_csv(line, 1))

            elif (line.startswith(DLID)):
                # The line has document length information
                docid = int(self.get_value_csv(line, 1))
                docl  = int(self.get_value_csv(line, 2))
                self.doc_lengths[docid] = docl

        # close file
        gsf.close()

    ## Data fetch functions ###################################################

    # GIVEN a document ID, docid
    # RETURNS the length of the document of id docid
    def document_length(self, docid):

        # Assert inputs
        assert (docid >= 0)

        # Assert that we have the information about length
        assert (len(self.doc_lengths) != 0)

        # Do we have information about the doc?
        assert (self.doc_lengths.get(docid) is not None)
        assert (self.doc_lengths.get(docid) > 0)

        return self.doc_lengths.get(docid)

    # Return the average document length (avdl)
    def get_avdl(self):

        # Assert that we have avdl information
        assert (self.avdl > 0)

        return self.avdl

    # Return N (total number of documents)
    def get_N(self):

        # Assert that we have information about N
        assert (self.N > 0)

        return self.N

    # Return corpus size
    def get_corpussize(self):

        # Assert that we have information about corpus size
        assert (self.corpus_size > 0)

        return self.corpus_size

    ## Utilties ################################################################

    # Given a comma separated string, and a column number
    # Returns the part of the string in the requested column
    def get_value_csv(self, csv_str, column):

        # split string into parts
        csv_parts = csv_str.split(", ")

        # make sure the csv has enough parts
        assert (len(csv_parts) > column)

        return csv_parts[column].strip()

    # print
    def print_stats(self):

        print NID, ", ", self.N
        print CORPUSSIZEID, ", ", self.corpus_size
        print AVDLID, ", ", self.avdl

        for docid, dl in self.doc_lengths.items():
            print DLID, ", ", docid, ", ", dl

