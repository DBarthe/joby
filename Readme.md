# Joby

Tested with python 3.5.

Require access to an Apache Cassandra cluster, or better, an [Elassandra](https://github.com/strapdata/elassandra) cluster.

Install:
```bash
$ pip3 install joby
```

Load offers:
```bash
$ CASSANDRA_ENDPOINTS="X.X.X.X,Y.Y.Y.Y" python3 -m joby.load
```

Update location using a geocoder web service:
```bash
$ CASSANDRA_ENDPOINTS="X.X.X.X,Y.Y.Y.Y" python3 -m joby.geocode
```


