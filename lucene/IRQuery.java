/** @file This file defines the query class */

class IRQuery {

    // Query ID
    private int qid;

    // Query String
    private String query;

    IRQuery(int qid_, String query_) {

	this.qid   = qid_;
	this.query = query_;
    }

    // Getters
    public int qidGet()      { return qid;   }
    public String queryGet() { return query; }
}
