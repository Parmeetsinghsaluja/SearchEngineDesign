*                                                                              *
*  Information Retrieval Fall 2017                                             *
*                                                                              *
*  Project - Ayush Shukla                                                      *
*            Parmeet Singh Saluja                                              *
*            Varun Sundar Rabindranath                                         *
*                                                                              *
********************************************************************************

IMPORTANT: This is the readme for the project. For extra credit readme, please
           refer to readme.extracredit.txt

README
------

 This project is split into various phases and tasks.

 The Lucene part of this project is implemented in Java
 All other parts of the project are completely implemented in Python

External libraries
------------------

    * BeautifulSoup : This library is used to parse CACM documents

    * argparse : This library is used to parse input arguments. This only
                 facilitates passing inputs to the program and has nothing
                 to do with the implementation itself

How to setup
------------

  Java
  ----

    * Java version     : Java 8 (output of "javac -version" : "javac 1.8.0_151")
    * Lucene version   : 4.7.2
    * Operating System : The project was developed in Linux and Windows simultaneously
                         Though the project can be executed in either operating
                         systems, Linux is preferred and also a shell script to
                         run all parts of the implementation is provided.

    Lucene 4.7.2's jar files are provided in this package itself (refer to
    the directory structure section of this readme). Therefore, the user of this
    package does not have to download any package to run Lucene program

  Python
  ------

    * Python version 2.7.12
    * Operating System : The assigment was done in Linux (Ubuntu)
                         Though the project can be executed in either operating
                         systems, Linux is preferred and also a shell script to
                         run all parts of the implementation is provided.

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
        * results/cacm.corpus.stemmed - Each stemmed cacm file text in cacm_stem.txt
                                        is split and represented as multiple corpus
                                        files

        Index Stores
        ------------
        * results/cacm.index         - cacm.corpus index folder
        * results/cacm.index.stopped - cacm.corpus.stopped index folder
        * results/cacm.index.stemmed - cacm.corpus.stemmed index folder

        Queries "queryid query" Format
        ------------------------------
        * results/queries.txt - Queries in cacm.query.txt represented in
                                "queryid query" format
        * results/queries.stopped.txt - Queries in cacm.query.txt, stopped and
                                        represented in "queryid query" format
        * results/queries.stemmed.txt - Queries in cacm_stem.query.txt
                                       reprensented in "queryid query" format

        cacm.index + queries.txt results (PHASE 1 - TASK 1)
        ---------------------------------------------------

        * results/cacm.result.qlm - Ranked documents reprensented as TREC Eval
                                    result string format for all queries in
                                    queries.txt, searched with index cacm.index
                                    with QLM retrieval model


        * results/cacm.result.tfidf - Ranked documents represented as TREC Eval
                                      result string format for all queries in
                                      queries.txt, searched with index cacm.index
                                      with TFIDF retrieval model

        * results/cacm.result.bm25 - Ranked documents represented as TREC Eval
                                     result string format for all queries in
                                     queries.txt, searched with index cacm.index
                                     with BM25 retrieval model

        * results/cacm.result.lucene - Ranked documents represented as TREC Eval
                                       result string format for all queries in
                                       queries.txt, searched from cacm.corpus with
                                       lucene's default retrieval model

        cacm.index + queries.txt + PRF (PHASE 1 - TASK 2)
        -------------------------------------------------

        * results/cacm.result.prf - Ranked documents represented as TREC Eval
                                    result string format for all queries in
                                    queries.txt, using Pseudo-Relevance Feedback

        cacm.index.stopped + queries.stopped.txt (PHASE 1 - TASK 3 Stopping)
        --------------------------------------------------------------------

        * results/cacm.result.stopped.bm25 - Ranked documents represented as TREC
                                             Eval result string format for all queries
                                             in queries.stopped.txt, searched with
                                             cacm.index.stopped with BM25 retrieval model

        * results/cacm.result.stopped.qlm - Ranked documents represented as TREC
                                            Eval result string format for all queries
                                            in queries.stopped.txt, searched with
                                            cacm.index.stopped with QLM retrieval model

        * results/cacm.result.stopped.tfidf - Ranked documents represented as TREC
                                              Eval result string format for all queries
                                              in queries.stopped.txt, searched with
                                              cacm.index.stopped with TFIDF retrieval model

        cacm.index.stemmed + queries.stemmed.txt (PHASE 1 - TASK 3 Stemming)
        --------------------------------------------------------------------

        * results/cacm.result.stemmed.bm25 - Ranked documents  represented as TREC
                                             Eval result string format for queries
                                             in queries.stemmed.txt, searched with
                                             cacm.index.stemmed with BM25 retrieval
                                             model

        * results/cacm.result.stemmed.qlm - Ranked documents  represented as TREC Eval
                                            result string format for queries in
                                            queries.stemmed.txt, searched with
                                            cacm.index.stemmed with QLM retrieval model

        * results/cacm.result.stemmed.tfidf  - ranked documents  represented as TREC
                                               Eval result string format for queries
                                               in queries.stemmed.txt, searched with
                                               cacm.index.stemmed with TFIDF retrieval model

        Snippet Generation (Phase 2)
        ----------------------------

        * results/snippets.bm25 - Ranked CACM document snippets for all results in
                                  cacm.result.bm25

        Evaluation (Phase 3)
        --------------------

        * results/evaluation.bm25/precision_recall_QID.txt - Precision-Recall table for query QID. Where
                                                             only the queries that appear in the relevance
                                                             judgement have precision_recall values
                                                             plotted.
        * results/evaluation.bm25/p@k.txt - Precision@K values for queries that appear in the relevance
                                            judgement

        * results/evaluation.bm25/Global_measures.txt - MAP and MRR values for this result 


        * results/evaluation.tfidf/* - Same meanings for files as mentioned for results/evaluation.bm25/*

        * results/evaluation.qlm/* - Same meanings for files as mentioned for results/evaluation.bm25/*

        * results/evaluation.lucene/* - Same meanings for files as mentioned for results/evaluation.bm25/*

        * results/evaluation.prf/* - Same meanings for files as mentioned for results/evaluation.bm25/*

        * results/evaluation.stoped.bm25/* - Same meanings for files as mentioned for results/evaluation.bm25/*

        * results/evaluation.stopped.qlm/* - Same meanings for files as mentioned for results/evaluation.bm25/*

        * results/evaluation.stopped.tfidf/* - Same meanings for files as mentioned for results/evaluation.bm25/*

        * resulttables/resulttables.* - Same as results/evaluation.*. These folders are duplicated for the sake of
                                           convenience of the graders

        +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        IMPLEMENTAION
        -------------

        Retrieval Models
        ----------------

        * tfidf.py  - Defines a TFIDF class that implements the tf.idf retrieval model

        * bm25.py - Defines a BM25 class that implements the BM25 retrieval model

        * qlm.py - Defines a QLM class that implements the Query Likelihood retrieval model


        Pseudo Relevance Feedback
        -------------------------

        * bm25_relvence.py - Defines a BM25_R class, that implements a Pseudo Relevance Feedback
                             technique

        Snippet Generation
        ------------------

        * gen_snippet.py - Given a result file with '\n' separated result strings
                           of TREC Eval format and other information, generates
                           a snippet for every ranked document for every query

        * snippet.py - Defines a Snippet class, that implements the snippet
                       generation algorithm

        * snippet_lm.py - Defines a SnippetLM class that provides implements
                          computations regarding relevance language model
                          technique used in snippet generation

        Evaluation
        ----------

        * evaluation.py - Computes evaluation metrics like precision, recall,
                          P@K, MAP and MRR.

        Lucene
        ------

        * ./lucene/IndexCorpus.java   : Main Java program that indexes documents
                                        in a corpus folder and creates an index
                                        using lucene

        * ./lucene/Search.java        : Main Java program that searches the index
                                        created by IndexCorpus.java with queries

        * ./lucene/IRQuery.java       : Contains a class definition to represent
                                        user queries

        * ./lucene/IRResult.java      : Contains class definitions to represent
                                        query results

        * ./lucene/LuceneIndexer.java : Wrapper class around Lucene's indexer

        * ./lucene/LuceneSearcher.java : Wrapper class around Lucene's searcher

        * ./lucene/Queries.java        : Help methods to create IRQuery list from
                                         a file containing multiple/single
                                         queryID-query pairs

        * ./lucene/lucenejars/*jar     : All the Lucene jars and the Lucene's
                                         dependent jars. These are all the jar
                                         dependencies required to run Task 1

        * ./lucene/Makefile            : Makefile to build and index and search
                                         using Lucene

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

        * corpus_stem.py - Consumes the cacm_stem.txt, and produces a stemmed
                           corpus folder. This program does not process the text
                           in any way. It only represents it in a format that our
                           indexer can work with

        * query_processing.py - Formats the queries in cacm.query.txt
                                to a space separated "queryid query\n" format

        * format_stem_queries.py - Transforms the queries in file cacm_stem.query.txt
                                   into a ubiquitous space separated "queryid query\n"
                                   format

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

        run.sh - A shell script that when invoked from this package's root folder
                 will create all the result files in a folder "run-results"

How to run
----------


    EASIEST WAY (ONLY FOR LINUX)
    ----------------------------

        * STEP 1 : Unpack the package.
        * STEP 2 : do "sh run.sh"

        * The package has all the input files in the "cacm" folder as mentioned in
          the "Directory Structure" section of the readme. The shell script, executes
          various parts of the project in a pipelined fashion and stores all results
          in a folder called "run-results". This folder will contain all the "cacm.results.*"
          files and all "evaluation.*" folders along with a "snippets.bm25" file
          as mentioned in the "RESULTS" sub-section of "Directory Strcuture" section


    MANUAL EXECUTION (Will work for both Linux and Windows. Linux is preferred however)
    -----------------------------------------------------------------------------------

    Note: Please execute all the programs from the same directory. Some programs
          like snippet generation depends on this fact to find the raw
          CACM documents (A mapping between docid, relative path to corpus file
          and a relative path to the raw document files is maintained in a file
          docid.map inside the indexfolder)

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
              basic text processing, stopped cacm documents, stemmed cacm documents)
              as corpus folders

            * python corpus.py --docstore=./cacm/cacm_docs --corpusstore=cacm.corpus
            * python corpus.py --docstore=./cacm/cacm_docs --corpusstore=cacm.corpus.stopped --stopfile=./cacm/common_words
            * python corpus_stem.py --cacmstemfile=./cacm/cacm_stem.txt --corpusstore=cacm.corpus.stemmed

        Stage 2 Creating queryfiles:
        ----------------------------

            * Create various versions of cacm query files (normal, stopped, stemmed)


            * python query_processing.py --ipqueryfile=./cacm/cacm.query.txt --opqueryfile=./queries.txt 
            * python query_processing.py --ipqueryfile=./cacm/cacm.query.txt --opqueryfile=./queries.stopped.txt --stopfile=./cacm/common_words
            * python format_stem_queries.py --ipqueryfile=./cacm/cacm_stem.query.txt --opqueryfile=./queries.stemmed.txt

        Stage 3 Creating indexstores:
        ----------------------------

            * Create one index folder for every corpus

            * python indexer.py --corpusstore=cacm.corpus --indexstore=cacm.index
            * python indexer.py --corpusstore=cacm.corpus.stopped --indexstore=cacm.index.stopped
            * python indexer.py --corpusstore=cacm.corpus.stemmed --indexstore=cacm.index.stemmed

        Stage 4 Search
        --------------

            Python searcher.py always output results in newline separated TREC Eval
            result strings, for all atmost 100 ranked documents for all queries in
            in the input query file

            CACM - Corpus/Index with only basic text processing
            ---------------------------------------------------
                * To search the index that has indexed the corpus with only basic
                  textprocessing

                * Using TFIDF
                * python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=tfidf --resultfile=cacm.result.tfidf

                * Using BM25
                * python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=bm25 --resultfile=cacm.result.bm25

                * Using QLM
                * python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=qlm --resultfile=cacm.result.qlm

                * Using Lucene
                * cd lucene
                # To index all files in the corpus "./../cacm.corpus" and store the index in "cacm.lucene.index"
                * make run-index
	        # To search the index "cacm.lucene.index" with queries in "./../queries.txt" and store results in cacm.result.lucene                   * make run-search
                * cd ..

                # Using Pseudo-Relevance Feedback
                * python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=prf --resultfile=cacm.result.prf

            CACM - Corpus/Index with basic text processing and stopping
            -----------------------------------------------------------
                * To search the index that has indexed the corpus with basic
                  textprocessing and stopping

                * Using TFIDF
                * python searcher.py --indexstore=./cacm.index.stopped  --queryfile=./queries.stopped.txt --model=tfidf --resultfile=cacm.result.stopped.tfidf --desc=STOPPED

                * Using BM25
                * python searcher.py --indexstore=./cacm.index.stopped  --queryfile=./queries.stopped.txt --model=bm25 --resultfile=cacm.result.stopped.bm25 --desc=STOPPED

                * Using QLM
                * python searcher.py --indexstore=./cacm.index.stopped  --queryfile=./queries.stopped.txt --model=qlm --resultfile=cacm.result.stopped.qlm --desc=STOPPED

            CACM - Corpus/Index with basic text processing and stemming
            -----------------------------------------------------------

                * To search the index that has indexed the corpus with basic
                  textprocessing and stemming

                * Using TFIDF
                * python searcher.py --indexstore=./cacm.index.stemmed  --queryfile=./queries.stemmed.txt --model=tfidf --resultfile=cacm.result.stemmed.tfidf --desc=STEMMED
                
                * Using BM25
                * python searcher.py --indexstore=./cacm.index.stemmed  --queryfile=./queries.stemmed.txt --model=bm25 --resultfile=cacm.result.stemmed.bm25 --desc=STEMMED
                
                * Using QLM
                * python searcher.py --indexstore=./cacm.index.stemmed  --queryfile=./queries.stemmed.txt --model=qlm --resultfile=cacm.result.stemmed.qlm --desc=STEMMED

        STAGE 5 Snippet Generation:
        --------------------------

            * Generate snippets for normal BM25 run : cacm.result.bm25 -> snippets.bm25
            * python gen_snippet.py --resultfile=cacm.result.bm25 --queryfile=queries.txt --indexstore=cacm.index --stopfile=cacm/common_words --snippetfile=snippets.bm25 --verbose

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

            * Evaluate TFIDF Normal : cacm.result.tfidf -> evaluation.tfidf
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.tfidf --modeltables=evaluation.tfidf
            * Evaluate BM25 Normal : cacm.result.bm25 -> evaluation.bm25
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.bm25 --modeltables=evaluation.bm25
        
            * Evaluate QLM Normal : cacm.result.qlm -> evaluation.qlm"
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.qlm --modeltables=evaluation.qlm
        
            * Evaluate Lucene Normal : cacm.result.lucene -> evaluation.lucene
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.lucene --modeltables=evaluation.lucene
        
            * Evaluate PRF : cacm.result.prf -> evaluation.prf
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.prf --modeltables=evaluation.prf

            * Evaluate TFIDF Stopped : cacm.result.stopped.tfidf -> evaluation.stopped.tfidf
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.stopped.tfidf --modeltables=evaluation.stopped.tfidf
        
            * Evaluate BM25 Stopped : cacm.result.stopped.bm25 -> evaluation.stopped.bm25
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.stopped.bm25 --modeltables=evaluation.stopped.bm25
        
            * Evaluate QLM Stopped : cacm.result.stopped.qlm -> evaluation.stopped.qlm
            * python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=cacm.result.stopped.qlm --modeltables=evaluation.stopped.qlm

********************************************************************************
