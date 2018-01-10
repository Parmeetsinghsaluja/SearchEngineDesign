/** @file  This file contains the main function that searches the index created
 *         by IndexCorpus.java with cacm queries using Lucene
 */

import java.io.File;
import java.io.FileWriter;
import java.io.BufferedWriter;
import java.io.IOException;
import java.util.List;

class Search {

    private static String help =
    " This program searches the index created by IndexCorpus.java with    \n" +
    " cacm queries            						  \n" +
    "									  \n" +
    " @param : idxstore     Path to the folder where index files are      \n" +
    "			    stored                                        \n" +
    "                                                                     \n" +
    " @param : queryfile    Path to the cacm queries file                 \n" +
    "                                                                     \n" +
    " @param : resultfile   Path to the result file                       \n" +
    "                                                                     \n" +
    " @param : desc         Description of the run. This corresponds to   \n" +
    "                       the last space separated word in TREC Eval    \n" +
    "                       result string                                 \n" +
    "									  \n" +
    " Examples:								  \n" +
    "    To search the index stored in cacm.lucene.index with queries     \n" +
    "    in file ./../queries.txt and store it in ./cacm.result.lucene    \n" +
    "									  \n" +
    "    java Search -idxstore=./cacm.lucene.index -queryfile=./../queries.txt -resultfile=./cacm.result.lucene -desc=STOPPED \n";

    /**
     * Main method that indexes documents
     *
     * @param : idxstore     Path to the folder where index files are stored
     *
     * @param : queryfile    Path to the cacm queries file
     *
     * @param : resultfile   Path to store the results in TREC Eval format
     *
     * @param : desc         Description of the run. This corresponds to
     *                       the last space separated word in TREC Eval
     *                       result string
     * Examples:
     *
     *  To search the index stored in cacm.lucene.index with queries
     *  in file ./../queries.txt and store it in ./cacm.result.lucene
     *
     *  java Search -idxstore=./cacm.lucene.index -queryfile=./../queries.txt -resultfile=./cacm.result.lucene -desc=STOPPED
     */
    public static void main(String args[]) {

	String idxStore, queryFile, resultFile, desc;

	// Do we have 4 arguments ?
	if (args.length != 4) {
	    System.out.println("\n FATAL : InSufficient Arguments \n");
	    System.out.println(help);
	    return;
       	}

	// Get value idxStore, queryFile options
	idxStore    = getValue(args, "-idxstore");
        queryFile   = getValue(args, "-queryfile");
        resultFile  = getValue(args, "-resultfile");
        desc        = getValue(args, "-desc");

	// Do we have all arguments ?
	if (idxStore.equals("")    ||
            queryFile.equals("")   ||
            resultFile.equals("")) {

	    System.out.println("\n FATAL : Incorrect arguments \n");
	    System.out.println(help);
	    return;
	}

	// Queries to search
	List<IRQuery> queries = Queries.queries(queryFile);

        // Searcher
        LuceneSearcher searcher = new LuceneSearcher(idxStore);

        // Search the index with queries
        List<List<IRResult> > results = searcher.search(queries, 100);

        // Sanity check
        assert (results.size() == queries.size())
            : "More result than there is queries";
        // Sanity check that we have utmost 100 results per query
        for (int resultidx = 0; resultidx < results.size(); resultidx++) {
            assert (results.get(resultidx).size() <= 100) : "Results more than 100";
        }

        // Print results
        // printResults(results);
        storeResults(results, resultFile, desc);

	return;
    }

    private static String getValue(String args[], String option) {

	// Iterate through args
	for (int argidx = 0; argidx < args.length; argidx++) {

	    String arg = args[argidx];

	    // Does the cla start with desired option
	    if (arg.startsWith(option)) { return arg.split("=", 2)[1]; }
	}

	// Did not find a matching option
	return "";
    }

    // Helpers
    private static void printResults(List<List<IRResult> > results) {

        // For result set of each query
        for (int qresult = 0; qresult < results.size(); qresult++) {

            List<IRResult> resultSet = results.get(qresult);

            System.out.println("-----------------------------------------------");

            if (resultSet.size() > 0) {
                System.out.println("Query : " + resultSet.get(0).query());
            }

            // For each result in result set
            for (int ridx = 0; ridx < resultSet.size(); ridx++) {

                System.out.println(resultSet.get(ridx).resultStr());
            }

            System.out.println("-----------------------------------------------");
        }
    }

    // Store results
    private static void storeResults(List<List<IRResult> > results, String resultFile, String desc) {

        try {

            // Create resultFile
	    FileWriter fw = new FileWriter(resultFile, false);

            // Create buffered writer
	    BufferedWriter bw = new BufferedWriter(fw);

            // For result set of each query
            for (int qresult = 0; qresult < results.size(); qresult++) {

                List<IRResult> resultSet = results.get(qresult);

                // For each result in result set
                for (int ridx = 0; ridx < resultSet.size(); ridx++) {
                    // Write TREC format strings to file
                    bw.write(resultSet.get(ridx).resultStr() + "_" + desc);
                    bw.newLine();
                }

            }

            // close buffered writer and file writer
	    bw.close();
	    fw.close();

	} catch (Exception e) {

	    System.out.println("Cannot write to file " + e.getMessage());
	}

    }
}
