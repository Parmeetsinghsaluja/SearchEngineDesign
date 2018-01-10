/** @file
 * Static class that contains static function helpers for the Query class
 */

/* XML Parser */
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.w3c.dom.Element;
import org.xml.sax.InputSource;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;

import java.io.FileReader;
import java.io.File;
import java.io.BufferedReader;
import java.io.StringReader;

import java.util.List;
import java.util.ArrayList;

class Queries {

    // Static factory method to get querylist
    /** Parse the input file to generate a list of queries
     *
     * @param : qfile Path to file containing queries
     *
     * @return: Returns a list of queries
     *
     * TODO: At present, the function expects the file to contain newline
     *	     separated strings, where every string is made of 2 parts,
     *
     *	     queryid SPACE query
     *
     *	     Make this more generic
     */
    public static List<IRQuery> queries(String file) {

	/* Decl return queries */
	List<IRQuery> qs = new ArrayList<IRQuery>();

        try {

	    /* Open file reader */
	    FileReader fr = new FileReader(new File(file));

	    /* Use buffered reader to parse filereader */
	    BufferedReader br = new BufferedReader(fr);

	    String line = null;

	    // read lines
	    while ((line = br.readLine()) != null) {

	        // Split line based on " ". The first part is qid and second
	        // part is the query
	        String[] lineParts = line.split(" ", 2);

	        // Conv line -> query
	        qs.add(new IRQuery(Integer.parseInt(lineParts[0]), lineParts[1]));
	    }

	    // Close file reader
	    fr.close();

        } catch (Exception e) {
            System.out.println("Cannot read queries from query file " + e.getMessage());
        }

	return qs;
    }

    /** Parse the cacm input query file to generate a list of queries
     *
     * @param : qfile Path to cacm file containing queries
     *
     * @return: Returns a list of queries
     */
    public static List<IRQuery> cacmQueries(String queryFile) {

	/* Decl return queries */
	List<IRQuery> qs = new ArrayList<IRQuery>();

        try {

            // Open query file
            FileReader fr = new FileReader(queryFile);

            BufferedReader br = new BufferedReader(fr);

            // Fill contents with contents of the query file
            String contents = "";

            String line = null;

            while ((line = br.readLine()) != null) {

                contents += line + "\n";
            }

            // Close query file
            fr.close();

            // The CACM query file is not a proper XML file. It has multiple
            // <DOC> root tags. Fabricate a global root tag to parse it with
            // Javax xml modules
            contents = "<ROOT>" + contents + "</ROOT>";

            // Parse xml
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            // Prepare input soruce
            InputSource is = new InputSource(new StringReader(contents));
            // Parse
            Document doc = dBuilder.parse(is);

            // Get all DOC tags
            NodeList nlist = doc.getElementsByTagName("DOC");

            // Iterate over DOC tags
            for (int i = 0; i < nlist.getLength(); i++) {

                Node n = nlist.item(i);

                qs.add(docNodeToQuery(n));
            }

        } catch (Exception e) {

            e.printStackTrace();
        }

	return qs;
    }

    // Helpers
    private static IRQuery docNodeToQuery(Node docNode) {

        return new IRQuery(readDocQueryID(docNode), readDocQuery(docNode));
    }

    private static String readDocQuery(Node docNode) {

        // All docNode's will have 3 children
        NodeList children = docNode.getChildNodes();
        assert (children.getLength() == 3);

        // The first and the third node form the query
        return children.item(0).getNodeValue().trim() + " " + children.item(2).getNodeValue().trim();
    }

    private static int readDocQueryID(Node docNode) {

        // All docNode's will have 3 children
        NodeList children = docNode.getChildNodes();
        assert (children.getLength() == 3);

        return Integer.parseInt(readDocNumNode(children.item(1)));
    }

    private static String readDocNumNode (Node docNumNode) {

        // DOCNO node has only one child
        NodeList children = docNumNode.getChildNodes();

        // Only one node possible in cacm
        assert (children.getLength() == 1);

        return children.item(0).getNodeValue().trim();
    }
}
