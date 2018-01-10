// This file defines the LuceneIndexer class that is just a wrapper around
// Lucene's API

import java.io.File;
import java.io.IOException;
import java.io.FileReader;
import java.io.FileNotFoundException;
import java.lang.NullPointerException;
import java.util.List;
import java.util.ArrayList;
import java.util.Arrays;

import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.IntField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

class LuceneIndexer {

    // LuceneIndexer globals
    private static SimpleAnalyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

    // Getting LuceneIndexer Analyzer in LuceneSearcher and other modules 
    public static SimpleAnalyzer indexAnalyzer() {
        return sAnalyzer;
    }

    /** LuceneIndexer constructor
     *
     * @param : idxPath Path to a directory where the index files will be
     *                  created. If the directory is not empty. the contents of
     *                  the directory will be deleted
     *
     * @param : docPath Path to a directory that contains the set of documents
     *                  to index. Only files with extension .txt will be indexed
     *
     * @throws : java.io.IOException when cannot find docPath
     *           java.io.IOException when there already is an idxPath
     */
    LuceneIndexer(String idxPath, String docPath) throws IOException {

        // Does the docPath exist ?
        if (!isDirectory(docPath)) {
            throw new IOException("Cannot find document folder " + docPath);
        }

        // Is there an index folder already ?
        if (isDirectory(idxPath)) {
            throw new IOException("Index already exists. Please delete " +
                                   idxPath + " before use");
        }

        // 1. Setup index writer
        IndexWriter idxWriter = luceneIndexWriter(idxPath);

        // 2. Add documents
        indexDirectory(docPath, idxWriter);

        // 3. Close writer
        idxWriter.close();
    }

    /** lucene IndexWriter creator
     *
     * @param : idxPath Path to the directory where the index files will be
     *                  created.
     *
     * @return : Returns a lucene index writer that writes index to idxPath
     *
     * @exception : Throws IOException if cannot create IndexWriter that
     *              writes to idxPath
     */
    private IndexWriter luceneIndexWriter(String idxPath) throws IOException {

        // Create lucene compatible FSDirectory from idxPath
        FSDirectory fsd = FSDirectory.open(new File(idxPath));

        // Configure index writer
        IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
                                                         sAnalyzer);
        // Initialize idxWriter
        return new IndexWriter(fsd, config);
    }

    /** Indexes files in the directory using the lucene's index writer
     *
     * @param : docPath Path to the directory containing documents to index
     *
     * @param : idxWriter Lucene's index writer as created by luceneIndexWriter
     *
     * @exception : Throws IOException / NullPointerException
     */
    private void indexDirectory(String docPath, IndexWriter idxWriter)
                                    throws IOException, NullPointerException {

        // Check inputs
        if (!isDirectory(docPath)) { throw new IOException();          }
        if (idxWriter == null)     { throw new NullPointerException(); }

        // List files in the directory
        File[] files = new File(docPath).listFiles();

        Arrays.sort(files);

        for (File f : files) {

            // Does the file pass the canIndex test ?
            if (!canIndex(f)) {
                System.out.println("Skipping file, " + f.getName());
                continue;
            }

            // Get document ID of the file
            int docID = cacmDocId(f.getName());

            // Get a document from the file
            Document d = new Document();

            // Get contents of file
            FileReader fr = new FileReader(f);

            // Add various relevant document fields
            d.add(new TextField("content", fr));
            d.add(new StringField("path", f.getPath(), Field.Store.YES));
            d.add(new StringField("name", f.getName(), Field.Store.YES));
            d.add(new IntField("DOCID", docID, Field.Store.YES));

            // Try to index
            try {
                idxWriter.addDocument(d);
            } catch (Exception e) {
                System.out.println("Could not add, " + f + " : " + e.getMessage());
            } finally {
                fr.close();
            }

        }

        System.out.println("Total files indexed ! " + idxWriter.numDocs());
    }

    /** Can the file be indexed ?
     *
     * @param : file The file in question
     */
    private boolean canIndex(File f) {

        if (!f.isFile()) { return false; }

        // Index only .txt files
        return f.getName().toLowerCase().endsWith(".txt") &&
               f.getName().toLowerCase().startsWith("cacm-");
    }

    /**
     * @param : cacm_file cacm filename of format CACM-XXXX.html.txt
     *
     * @return : The document ID from the cacm filename
     */
    private int cacmDocId(String cacm_filename) {

        /* Split filename by '-' */
        String[] hyphenSplit = cacm_filename.split("-", 2);

        /* assert that the first part is CACM */
        assert (hyphenSplit[0].compareTo("CACM") == 0);

        /* Split the second part of hyphenSplit by '.html' */
        String[] dotSplit = hyphenSplit[1].split(".html", 3);

        /* assert that the second part is .html.txt */
        assert (dotSplit[1].compareTo(".txt") == 0);

        /* the 0th part of dotSplit must be a number */
        return Integer.parseInt(dotSplit[0]);
    }

    /** Is the entity pointed to by the path a directory ?
     *
     * @param  : path Path to check
     *
     * @return : true iff the path points to a directory
     */
    private boolean isDirectory(String path) {

        return (new File(path).isDirectory());
    }

    /** Is the entity pointed to by the path a file ?
     *
     * @param : path Path to check
     *
     * @return : true iff the path points to a file
     */
    private boolean isFile(String path) {

        return (new File(path).isFile());
    }

}

