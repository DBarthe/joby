from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table, create_keyspace_network_topology
from cassandra.cqlengine.models import Model

from joby import settings
from joby.logs import log


class Job(Model):
    log.info("Define Job model")
    location_text = columns.Text(partition_key=True, min_length=1)
    date = columns.DateTime(primary_key=True, clustering_order='DESC')
    company = columns.Text(primary_key=True, min_length=1)
    title = columns.Text(primary_key=True, min_length=1)
    source = columns.Text(primary_key=True, min_length=1)
    location = columns.Text(required=False, static=True)
    url = columns.Text()
    description = columns.Text(required=False)
    keywords = columns.List(value_type=columns.Text, required=False)


def setup():
    log.info("Setup cassandra connection")
    connection.setup(settings.CASSANDRA_ENDPOINT, settings.MAIN_KEYSPACE)

    log.info("Create keyspace")
    create_keyspace_network_topology(settings.MAIN_KEYSPACE, {"1": settings.REPLICATION_FACTOR})

    log.info("Sync table")
    sync_table(Job)

if __name__ == '__main__':
    setup()
