## This program takes in the indexstore created by indexer.py and a cacm query
#  as argument and retrieves document IDs in the index that are determined to be
#  relevant to the query
from operator          import itemgetter

import argparse
import os
import shutil
from   argparse import RawTextHelpFormatter

## Globals #####################################################################
# Print to terminal about what the program is doing
# this is set by input to the program
verbose = False

# the relevance dictionary, holding key value pairs for each query and
# corresponding pages having relevance for that query
rel_dict = dict()

# the dictionary for top documents for each query as the key and the top DocumentScore
# as the values
top_doc_dict = dict()


## Help strings ################################################################

program_help = '''

    evaluation.py takes in as argument, the path to the relevance file
    of the cacm, the path to the file having 100 top documents of any model,
    the path where the files for meaures of recall and precision for each query
    and the global measure for every model are to be stored.

    Argument 1: relevancefile - Path to the folder, where the cacm relevance
                                file is present

    Argument 2: top100docsfile  - Path to file having the top documents

    Argument 3: modeltables     - Path where you want to store the tables for all queries

    EXAMPLES:

        python evaluation.py --relevancefile=./cacm.rel.txt --top100docsfile=cacm.result.bm25 --modeltables=E:\IR-PROJECT\Evaluation_Results\TF-IDF
  '''

relevancefile_help = '''

    Path to the folder, where the cacm relevance
                                file is present
    '''

top100docsfile_help = '''
    Path to file having the top documents
    '''

modeltables_help = '''
    Path where you want to store the tables for all queries
    '''


## Setup argument parser #######################################################

argparser = argparse.ArgumentParser(description = program_help,
                                    formatter_class = RawTextHelpFormatter)

argparser.add_argument("--relevancefile",
                       metavar  = "rl",
                       required = True,
                       type     = str,
                       help     = relevancefile_help)

argparser.add_argument("--top100docsfile",
                       metavar  = "t100",
                       required = True,
                       type     = str,
                       help     = top100docsfile_help)

argparser.add_argument("--modeltables",
                       metavar  = "m",
                       required = True,
                       type     = str,
                       help     = modeltables_help)

## Utilities ###################################################################

# GIVEN: relevancefile, which specifies the path oof the relevance file
# ------------------
# This function creates a dictionary, whic holds the query ID's as the key
# and the documents that are relevant as the values
def create_rel_dictionary(relevancefile):

    # creating the relevance dictionary
    with open(relevancefile, "r") as f:
        for line in f:
            q_info = line.split()
            k = q_info[0]
            v = q_info[2]
            if k in rel_dict:
                rel_dict[k].append(v[5:])
            else:
                rel_dict[k] = [v[5:]]


# GIVEN: top100docsfile, which specifies the path of the file having top
#        100 documents for a given model
# ----------------------
# This function creates a dictionary with key as the Query ID's and values
# as the top 100 documents for that query as per the given model
def create_top_docs_dictionary(top100docsfile):

    # creating the dictionary of top documents for tfidf model
    with open(top100docsfile,"r") as f:
        for line in f:
            qid_doc = line.split()
            k = qid_doc[0]
            v = qid_doc[2].strip("\n")
            if k in top_doc_dict:
                top_doc_dict[k].append(v)
            else:
                top_doc_dict[k] = [v]



