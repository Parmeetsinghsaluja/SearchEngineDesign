## This file defines a data store that represents a query and provides utilities
#  that can read a queries from files

import os
from bs4 import BeautifulSoup
from text_processing import process_text

## Query #######################################################################

class Query:

    # Query ID
    qid   = -1
    # Query
    querystr = ""

    # Constructor
    def __init__(self, qid_, querystr_):

        # reset
        self.reset()

        self.qid      = qid_
        self.querystr = querystr_

    # Reset
    def reset(self):
        self.qid      = -1
        self.querystr = ""

## Utilities ###################################################################

## GIVEN a query file, containing lines of space separated queryid and query
#  RETURNS a list of Query
def queries (queryfile):

    # Input check
    assert (os.path.exists(queryfile))

    # Initialize list of queries
    query_lst = []

    # Read all lines in query file
    query_lines = []
    with open(queryfile) as f:
        query_lines = f.readlines()

    # every line is a query
    for query_line in query_lines:

        # query line parts
        ql_parts = query_line.split(" ", 1)

        # assert there really is 2 parts
        assert (len(ql_parts) == 2)

        # queryid and querystr
        qid      = int(ql_parts[0].strip())
        querystr = ql_parts[1].strip()

        # build query
        query_lst.append(Query(qid, querystr))

    # return
    return query_lst

## GIVEN a cacm query file in an xml format
#  Returns a list of Query
def cacm_queries(queryfile):

    # Input check
    assert (os.path.exists(queryfile))

    # Initialize list of queries
    querylst = []

    # Soup the xml query file
    with open(queryfile, "r") as qf:
        # The query file is in XML with multiple roots. BeautifulSoup's
        # xml parser is unable to find multiple roots. The html parser works
        # nicely for this purpose
        query_soup = BeautifulSoup(qf, "html.parser")

    # Get all query sections bounded by <DOC> tags
    doctags = query_soup.find_all("doc")

    # For all doctags
    for doctag in doctags:

        # Initialize query variables
        qid      = -1
        querystr = ""

        # get docno tag, where query ids are stored
        docnotag = doctag.find("docno")
        assert (docnotag is not None)

        # Get query id
        qid = int(docnotag.text)

        # decompose docnotag. we no longer need it. it will get in the way of
        # getting the query
        docnotag.decompose()

        # Get query string
        querystr = process_text(doctag.text.encode('ascii', 'ignore'))

        # create query
        querylst.append(Query(qid, querystr))

    return querylst

################################################################################
