# This file provides utilities to read and write corpus files

from cacm_parser import is_cacm_doc

import os

## NOTE ########################################################################

# Corpus files are created and stored in the following format.
# The path to the document from which the corpus file was created is the first
# line in the corpus file.
# The rest of the lines correspond to the corpus file content

## Globals #####################################################################

# Corpus extension
CORPUS_EXTN = ".txt"

## Utilities ###################################################################

# Given the name of a file
# return true iff the file is a corpus file
def is_corpus_file(fname):

    return fname.endswith(CORPUS_EXTN)

# Given the name of a document file
# Returns the name of the corpus file that represents the cleaned up version
# of the document
def corpus_filename(docfname):

    return docfname + CORPUS_EXTN

## CorpusRW ####################################################################

# class to read/write corpus
class CorpusRW:

    # Given the cleaned up content of a document, and
    #       the name of the corpus file in which the content should be stored
    #       the path where all the cleaned up contents must be stored,
    # Store the cleaned up content in the path specified
    def store_corpus(self, content, corpus_fname, corpusstore):

        assert (is_corpus_file(corpus_fname))
        assert (os.path.exists(corpusstore))

        # corpus file path to store
        corpus_fpath = os.path.join(corpusstore, corpus_fname)

        # open corpus file
        cf = open(corpus_fpath, "w+")

        # write doc content
        cf.write(content)

        cf.close()

    # Given the path to a corpus file
    # Returns the contents of the corpus file
    def corpus_content(self, cfpath):

        assert (os.path.exists(cfpath))
        assert (is_corpus_file(os.path.basename(cfpath)))

        # open corpus file
        cf = open(cfpath, "r")

        # Get file contents
        content = cf.read()

        # close corpus file
        cf.close()

        return content

################################################################################
