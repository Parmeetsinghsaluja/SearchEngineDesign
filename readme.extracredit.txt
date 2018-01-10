*                                                                              *
*  Information Retrieval Fall 2017                                             *
*                                                                              *
*  Proximity Enabled Search  - Ayush Shukla                                    *
*                              Parmeet Singh Saluja                            *
*                              Varun Sundar Rabindranath                       *
*                                                                              *
********************************************************************************

IMPORTANT: This is the readme for the extra credit assignment (Proximity
           enabled search). For the project readme, please refer to readme.txt.
           Please refer to ashukla1_psaluja2_vrabindranath3_extra_credit.pdf file
           for detailed implementation description, results and comparison.

README
------
    Proximity Enabled Search on CACM

External libraries
------------------

    * BeautifulSoup : This library is used to parse CACM documents

    * argparse : This library is used to parse input arguments. This only
                 facilitates passing inputs to the program and has nothing
                 to do with the implementation itself

How to setup
------------

  Python
  ------

    * Python version 2.7.12
    * Operating System : The assigment was done in Linux (Ubuntu)

    Having the external libraries specified should be enough to run the programs

Directory structure
-------------------

        INPUTS
        ------
        * cacm/cacm_docs - The given cacm.tar.gz is untar'd to cacm_docs folder.
                           This folder contains all CACM-XXXX.html files

        * cacm/cacm.query.txt - Given CACM queries file

        * cacm/cacm.rel.txt - Given CACM relevance judgement file

        * cacm/cacm_stem.query.txt - Given CACM stemmed queries

        * cacm/cacm_stem.txt - Given CACM stemmed file

        * cacm/common_words - Given stoplist file

        RESULTS
        -------

        Corpus Stores
        -------------
        * results/cacm.corpus - Cleaned (casefolded and punctuation handled) cacm
                                documents folder
        * results/cacm.corpus.stopped - Cleaned (casefolded and punctuation handled)
                                        and stopped cacm documents folder

        Index Stores
        ------------
        * results/cacm.index         - cacm.corpus index folder
        * results/cacm.index.stopped - cacm.corpus.stopped index folder

        Queries "queryid query" Format
        ------------------------------
        * results/queries.txt - Queries in cacm.query.txt represented in
                                "queryid query" format
        * results/queries.stopped.txt - Queries in cacm.query.txt, stopped and
                                        represented in "queryid query" format

        cacm.index + queries.txt results (Non-Stopped)
        ----------------------------------------------

        * results/cacm.result.proximity - Ranked documents reprensented as TREC Eval
                                          result string format for all queries in
                                          queries.txt, searched with index cacm.index
                                          with Proximity Enabled search


        cacm.index.stopped + queries.stopped.txt (Stopped)
        --------------------------------------------------

        * results/cacm.result.stopped.proximity - Ranked documents represented as TREC
                                                  Eval result string format for all queries
                                                  in queries.stopped.txt, searched with
                                                  cacm.index.stopped with Proximity
                                                  Enabled search

        Evaluation
        ----------

        * results/evaluation.proximity/precision_recall_QID.txt - Precision-Recall table for query QID. Where
                                                                  only the queries that appear in the relevance
                                                                  judgement have precision/recall values
                                                                  recorded.

        * results/evaluation.proximity/p@k.txt - Precision@K values for queries that appear in the relevance
                                                 judgement

        * results/evaluation.proximity/Global_measures.txt - MAP and MRR values for this result 

        * results/evaluation.stopped.proximity/* - Same meanings for files as mentioned for results/evaluation.proximity/*

        +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        IMPLEMENTAION
        -------------

        Retrieval Model
        ----------------

        * proximity_model.py - Defines ProximityModel class that implements proximity
                               enabled search

        Evaluation
        ----------

        * evaluation.py - Computes evaluation metrics like precision, recall,
                          P@K, MAP and MRR.

        Other
        -----

        * index.py - Defines an Index class that represents the inverted index

        * indexer.py  - This program, given the cleaned-corpus folder, indexes
                         the files in the corpus folder

        * searcher.py - Given the path to an index folder, a queryfile that contains
                        queries in space separated "queryid query\n" format, and
                        a retrieval model, ranks documents indexed by the inverted
                        index based on the retrieval model and the query

        * corpus.py - Given a path to a folder containing raw documents  and few
                      text processing options, creates a set of cleaned corpus files.

        * query_processing.py - Formats the queries in cacm.query.txt
                                to a space separated "queryid query\n" format

        * cacm_parser.py - Parses the CACM-XXXX.html files into document ID and
                           document contents

        * docid_mapper.py  - Provides utility class and functions that facilitates the
                             reading and writing of mapping between docid, corpus file
                             and the raw document file
        * global_statistics.py - Provides utility class and functions that facilitates the
                                 reading and writing of global statistics information

        * stopping.py - Defines a stopping class that provides utilities to stop
                        words from text given a stopfile

        * docrank_trec.py - Defines a DocRankTREC class that represents a TREC
                            Eval result string

        * query.py - Defines Query class

        * text_processing.py - Provides text processing utilities for punctuaion
                               handling and casefolding

        * result_set.py - Defines a Result and ResultSet class. The Result class
                          represents the result of an individual document for a
                          query and the ResultSet class represents the results
                          of all ranked documents for a query.

        * corpus_rw.py - Defines a CorpusRW class that facilitates the reading
                         and writing of cleaned up corpus files

        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        EXECUTION
        ---------

        proximity_run.sh - A shell script that when invoked from this package's root folder
                           will create all the result files in a folder "proximity-run-results"


How to run
----------


    EASIEST WAY (ONLY FOR LINUX)
    ----------------------------

        * STEP 1 : Unpack the package.
        * STEP 2 : do "sh proximity_run.sh"

        * The package has all the input files in the "cacm" folder as mentioned in
          the "Directory Structure" section of the readme. The shell script, executes
          various parts of the project in a pipelined fashion and stores all results
          in a folder called "proximity-run-results". This folder will contain all the
          "cacm.results.*" files and all "evaluation.*" folders as mentioned in the
          "RESULTS" sub-section of "Directory Strcuture" section

    MANUAL WAY (Works with Windows and Linux; But Linux preferred)
    --------------------------------------------------------------

    Note: Please execute all the programs from the same directory. Some programs
          depend on this fact to find the raw CACM documents (A mapping between
          docid, relative path to corpus file and a relative path to the raw document
          files is maintained in a file docid.map inside the indexfolder)

    EXECUTION PIPELINE
    ------------------

        Various parts of the project implementation depend on eachother.

        Stage 1 : Inputs
        ----------------
            * Create a folder called "cacm"
            * Untar the cacm.tar.gz into "cacm/cacm_docs". So that the cacm files are
              present as "cacm/cacm_docs/CACM-XXXX.html"
            * Move all other input files like "cacm.query.txt", "cacm.rel.txt",
              "cacm_stem.query.txt", "cacm_stem.txt" and "common_words" into the
              "cacm" folder

        Stage 1  Creating the copus files  :
        -----------------------------------

            * Create various versions of cacm documents (cacm documents with only
              basic text processing, stopped cacm documents) as corpus folders

            * python corpus.py --docstore=./cacm/cacm_docs --corpusstore=cacm.corpus
            * python corpus.py --docstore=./cacm/cacm_docs --corpusstore=cacm.corpus.stopped --stopfile=./cacm/common_words

        Stage 2 Creating queryfiles:
        ----------------------------

            * Create various versions of cacm query files (normal, stopped)

            * python query_processing.py --ipqueryfile=./cacm/cacm.query.txt --opqueryfile=./queries.txt 
            * python query_processing.py --ipqueryfile=./cacm/cacm.query.txt --opqueryfile=./queries.stopped.txt --stopfile=./cacm/common_words

        Stage 3 Creating indexstores:
        ----------------------------

            * Create one index folder for every corpus

            * python indexer.py --corpusstore=cacm.corpus --indexstore=cacm.index
            * python indexer.py --corpusstore=cacm.corpus.stopped --indexstore=cacm.index.stopped

        Stage 4 Search
        --------------

            Python searcher.py always output results in newline separated TREC Eval
            result strings, for all atmost 100 ranked documents for all queries in
            in the input query file

            Search cacm.index with queries.txt using ProximityModel -> cacm.result.proximity
            ---------------------------------------------------------------------------------
            python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=proximity --resultfile=cacm.result.proximity
            
            Search cacm.index.stopped with queries.stopped.txt using ProximityModel -> cacm.result.stopped.proximity
            ---------------------------------------------------------------------------------------------------------
            python searcher.py --indexstore=./cacm.index.stopped  --queryfile=./queries.stopped.txt --model=proximity --resultfile=cacm.result.stopped.proximity --desc=STOPPED


        STAGE 6 Evaluation:
        -------------------

            Python evaluation.py creates an output folder with the evaluation results.
            For example,
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.tfidf --modeltables=evaluation.tfidf
            Will create a folder evaluation.tfidf that will contain the following files,

                * evaluation.tfidf/precision_recall_QID.txt - Precision-Recall table for query QID. Where
                                                              only the queries that appear in the relevance
                                                              judgement have precision_recall values
                                                              recorded.
                * evaluation.tfidf/p@k.txt - Precision@K values for queries that appear in the relevance
                                              judgement
                * evaluation.tfidf/Global_measures.txt - MAP and MRR values for this result 

            Evaluate ProximityModel Normal : cacm.result.proximity -> evaluation.proximity
            ------------------------------------------------------------------------------
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.proximity --modeltables=evaluation.proximity
            
            Evaluate ProximityModel Stopped : cacm.result.stopped.proximity -> evaluation.stopped.proximity
            -----------------------------------------------------------------------------------------------
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.stopped.proximity --modeltables=evaluation.stopped.proximity

********************************************************************************
