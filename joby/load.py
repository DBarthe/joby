import datetime
import requests
import time
from cassandra.cqlengine import ValidationError
from cassandra.cqlengine.query import BatchQuery

from joby import models
from joby.logs import log
from joby.models import Job


def load():
    models.setup()
    base_url = "http://service.dice.com"
    path = "/api/rest/jobsearch/v1/simple.json?sort=1"
    for page_num in range(70000):
        page = get_page(base_url + path)
        save_page(page, page_num)
        path = page['nextUrl']


def get_page(url):
    log.info("requesting dice api {}".format(url))
    r = requests.get(url)
    log.info("response code is {}".format(r.status_code))
    if r.status_code != 200:
        log.error(r.text)
        raise RuntimeError
    return r.json()


def save_page(page, page_num):
    log.info("saving page {}".format(page_num))
    with BatchQuery() as b:
        for job_item in page['resultItemList']:
            try:
                date = time.mktime(datetime.datetime.strptime(job_item['date'], "%Y-%m-%d").timetuple())
                job = Job.create(date=date,
                                 location_text=job_item['location'],
                                 title=job_item['jobTitle'],
                                 company=job_item['company'],
                                 url=job_item['detailUrl'],
                                 source='dice')
                job.batch(b).save()
            except ValidationError as e:
                log.warn("Problem loading {}: {}".format(job_item, e))


if __name__ == '__main__':
    load()
