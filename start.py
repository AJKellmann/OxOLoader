#!/usr/bin/env python
"""
Script for loading large amount sof data in OxO formatted CSV files into a OxO Neo4j and creating a solr index
"""
__author__ = "kellmann"
__license__ = "Apache 2.0"
__date__ = "28/02/2020"

import os
from optparse import OptionParser

def start():
    parser = OptionParser()
    parser.add_option("-u", "--neoUser", help="specify a username for the neo4j database")
    parser.add_option("-p", "--neoPass", help="specify a password for the neo4j database")
    parser.add_option("-n", "--neoURL", help="specify the bolt url for the neo4j database")
    parser.add_option("-s", "--solrUrl")
    parser.add_option("-W", "--wipe", action="store_true", dest="wipe", help="wipe Neo4j")
    parser.add_option("-d", "--datasources", help="load the datasource file")
    parser.add_option("-t", "--terms", help="load the term file")
    parser.add_option("-m", "--mappings", help="load the mapping file")
    parser.add_option("-c", "--config", help="config file")
    parser.add_option("--doNotWipeSolr", action="store_true", help="Prevents Solr to be whiped before the index gets created.")
    parser.add_option("-a", "--additionalFilesToLoad", action="store_true", help="Skips (re)building a solr index. Use this option e.g. if you want to import more files into Neo4j before creating a solr index")
    (options, args) = parser.parse_args()

    parametersDataLoader= ['', ' -u ' + str(options.neoUser)][options.neoUser!= None] + \
                          ['', ' -p ' + str(options.neoPass)][options.neoPass != None] + \
                          ['', ' -n ' + str(options.neoURL)][options.neoURL != None] + \
                          ['', ' -W '][options.wipe != None]+ \
                          ['', ' -d ' + str(options.datasources)][options.datasources != None] + \
                          ['', ' -t ' + str(options.terms)][options.terms != None] + \
                          ['', ' -m ' + str(options.mappings)][options.mappings != None] + \
                          ['', ' -c ' + str(options.config)][options.config != None]

    os.system("python  oxoloader/OxoNeo4jLoader.py "+ parametersDataLoader)
    if options.additionalFilesToLoad:
        print("Building the solr index was skipped")
        return (0)
    else:
        parametersSolr = ['', ' -u ' + str(options.neoUser)][options.neoUser!= None] + \
                         ['', ' -p ' + str(options.neoPass)][options.neoPass != None] + \
                         ['', ' -n ' + str(options.neoURL)][options.neoURL != None] + \
                         ['', ' -s ' + str(options.solrUrl)][options.solrUrl != None] + \
                         [' -W ', ''][options.doNotWipeSolr != None]

            #The solr index will be wiped and recreated.
        os.system("python  oxoloader/SolrIndexer.py" + parametersSolr)
    return(0)

if __name__ == '__main__':
    start()