#!/usr/bin/env python

import json
import md5
import urllib2
import sys
from datetime import timedelta
from datetime import datetime
from multiprocessing import Pool
import time


def send_data(delta):
    global start_date
    date = start_date + timedelta(seconds=+delta)
    data = {'uid': uid, 'name': name, 'date': date.isoformat()}
    checksum = md5.new(json.dumps(data)).hexdigest()
    data['md5checksum'] = checksum
    req = urllib2.Request(url)
    req.add_header('Content-Type', 'application/json')
    urllib2.urlopen(req, json.dumps(data))
    #response = urllib2.urlopen(req, json.dumps(data))
    #print json.load(response)


if __name__ == '__main__':
    uid = 999
    name = "Vasya Pupkin"
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    url = "http://127.0.0.1:8080/post"

    deltas = range(80000)

    pool = Pool(4)
    results = pool.map(send_data, deltas)
    pool.close()
    pool.join()

    sys.exit(0)
