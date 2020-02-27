#!/usr/bin/env python
"""
Script for loading large amount sof data in OxO formatted CSV files into a OxO Neo4j and creating a solr index
"""
__author__ = "kellmann"
__license__ = "Apache 2.0"
__date__ = "17/02/2020"

import os
from optparse import OptionParser

def start():
    parser = OptionParser()
    parser.add_option("-u", "--neoUser", help="specify a username for the neo4j database")
    parser.add_option("-p", "--neoPass", help="specify a password for the neo4j database")
    parser.add_option("-n", "--neoURL", help="specify the bolt url for the neo4j database")
    parser.add_option("-s", "--solrUrl")
    parser.add_option("-W", "--wipe", action="store_true", dest="wipe", help="wipe Neo4j and the solr database")
    parser.add_option("-d", "--datasources", help="load the datasource file")
    parser.add_option("-t", "--terms", help="load the term file")
    parser.add_option("-m", "--mappings", help="load the mapping file")
    parser.add_option("-c", "--config", help="config file")
    (options, args) = parser.parse_args()

#    os.system("python  OxoNeo4jLoader.py "+['', '-W'][options.wipe]+['', '-d'+ str(options.datasources)][options.datasources]+['', '-t'+ str(options.terms)][options.terms]+['', '-m'+ str(options.mapppings)][options.mapppings])
    #os.system("python  OxoNeo4jLoader.py -d /c/Users/alexa/PycharmProjects/OxODataLoader/oxo-mappings-2020-02-04/datasources.csv -t /c/Users/alexa/PycharmProjects/OxODataLoader/oxo-mappings-2020-02-04/umls_terms.csv -m /c/Users/alexa/PycharmProjects/OxODataLoader/oxo-mappings-2020-02-04/umls_mappings.csv")
    #os.system("python  SolrIndexer.py -u "neo4j" -p "dba" -W")
    return(0)

if __name__ == '__main__':
    start()