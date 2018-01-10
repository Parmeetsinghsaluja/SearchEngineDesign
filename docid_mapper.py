## This file provides read/write functions retrieve/store document ID to file
#  map information

from corpus_rw   import is_corpus_file
from cacm_parser import is_cacm_doc

import os
import shutil

## Globals #####################################################################

# Default document ID mapper file name
DOCIDMAPPER = "docid.map"

## DocID mapper ################################################################

class DocIDMapper:

    # given a dictionary of key, value pairs of where the key is the
    #       document ID and the value is a tuple of corpus file path and
    #       document file path
    # Store the mapping to a file
    def store(self, mapstore, docid_map):

        # assert we have a mapstore
        assert (os.path.exists(mapstore))

        # create docid mapper file in mapstore
        docidmapf = open(os.path.join(mapstore, DOCIDMAPPER), "w+")

        for docid in docid_map:
            # Write in the format
            # documentid , corpusfilepath , documentfilepath
            docidmapf.write(str(docid)              + " , " + \
                            docid_map.get(docid)[0] + " , " + \
                            docid_map.get(docid)[1] + "\n")

        docidmapf.close()

    # given the mapstore, where DOCIDMAPPER file is stored
    # returns a dictionary of key, value pairs of where the key is the
    #         documentID and the value is a tuple of corpus file path and
    #         document file path
    def read(self, mapstore):

        # assert that there is a mapstore
        assert (os.path.exists(mapstore))
        assert (os.path.exists(os.path.join(mapstore, DOCIDMAPPER)))

        # path to the docid map file
        mapfpath = os.path.join(mapstore, DOCIDMAPPER)

        # docid dict
        docid_map = {}

        # read mapfile lines
        map_lines = []
        with open(mapfpath, "r") as f:
            map_lines = f.readlines()

        # read each map line and populate docid_map
        for map_line in map_lines:

            # split map_line into parts
            map_line_parts = map_line.split(",")
            assert (len(map_line_parts) == 3)

            docid       = int(map_line_parts[0].strip())
            corpusfpath = map_line_parts[1].strip()
            docfpath    = map_line_parts[2].strip()

            # store in docid_map
            docid_map[docid] = (corpusfpath, docfpath)

        return docid_map

    # Given a document id, and
    #       a dictionary of key, value pairs of where the key is the
    #       documentID and the value is a tuple of corpus file path and
    #       document file path
    # Returns the corpus file path of the document id
    def corpusfpath (self, doc_id, docid_map):

        assert (docid_map[doc_id] is not None)

        # This is where we store the corpus file path
        cfpath = docid_map[doc_id][0];
        assert (is_corpus_file(os.path.basename(cfpath)))

        return cfpath

    # Given a document id, and
    #       a dictionary of key, value pairs of where the key is the
    #       documentID and the value is a tuple of corpus file path and
    #       document file path
    # Returns the cacm document file path of the document id
    def docfpath (self, doc_id, docid_map):

        assert (docid_map[doc_id] is not None)

        # This is where we store the doc file path
        dfpath = docid_map[doc_id][1];
        assert (is_cacm_doc(os.path.basename(dfpath)))

        return dfpath

    # Given a source mapstore (a folder where a file DOCIDMAPPER exists) and
    # a destination mapstore (a folder where we want to copy the DOCIDMAPPER
    # file to)
    # Copy DOCIDMAPPER from source folder to destination folder
    def copy_docidmapper(self, src_mapstore, dst_mapstore):

        assert (os.path.exists(src_mapstore))
        assert (os.path.exists(dst_mapstore))

        # docid map source and destination file paths
        mapsfpath = os.path.join(src_mapstore, DOCIDMAPPER)
        mapdfpath = os.path.join(dst_mapstore, DOCIDMAPPER)

        assert (os.path.exists(mapsfpath))
        shutil.copy(mapsfpath, mapdfpath)

################################################################################
