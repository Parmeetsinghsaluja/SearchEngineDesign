
CPFLAG=-cp ".:./lucenejars/*"

all: lindexer lsearcher irquery irresult queries indexcorpus search

lindexer: LuceneIndexer.java
	javac $(CPFLAG) LuceneIndexer.java

lsearcher: LuceneSearcher.java
	javac $(CPFLAG) LuceneSearcher.java

irquery: IRQuery.java
	javac $(CPFLAG) IRQuery.java

irresult: IRResult.java
	javac $(CPFLAG) IRResult.java

queries: Queries.java
	javac $(CPFLAG) Queries.java

indexcorpus: IndexCorpus.java
	javac $(CPFLAG) IndexCorpus.java

search: Search.java
	javac $(CPFLAG) Search.java

run-index: all
	java $(CPFLAG) -enableassertions IndexCorpus -corpusstore=./../cacm.corpus -idxstore=./cacm.lucene.index

run-search: all
	java $(CPFLAG) -enableassertions Search -idxstore=./cacm.lucene.index -queryfile=./../queries.txt -resultfile=./cacm.result.lucene -desc=NOTSTOPPED

run-index-stopped: all
	java $(CPFLAG) -enableassertions IndexCorpus -corpusstore=./../cacm.corpus.stopped -idxstore=./cacm.lucene.index.stopped

run-search-stopped: all
	java $(CPFLAG) -enableassertions Search -idxstore=./cacm.lucene.index.stopped -queryfile=./../queries.stopped.txt -resultfile=./cacm.result.lucene.stopped -desc=STOPPED

run: run-search