# GIVEN: modeltables, which specifies the path where the query tables will be stored
# -------------------
# This function computes the precision and recall at every rank for each and every
# query, and it also calculates the Mean Average Precision, and Mean reciprocal
# rank for the given model.
def precision_and_recall_at_k(modeltables):

    sum_total_precision = 0.0      # for precision over all queries
    sum_total_reciprocal = 0.0     # for reciprocal ranks over all queries
    actual_num_queries = len(rel_dict)   # number of queries whose relevance data is present

    # open the file to write into the p@5 and p@20
    pk_file = open(os.path.join(modeltables, "p@k.txt"), "w+")

    # run for all queries in the top documents dictionary
    for k in top_doc_dict:


        total_precision = 0.0    # summation of precision of relevant pages
        r_rank = 0.0             # reciprocal rank of 1st relevant page
        A = 0.0         # Set of Relevant documents
        B = 0.0         # Set of Retrieved documents
        AB = 0.0        # Set of Retrieved documents that are Relevant
        precision = 0.0
        recall = 0.0
        index = 0       # keep track of rank
        rel_count = 0.0   # number of relevant documents for a query
        p_5 = 0.0       # Precision at 5
        p_20 = 0.0      # Precision at 20



        if k in rel_dict:

            # Opens the file for this query to enter the recall and precision value
            pr_file = open(os.path.join(modeltables, "precision_recall_" + k + ".txt"), "w+")

            # Open the file and write the headings for the measures
            pr_file.write("Rank" + " " + "Document_Id" + " " + "Precision" + " " + "Recall" + "\n\n")

            A = len(rel_dict[k])            # relevant number of documents in the corpus

            for n in top_doc_dict[k]:
                index = index + 1           # increase rank parameter by 1
                if n in rel_dict[k]:
                    rel_count = rel_count + 1    # increase relevance document count
                    if rel_count == 1:
                        r_rank = float(1/index)  # reciprocal rank
                    AB = AB + 1
                    B = B + 1
                    precision = float(AB/B)
                    total_precision = total_precision + precision
                    recall = float(AB/A)
                else:
                    B = B + 1
                    precision = float(AB/B)
                    recall = float(AB/A)
                if index == 5:                   # for precision, recall at 5
                    p_5 = precision
                if index == 20:                  # for precision, recall at 20
                    p_20 = precision


                # writing the values precision, recall values for every document in top 100 documents
                pr_file.write('%s\t %s\t %s\t %s\n' % (index, n, round(precision,3), round(recall,3)))


            # writing the precision at 5,20 in the p@k file for each query
            pk_file.write('for query %s \nP@5 =  %s\nP@20 = %s\n\n' % (k,p_5,p_20))


            # close recall file
            pr_file.close()

        else:
            continue


        # calculating the sum of total precisions and recalls over all the queries
        if (rel_count != 0):
            sum_total_precision = sum_total_precision + total_precision/rel_count
        sum_total_reciprocal = sum_total_reciprocal + r_rank

    # closes the p@k file
    pk_file.close()

    # function to calculate the MAP and MRR
    calculate_map_mrr(sum_total_precision, sum_total_reciprocal, actual_num_queries)


# GIVEN: sum_total_precision(summation of total precisions for all queries),
#        sum_total_reciprocal(summation of reciprocal ranks for all queries),
#        actual_num_queries(total number of queries whose relevance is known)
#  This functions write the MAP and MRR, after calculating these values, to
#  the mentioned files
def calculate_map_mrr(sum_total_precision, sum_total_reciprocal, actual_num_queries):

    MAP = sum_total_precision/actual_num_queries   # calculating MAP
    MRR = sum_total_reciprocal/actual_num_queries  # calculating MRR

    # writing the MAP and MRR, in a separate file named Global Measures alongside
    # the files for each query
    with open(os.path.join(modeltables, "Global_measures.txt"), "w+") as f:
        f.write('MAP %s\n\nMRR %s' % (MAP, MRR))


## Main ########################################################################

## Get arguments
args = vars(argparser.parse_args())

## Inputs
relevancefile = args['relevancefile']
top100docsfile = args['top100docsfile']
modeltables    = args['modeltables']

## Input check
if (not os.path.exists(relevancefile)):
    print "FATAL: Cannot find cacm relevance file, ", relevancefile
    exit (-1)
if (not os.path.exists(top100docsfile)):
    print "FATAL: Cannot find top documents file, ", top100docsfile
    exit (-1)
if (os.path.exists(modeltables)):
    print "WARNING: Deleting existing ", modeltables
    shutil.rmtree(modeltables)
# Create modeltables
os.makedirs(modeltables)

if (not os.path.exists(modeltables)):
    print "FATAL: Cannot find path to store files", modeltables
    exit(-1)

create_rel_dictionary(relevancefile)

create_top_docs_dictionary(top100docsfile)

precision_and_recall_at_k(modeltables)
