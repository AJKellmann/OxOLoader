# OxO Loader 

Goal of this project was to rewrite some files for EBI's OxO that allows to load some data into OxO.
The first step is loading data from formatted CSV files into a Neo4j graph database.
To increase the search speed within the data, it gets indexed by Solr.

Currently there are two python scripts doing this job. - They do work properly.
The idea was to dockerize this process, but the docker file is not properly set up yet.
