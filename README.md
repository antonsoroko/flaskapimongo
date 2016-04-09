# flaskapimongo

The test task - JSON API application based on flask and mongodb. See task description  [here](DESCRIPTION.md).

Start with:
```
vagrant up
```

Application will be available at [http://localhost:8080/](http://localhost:8080/)

POST url is /post, GET url is /get.

Ansible playbook will be applied automatically by vagrant provisioning at the first boot.

Then you can re-run it (after commiting some changes for example) by:

```
$ vagrant provision
```

Application will be updated and restarted.


You can run unit test by doing following (if you have mongodb installed on localhost - you can do it in repo dir, otherwise inside vagrant VM in /opt/flaskapimongo/ dir):

```
$ . venv/bin/activate
$ python -m unittest discover -v
test_bad_input_data_in_get (tests.TestCase)
Send bad data to /get ... ok
test_bad_input_data_in_post (tests.TestCase)
Send bad data to /post ... ok
test_good_and_bad (tests.TestCase)
Post array of 2 json objects to /post. First object a good one, second a bad one. ... ok
test_non_array_post (tests.TestCase)
Post 10 objects one by one (not in array). ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.630s

OK
```

Also you can do some manual test using manual_tests.sh, or fill up database with fill_db.py:
```
$ ./manual_tests.sh 
HTTP/1.1 201 CREATED
Server: gunicorn/19.4.5
Date: Sun, 20 Mar 2016 18:15:29 GMT
Connection: close
Content-Type: application/json
Content-Length: 64

{
  "0": "OK", 
  "1": "FAIL", 
  "execution_time": "0.01167s"
}

HTTP/1.1 200 OK
Server: gunicorn/19.4.5
Date: Sun, 20 Mar 2016 18:15:29 GMT
Connection: close
Content-Type: application/json
Content-Length: 81

{
  "count": 1, 
  "execution_time": "0.00672s", 
  "status": "OK", 
  "uid": 1
}

HTTP/1.1 200 OK
Server: gunicorn/19.4.5
Date: Sun, 20 Mar 2016 18:15:29 GMT
Connection: close
Content-Type: application/json
Content-Length: 81

{
  "count": 0, 
  "execution_time": "0.00315s", 
  "status": "OK", 
  "uid": 2
}
```

```
$ ./fill_db.py
$ curl -i 'http://127.0.0.1:8080/get?uid=999&date=2016-03-20'
HTTP/1.1 200 OK
Server: gunicorn/19.4.5
Date: Sun, 20 Mar 2016 18:36:19 GMT
Connection: close
Content-Type: application/json
Content-Length: 87

{
  "count": 80000, 
  "execution_time": "0.03375s", 
  "status": "OK", 
  "uid": 999
}
```

#### License

Licensed under the GPLv3 License. See the [LICENSE](LICENSE) file for details.
