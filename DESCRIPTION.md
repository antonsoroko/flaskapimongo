Write a small Flask web application that will listen on port 8080.

The Flask application should have only 2 endpoints.

The first endpoint should accept only POST requests which will have a json payload.


The JSON payload will be:
```
   [{"uid": "1",
   "name": "John Doe",
   "date": "2015-05-12T14:36:00.451765",
   "md5checksum": "e8c83e232b64ce94fdd0e4539ad0d44f"},

   {"uid": "2"
   "name": "Jane Doe",
   "date": "2015-05-13T14:36:00.451765",
   "md5checksum": "b419795d50db2a35e94c8364978d898f"},

   ...]
```

The endpoint should store the data in a mongo data store.

Before storing the data we need to make sure that the checksum for each JSON object (just fields: uid, name and date) is correct and matches the original checksum in the JSON payload.

For instance for the first object we would need to check the checksum for the following json string: '{"date": "2015-05-12T14:36:00.451765", "uid": "1", "name": "John Doe"}'.


The second Endpoint should only accept GET requests with an uid parameter and a date parameter. Given a uid and a date the endpoint should return the number of occurrences of a given UID for that day.


Write tests for the application.
