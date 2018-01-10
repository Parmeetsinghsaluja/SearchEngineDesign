
# Results Store directory
RESULTSTORE=./proximity-run-results

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

#------------------------------------------------------------------------------#

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index with queries.txt using ProximityModel -> "$RESULTSTORE"/cacm.result.proximity"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index  --queryfile=./queries.txt --model=proximity --resultfile=$RESULTSTORE/cacm.result.proximity

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Search cacm.index.stopped with queries.stopped.txt using ProximityModel -> "$RESULTSTORE"/cacm.result.stopped.proximity"
echo "-------------------------------------------------------------------------"
python searcher.py --indexstore=./cacm.index.stopped  --queryfile=./queries.stopped.txt --model=proximity --resultfile=$RESULTSTORE/cacm.result.stopped.proximity --desc=STOPPED

#------------------------------------------------------------------------------#

echo "Evaluations"

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate ProximityModel Normal : "$RESULTSTORE"/cacm.result.proximity -> "$RESULTSTORE"/evaluation.proximity"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.proximity --modeltables=$RESULTSTORE/evaluation.proximity

echo "\n"
echo "-------------------------------------------------------------------------"
echo "Evaluate ProximityModel Stopped : "$RESULTSTORE"/cacm.result.stopped.proximity -> "$RESULTSTORE"/evaluation.stopped.proximity"
echo "-------------------------------------------------------------------------"
python evaluation.py --relevancefile=./cacm/cacm.rel.txt --top100docsfile=$RESULTSTORE/cacm.result.stopped.proximity --modeltables=$RESULTSTORE/evaluation.stopped.proximity

#------------------------------------------------------------------------------#
