import os

CASSANDRA_ENDPOINT = os.environ.get('CASSANDRA_ENDPOINTS', 'localhost').split(",")
MAIN_KEYSPACE = os.environ.get("MAIN_KEYSPACE", "jobs")
REPLICATION_FACTOR = 1
TOPOLOGY = os.environ.get('TOPOLOGY', 'network')
DC = os.environ.get('DC', 'DC1')
