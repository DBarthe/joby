import os

CASSANDRA_ENDPOINT = os.environ.get('CASSANDRA_ENDPOINTS', 'localhost').split(",")
MAIN_KEYSPACE = "jobs2"
REPLICATION_FACTOR = 1