/** @file  This file contains the main function to index documents in a folder
 * using Lucene
 */

import java.io.File;
import java.util.List;

class IndexCorpus {

    private static String help =
    " This program indexes files in a folder using Lucene                 \n" +
    "									  \n" +
    " @param : corpusstore  Path to the documents folder that contains    \n" +
    "                       documents to index                            \n" +
    "                                                                     \n" +
    " @param : idxstore     Path to the folder where index files must be  \n" +
    "			    stored                                        \n" +
    "									  \n" +
    " Examples:								  \n" +
    "   To index files in a folder bfs_corpus and store the index in the  \n" +
    "   folder bfs_index,						  \n" +
    "									  \n" +
    "    java IndexCorpus -corpusstore=./bfs_corpus -idxstore=./bfs_index \n";

    /**
     * Main method that indexes documents
     *
     * @param : corpusstore  Path to the documents folder that contains documents
     *                       to index
     *
     * @param : idxstore     Path to the folder where index files must be stored
     *
     * Examples:
     *   To index files in a folder bfs_corpus and store the index in the folder
     *   bfs_index
     *
     *   java IndexCorpus -corpusstore=./bfs_corpus -idxstore=./bfs_index
     */
    public static void main(String args[]) {

	String corpusStore, idxStore;

	// Do we have 2 arguments ?
	if (args.length != 2) {
	    System.out.println("\n FATAL : InSufficient Arguments \n");
	    System.out.println(help);
	    return;
       	}

	// Get value corpusStore, idxStore, queryFile options
	corpusStore = getValue(args, "-corpusstore");
	idxStore    = getValue(args, "-idxstore");

	// Do we have all arguments ?
	if (corpusStore.equals("") ||
            idxStore.equals("")) {

	    System.out.println("\n FATAL : Incorrect arguments \n");
	    System.out.println(help);
	    return;
	}

        // corpusStore exists?
        if (!isDirectory(corpusStore)) {

            System.out.println("FATAL : Cannot find corpusStore " + corpusStore);
            return;
        }

        // If the idxStore already exists. delete it
        if (isFile(idxStore) || isDirectory(idxStore)) {

           System.out.println("Deleting existing indexstore " + idxStore);
            // Delete indexstore
            delete(new File(idxStore));
        }

	// Index
	try {

	    // Create index
	    LuceneIndexer lindexer = new LuceneIndexer(idxStore, corpusStore);

	} catch (Exception e) {

	    System.out.println("Cannot create index " + e.getMessage());
	}

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

    /** Is the entity pointed to by the path a directory ?
     *
     * @param  : path Path to check
     *
     * @return : true iff the path points to a directory
     */
    private static boolean isDirectory(String path) {

        return (new File(path).isDirectory());
    }

    /** Is the entity pointed to by the path a file ?
     *
     * @param : path Path to check
     *
     * @return : true iff the path points to a file
     */
    private static boolean isFile(String path) {

        return (new File(path).isFile());
    }

    /** Delete the directory / file passed as input
     *
     * @param : f File/Directory to delete
     */
    private static void delete(File f) {

        // Is the path pointed to a file ?
        if (f.isFile()) { f.delete(); return; }

        // This is a directory
        for (File lf : f.listFiles()) {
            delete(lf);
        }

        // delete the directory itself
        f.delete();

        return;
    }
}
