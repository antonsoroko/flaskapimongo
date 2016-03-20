# flaskapimongo

The test task - json api application based on flash and mongodb.

Start with:
```
vagrant up
```

Ansible playbook will be applied automatically by vagrant provisioning at the first boot.

Then you can re-run it by:

```
$ vagrant provision
```

Application will be available at [http://localhost:8080/](http://localhost:8080/)

POST url is /post, GET url is /get.

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
