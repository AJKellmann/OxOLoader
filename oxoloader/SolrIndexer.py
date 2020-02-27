#!/usr/bin/env python
"""
Script for loading large amount sof data in OxO formatted CSV files into a OxO Neo4j.
You can delete the neo4j database, load datasoruces, terms and mapping files with this script
"""
__author__ = "kellmann"
__license__ = "Apache 2.0"
__date__ = "14/02/2020"

from neo4j.v1 import GraphDatabase, basic_auth
from optparse import OptionParser
import pysolr

class SolrIndexer():
    def __init__(self):
        parser = OptionParser()
        parser.add_option("-u", "--neoUser", default="neo4j", help="specify a username for the neo4j database")
        parser.add_option("-p", "--neoPass", default="dba", help="specify a password for the neo4j database")
        parser.add_option("-n", "--neoURL", default="bolt://localhost:7687", help="specify the bolt url for the neo4j database")
        parser.add_option("-s", "--solrUrl", default="http://localhost:8983/solr/mapping/")
        parser.add_option("-W","--wipe", action="store_true", dest="wipe", help="wipe the solr database")

        #Reading the given parameters
        (options, args) = parser.parse_args()
        uri = options.neoURL
        neoUser = options.neoUser
        neoPass = options.neoPass
        solrUrl = options.solrUrl

        #Connecting to Neo4j
        print("Connecting to Neo4j")
        driver = GraphDatabase.driver(uri, auth=basic_auth(neoUser, neoPass))
        self.session = driver.session()

        #Connecting to Solr
        print("Connecting to Solr")
        solr = pysolr.Solr(solrUrl)

        #Creates the different combinations of (alternative) Prefix and Identifier
        def create_dict(record):
            d = {'id': record["n.curie"]}
            d['identifier'] = [record["n.id"]]
            for Prefix in record["d.alternatePrefix"]:
                d['identifier'].append(Prefix + ":" + record["n.id"])
                d['identifier'].append(Prefix + "_" + record["n.id"])
            return d

        #Delete the exisitng Solr Index
        if options.wipe:
            print("Deleting Solr Index")
            solr.delete(q='*:*')

        #Query Neo4j
        result = self.session.run("MATCH (n:Term)-[:HAS_SOURCE]->(d:Datasource) RETURN n.curie, n.id, d.alternatePrefix")

        #Split the Results in Chunks and load them into Solr
        print("Creating Solr Index")
        chunksize=10000
        n=0
        temp_list=[]
        for record in result:
            temp_list.append(create_dict(record))
            if len(temp_list)<chunksize:
                continue
            solr.add(temp_list)
            temp_list.clear()
            n += 1
            print(str((chunksize*n))+" entries created")
            print("Solr Index created for " + str((chunksize * n + len(temp_list))) + " entries")
        solr.add(temp_list)
        print(str((chunksize * n+len(temp_list))) + " entries created")
        print("Solr Index created for "+str((chunksize * n+len(temp_list))) + " entries")

if __name__ == '__main__':
    SolrIndexer()