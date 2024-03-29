#!/usr/bin/env python
"""
Script for loading large amounts of data in OxO formatted CSV files into a OxO Neo4j.
You can delete the neo4j database, load datasoruces, terms and mapping files with this script
"""
__author__ = "jupp, kellmann"
__license__ = "Apache 2.0"
__date__ = "07/02/2020"

from neo4j.v1 import GraphDatabase, basic_auth
import configparser
from optparse import OptionParser

class Neo4jOxOLoader:
    def __init__(self):

        parser = OptionParser()
        parser.add_option("-d","--datasources",  help="load the datasource file")
        parser.add_option("-t","--terms", help="load the term file")
        parser.add_option("-m","--mappings", help="load the mapping file")
        parser.add_option("-W","--wipe", action="store_true", dest="wipe", help="wipe the neo4j database")
        parser.add_option("-u","--neoUser", help="specify a username for the neo4j database")
        parser.add_option("-p","--neoPass", help="specify a password for the neo4j database")
        parser.add_option("-n","--neoURL", help="specify the bolt url for the neo4j database")
        parser.add_option("-c","--config", help="config file")

        (options, args) = parser.parse_args()
        uri=None
        neoUser=None
        neoPass=None
        defaultNeoUser = "neo4j" #options.neoUser
        defaultNeoPass = "dba" #options.neoPass
        #defaultUri = "bolt://172.17.0.1:7687"
        defaultUri ="bolt://localhost:7687"#options.neoURL

        #First check for the config file:
        if options.config:
            config = configparser.ConfigParser()
            config.read(options.config)
            if len(config.sections()) > 0:
                try:
                    uri = config.get("Basics", "neoURL")
                except:
                    pass
                try:
                    neoUser = config.get("Basics", "neoUser")
                except:
                    pass
                try:
                    neoPass = config.get("Basics", "neoPass")
                except:
                    pass
            else:
                print("Couldn't find the config file")
                exit("1")

        #Then check for the options:
        if options.neoURL:
            uri = options.neoURL
        if options.neoUser:
            neoUser = options.neoUser
        if options.neoPass:
            neoPass = options.neoPass

        #In case anything is not set yet, overwrite it with defaults:
        if uri is None: uri=defaultUri
        if neoUser is None: neoUser = defaultNeoUser
        if neoPass is None: neoPass = defaultNeoPass

        #Connecting to Neo4j
        driver = GraphDatabase.driver(uri, auth=basic_auth(neoUser, neoPass))
        self.session = driver.session()

        self.session.run("CREATE CONSTRAINT ON (i:Term) ASSERT i.curie IS UNIQUE")
        self.session.run("CREATE CONSTRAINT ON (i:Datasource) ASSERT i.prefix IS UNIQUE")

        if options.wipe:
            while self.deleteMappings() > 0:
                print("Still deleting...")
            print("Mappings deleted!")

            while self.deleteSourceRels() > 0:
                print ("Still deleting...")
            print("Source rels deleted!")

            while self.deleteTerms() > 0:
                print("Still deleting...")
            print("Terms deleted!")

            while self.deleteDatasources() > 0:
                print("Still deleting...")
            print("Datasources deleted!")

        if options.datasources:
            self.loadDatasources(options.datasources)
        if options.terms:
            self.loadTerms(options.terms)
        if options.mappings:
            self.loadMappings(options.mappings)


    def deleteMappings(self):
        result = self.session.run("match (t)-[m:MAPPING]->() WITH m LIMIT 50000 DETACH DELETE m RETURN count(*) as count")
        for record in result:
            return record["count"]

    def deleteSourceRels(self):
        result = self.session.run("match (t)-[m:HAS_SOURCE]->()  WITH m LIMIT 50000 DETACH DELETE m RETURN count(*) as count")
        for record in result:
            return record["count"]

    def deleteTerms(self):
        result = self.session.run("match (t:Term) WITH t LIMIT 50000 DETACH DELETE t RETURN count(*) as count")
        for record in result:
            return record["count"]

    def deleteDatasources(self):
        result = self.session.run("match (d:Datasource) WITH d LIMIT 1000 DETACH DELETE d RETURN count(*) as count")
        for record in result:
            return record["count"]

    def loadTerms(self, terms):
        print ("Loading terms from "+terms+"...")

        loadTermsCypher = "USING PERIODIC COMMIT 10000 LOAD CSV WITH HEADERS FROM 'file:///"+terms+"""' AS line
                        MATCH (d:Datasource {prefix : line.prefix})
                        WITH d, line
                        MERGE (t:Term { curie: line.curie})
                        SET t.id = line.identifier, t.label = line.label, t.uri = line.uri
                        with t,d
                        CREATE (t)-[:HAS_SOURCE]->(d)"""
        result = self.session.run(loadTermsCypher)
        print (result.summary())


    def loadMappings(self, mappings):
        print("Loading mappings from "+mappings+"...")
        loadMappingsCypher = "USING PERIODIC COMMIT 10000 LOAD CSV WITH HEADERS FROM 'file:///"+mappings+"""' AS line
                        MATCH (f:Term { curie: line.fromCurie}),(t:Term { curie: line.toCurie})
                        WITH f,t,line
                        CREATE (f)-[m:MAPPING {sourcePrefix: line.datasourcePrefix, datasource:line.datasourcePrefix ,sourceType: line.sourceType, scope: line.scope, date: line.date}]->(t)"""

        result = self.session.run(loadMappingsCypher)
        print (result.summary())

    def loadDatasources(self, datasources):
        print ("Loading datasources from " + datasources + " ...")
        loadDatasourcesCypher = """
            LOAD CSV WITH HEADERS FROM 'file:///"""+datasources+"""' AS line
            WITH line
            MERGE (d:Datasource {prefix : line.prefix})
            WITH d, line
            SET d.preferredPrefix = line.prefix, d.name = line.title, d.description = line.description, d.versionInfo = line.versionInfo, d.idorgNamespace = line.idorgNamespace, d.licence = line.licence, d.sourceType = line.sourceType, d.alternatePrefix = split(line.alternatePrefixes,",")
            """
        result = self.session.run(loadDatasourcesCypher)
        print (result.summary())

if __name__ == '__main__':
    Neo4jOxOLoader()
