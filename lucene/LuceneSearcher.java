/** @file This file implements a class LuceneSearcher that searches the lucene
 * created index with queries
 */

import java.io.File;

import java.util.List;
import java.util.ArrayList;

import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.document.Document;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.util.Version;

class LuceneSearcher {

    /* Reader */
    private IndexReader reader;
    /* Searcher */
    private IndexSearcher searcher;

    /** LuceneSearcher constructor
     *  The LuceneSearcher takes in as arguments the index store (folder where
     *  LuceneIndexer created the index files) and a list of query strings
     *
     * @param : idxStore Path to the folder where LuceneIndexer created the index
     */
     LuceneSearcher(String idxStore) {

         // Try to read indexstore
         try {

	    /* Initialize index reader */
	    reader = DirectoryReader.open(FSDirectory.open(new File(idxStore)));

	    /* Initialize searcher */
	    searcher = new IndexSearcher(reader);

         } catch (Exception e) {

             reader   = null;
             searcher = null;

             System.out.println("FATAL : LuceneSearcher cannot read index " + e.getMessage());
         }
     }

    /** Searches the index with list of queries in the input
     *
     * @param : queries  List of Query to search the index with
     *
     * @param : maxMatch Maximum number of results for a query
     *
     * @return: a list of list of strings.
     *	        Where each list of string is the list of utmost 100 ranked
     *		document names of the following format,
     *	        queryid Q0 doc_id rank score lucene
     */
     List<List<IRResult> > search(List<IRQuery> queries, int maxMatch) {

	/* Scored document list */
	List<List<IRResult> > queriesScored = new ArrayList<List<IRResult> >();

	for (int qidx = 0; qidx < queries.size(); qidx++) {

	    // Get query of concern
	    IRQuery irq = queries.get(qidx);

	    TopScoreDocCollector collector = TopScoreDocCollector.create(maxMatch,
              		   				                 true);
	    // Query parser setup
	    Query q;

            try {
                q = new QueryParser(Version.LUCENE_47,
		             	    "content",
				    LuceneIndexer.indexAnalyzer()).parse(irq.queryGet());
            } catch (Exception e) {
                System.out.println("Cannot parse query, " + e.getMessage());
                return queriesScored;
            }

	    // Search query
            try {
	        searcher.search(q, collector);

            } catch (Exception e) {
                System.out.println("Cannot search index for query, " +
                                   irq.queryGet() + " " + e.getMessage());
            }

	    // Score
	    ScoreDoc[] hits = collector.topDocs().scoreDocs;

	    // Get list of query results
	    List<IRResult> queryScored = new ArrayList<IRResult>();
	    for (int hitidx = 0; hitidx < hits.length; hitidx++) {

                /* Get this ScoreDoc */
                ScoreDoc sd = hits[hitidx];

                /* Get this document */
                Document d = null;

                try {
                    d = searcher.doc(sd.doc);
                } catch (Exception e) {
                    System.out.println("Exception : " + e.getMessage());
                }

                /* Get stored document ID */
                int docID   = Integer.parseInt(d.get("DOCID"));

                /* get document score */
                float score = hits[hitidx].score;

		queryScored.add(new IRResult(irq, hitidx + 1, "lucene", docID, score));
	    }

	    queriesScored.add(queryScored);
	}

	return queriesScored;
     }
}
