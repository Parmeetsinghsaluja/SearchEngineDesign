# This file contains Stopping class, that one can use to stop words in a
# text, given a stopfile

import os

## Globals #####################################################################

# Separator for terms in stopfile
# WARNING: WHEN CHANGING THIS, CHANGE THE DOCUMENTATION AS WELL
STOPFILE_DELIMITER = '\n'

## Stopping class ##############################################################

## Class used to stop words in a text, given a stopfile
class Stopping:

    # Path to a stopfile
    stopfile  = ""
    # List of stopwords in the stopfile
    stopwords = []

    # reset
    def reset(self):
        stopfile  = ""
        stopwords = []

    # constructor
    def __init__(self, stopfile_):

        # reset
        self.reset()

        # set stopfile
        self.stopfile = stopfile_

        # Stopfile not given
        if (self.stopfile == ""):
            return

        # Stopfile given. Check existence
        assert (os.path.exists(self.stopfile))

        with open(self.stopfile, "r") as f:
            # TODO: Make use of STOPFILE_DELIMITER more generic
            assert (STOPFILE_DELIMITER == "\n")
            self.stopwords = f.readlines();
            self.stopwords = map(lambda w: w.strip(), self.stopwords)

        return

    ## Utitility to stop words in the text that appears in the stopwords
    def stop(self, text):

        # split text in to words
        words = text.split(" ")

        # stop words
        words = filter(lambda w: w not in self.stopwords, words)

        # rearrange text
        return (" ").join(words)

################################################################################
