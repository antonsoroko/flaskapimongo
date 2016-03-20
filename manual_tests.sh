curl -H "Content-type: application/json" -i http://127.0.0.1:8080/post -X POST --data '[{"date": "2015-05-12T14:36:00.451765", "uid": "1", "md5checksum": "e8c83e232b64ce94fdd0e4539ad0d44f", "name": "John Doe"}, {"date": "2015-05-13T14:36:00.451765", "uid": "2", "md5checksum": "13065eda9a6ab62be1e63276cc7c46b1", "name": "Jane Doe"}]'
curl -i 'http://127.0.0.1:8080/get?uid=1&date=2015-05-12T14:36:00.451765'
curl -i 'http://127.0.0.1:8080/get?uid=2&date=2015-05-13T14:36:00.451765'

