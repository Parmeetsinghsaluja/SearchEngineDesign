
# Results Store directory
RESULTSTORE=./run-results

# Delete Existing result store and create new one
rm -rf $RESULTSTORE
mkdir -p $RESULTSTORE

# Create corpus and query files
echo "-------------------------------------------------------------------------"
echo "Creating Normal Corpus : ./cacm/cacm_docs -> ./cacm.corpus"
echo "-------------------------------------------------------------------------"
python corpus.py --docstore=./cacm/cacm_docs --corpusstore=cacm.corpus


echo "\n"
echo "-------------------------------------------------------------------------"
echo "Creating Stopped Corpus : ./cacm/cacm_docs -> ./cacm.corpus.stopped"
echo "-------------------------------------------------------------------------"
python corpus.py --docstore=./cacm/cacm_docs --corpusstore=cacm.corpus.stopped --stopfile=./cacm/common_words

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Creating Stemmed Corpus : ./cacm/cacm_docs -> ./cacm.corpus.stemmed"
echo "-------------------------------------------------------------------------"
python corpus_stem.py --cacmstemfile=./cacm/cacm_stem.txt --corpusstore=cacm.corpus.stemmed

#------------------------------------------------------------------------------#

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Represent queries in space separated \"qid query\" format : ./cacm/cacm.query.txt -> ./queries.txt :"
echo "-------------------------------------------------------------------------"
python query_processing.py --ipqueryfile=./cacm/cacm.query.txt --opqueryfile=./queries.txt 


echo "\n"
echo "-------------------------------------------------------------------------"
echo "Represent queries in space separated \"qid query\" format with stopping: ./cacm/cacm.query.txt -> ./queries.stopped.txt :"
echo "-------------------------------------------------------------------------"
python query_processing.py --ipqueryfile=./cacm/cacm.query.txt --opqueryfile=./queries.stopped.txt --stopfile=./cacm/common_words

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Represent stemmed queries in space separated \"qid query\" format: ./cacm/cacm_stem.query.txt -> ./queries.stemmed.txt :"
echo "-------------------------------------------------------------------------"
python format_stem_queries.py --ipqueryfile=./cacm/cacm_stem.query.txt --opqueryfile=./queries.stemmed.txt

#------------------------------------------------------------------------------#

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Index normal corpus: ./cacm.corpus -> ./cacm.index"
echo "-------------------------------------------------------------------------"
python indexer.py --corpusstore=cacm.corpus --indexstore=cacm.index

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Index stopped corpus: ./cacm.corpus.stopped -> ./cacm.index.stopped"
echo "-------------------------------------------------------------------------"
python indexer.py --corpusstore=cacm.corpus.stopped --indexstore=cacm.index.stopped

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Index stemmed corpus: ./cacm.corpus.stemmed -> ./cacm.index.stemmed"
echo "-------------------------------------------------------------------------"
python indexer.py --corpusstore=cacm.corpus.stemmed --indexstore=cacm.index.stemmed

#------------------------------------------------------------------------------#

# Lucene
echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search the ./cacm.corpus with ./queries.txt using Lucene"
echo "-------------------------------------------------------------------------"

# Move to Lucene folder
cd ./lucene

# Run the index with normal corpus
make run-index
# Search the lucene's index with normal queries
make run-search
cd ..

mv ./lucene/cacm.result.lucene $RESULTSTORE


echo "Lucene resultfile " $RESULTSTORE"/cacm.result.lucene"

#------------------------------------------------------------------------------#

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index with queries.txt using TFIDF -> "$RESULTSTORE"/cacm.result.tfidf"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=tfidf --resultfile=$RESULTSTORE/cacm.result.tfidf

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index with queries.txt using BM25 -> "$RESULTSTORE"/cacm.result.bm25"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=bm25 --resultfile=$RESULTSTORE/cacm.result.bm25

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index with queries.txt using QLM -> "$RESULTSTORE"/cacm.result.qlm"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=qlm --resultfile=$RESULTSTORE/cacm.result.qlm

#------------------------------------------------------------------------------#

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index with queries.txt employing PRF -> "$RESULTSTORE"/cacm.result.prf"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=prf --resultfile=$RESULTSTORE/cacm.result.prf

#------------------------------------------------------------------------------#

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index.stopped with queries.stopped.txt using TFIDF -> "$RESULTSTORE"/cacm.result.stopped.tfidf"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index.stopped  --queryfile=./queries.stopped.txt --model=tfidf --resultfile=$RESULTSTORE/cacm.result.stopped.tfidf --desc=STOPPED


echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index.stopped with queries.stopped.txt using BM25 -> "$RESULTSTORE"/cacm.result.stopped.bm25"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index.stopped  --queryfile=./queries.stopped.txt --model=bm25 --resultfile=$RESULTSTORE/cacm.result.stopped.bm25 --desc=STOPPED


echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index.stopped with queries.stopped.txt using QLM -> "$RESULTSTORE"/cacm.result.stopped.qlm"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index.stopped  --queryfile=./queries.stopped.txt --model=qlm --resultfile=$RESULTSTORE/cacm.result.stopped.qlm --desc=STOPPED

#------------------------------------------------------------------------------#


echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index.stemmed with queries.stemmed.txt using TFIDF -> "$RESULTSTORE"/cacm.result.stemmed.tfidf"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index.stemmed  --queryfile=./queries.stemmed.txt --model=tfidf --resultfile=$RESULTSTORE/cacm.result.stemmed.tfidf --desc=STEMMED


echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index.stemmed with queries.stemmed.txt using BM25 -> "$RESULTSTORE"/cacm.result.stemmed.bm25"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index.stemmed  --queryfile=./queries.stemmed.txt --model=bm25 --resultfile=$RESULTSTORE/cacm.result.stemmed.bm25 --desc=STEMMED

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index.stemmed with queries.stemmed.txt using QLM -> "$RESULTSTORE"/cacm.result.stemmed.qlm"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index.stemmed  --queryfile=./queries.stemmed.txt --model=qlm --resultfile=$RESULTSTORE/cacm.result.stemmed.qlm --desc=STEMMED

#------------------------------------------------------------------------------#

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Generate snippets for normal BM25 run : "$RESULTSTORE"/cacm.result.bm25 -> "$RESULTSTORE"/snippets.bm25"
echo "-------------------------------------------------------------------------"
python gen_snippet.py --resultfile=$RESULTSTORE/cacm.result.bm25 --queryfile=queries.txt --indexstore=cacm.index --stopfile=cacm/common_words --snippetfile=$RESULTSTORE/snippets.bm25 --verbose

#------------------------------------------------------------------------------#

echo "Evaluations"

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate TFIDF Normal : "$RESULTSTORE"/cacm.result.tfidf -> "$RESULTSTORE"/evaluation.tfidf"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.tfidf --modeltables=$RESULTSTORE/evaluation.tfidf

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate BM25 Normal : "$RESULTSTORE"/cacm.result.bm25 -> "$RESULTSTORE"/evaluation.bm25"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.bm25 --modeltables=$RESULTSTORE/evaluation.bm25

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate QLM Normal : "$RESULTSTORE"/cacm.result.qlm -> "$RESULTSTORE"/evaluation.qlm"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.qlm --modeltables=$RESULTSTORE/evaluation.qlm

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate Lucene Normal : "$RESULTSTORE"/cacm.result.lucene -> "$RESULTSTORE"/evaluation.lucene"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.lucene --modeltables=$RESULTSTORE/evaluation.lucene

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate PRF : "$RESULTSTORE"/cacm.result.prf -> "$RESULTSTORE"/evaluation.prf"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.prf --modeltables=$RESULTSTORE/evaluation.prf

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate TFIDF Stopped : "$RESULTSTORE"/cacm.result.stopped.tfidf -> "$RESULTSTORE"/evaluation.stopped.tfidf"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.stopped.tfidf --modeltables=$RESULTSTORE/evaluation.stopped.tfidf

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate BM25 Stopped : "$RESULTSTORE"/cacm.result.stopped.bm25 -> "$RESULTSTORE"/evaluation.stopped.bm25"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.stopped.bm25 --modeltables=$RESULTSTORE/evaluation.stopped.bm25

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate QLM Stopped : "$RESULTSTORE"/cacm.result.stopped.qlm -> "$RESULTSTORE"/evaluation.stopped.qlm"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.stopped.qlm --modeltables=$RESULTSTORE/evaluation.stopped.qlm

#echo "Proximity search without stopping"
#python searcher.py --indexstore=./cacm.index --queryfile=./queries.txt --model=Proximity --resultfile=./cacm.result.proximity

#echo "Proximity search with stopping"
#python searcher.py --indexstore=./cacm.index.stopped --queryfile=./queries.stopped.txt --model=proximity --resultfile=./cacm.result.stopped.proximity

