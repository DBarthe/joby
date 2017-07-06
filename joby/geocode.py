from geopy import geocoders
import geohash2
from cassandra.query import SimpleStatement
from cassandra.cqlengine import connection

from joby import models, settings
from joby.logs import log

default_locator = geocoders.GoogleV3()


def geocode(location_text, locator=default_locator):
    location = locator.geocode(location_text, timeout=10)
    if location:
        return geohash2.encode(location.latitude, location.longitude, precision=7)
    else:
        return None


def update_one_partition(location_text, geohash):
    query = "UPDATE {}.job SET location = %(geohash)s WHERE location_text = %(text)s".format(settings.MAIN_KEYSPACE)
    statement = SimpleStatement(query)
    connection.session.execute(statement, dict(geohash=geohash, text=location_text))


def update_all():
    models.setup()
    query = "SELECT DISTINCT location_text, location FROM {}.job".format(settings.MAIN_KEYSPACE)
    statement = SimpleStatement(query, fetch_size=50)
    for row in connection.session.execute(statement):
        if row['location'] is not None:
            log.info("skipping {}".format(row['location_text']))
            continue
        else:
            log.info("geocoding {}".format(row['location_text']))
            try:
                geohash = geocode(row['location_text'])
                if geohash:
                    update_one_partition(row['location_text'], geohash)
            except Exception as e:
                log.info("problem geocoding {}: {}".format(row['location_text'], e))


if __name__ == '__main__':
    update_all()
