/** @file This file contains IRResult class that stores necessary
 *  retrieval results for a query
 */

import org.apache.lucene.search.ScoreDoc;

class IRResult {

    // result for query
    private IRQuery query;

    // Result string
    private String result;

    // IRResult constructor
    IRResult (IRQuery query_, String result_) {

	query = query_;
	result = result_;
    }

    // IRResult constructor
    IRResult (IRQuery query_, int rank, String desc, int docID, float score) {

	query  = query_;
	result = resultString(query.qidGet(), rank, desc, docID, score);
    }

    // Getters
    public String query()     { return query.queryGet(); }
    public int    qid()       { return query.qidGet();   }
    public String resultStr() { return result;           }

    // Helpers

    /** Formats result into a string */
    private String resultString(int qid, int rank, String desc, int docID, float score) {

        return qid + " Q0 " + docID + " " + rank + " " + score + " " + desc;
    }
}
