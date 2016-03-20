import unittest
import datetime
import dateutil.relativedelta
import md5
import json
import urllib
from flaskapimongo import app, mongo


class TestCase(unittest.TestCase):


    db_name = "activity_log_unittest"
    good_uid = 1000
    good_name = "Vasya Pupkin"
    bad_uid = 1001
    bad_name = "Some Asshole"

    # I did not find the way to change database in
    # Flask-PyMongo on the fly. Need to re-init,
    # only once. So I have to use setUpClass.
    @classmethod
    def setUpClass(cls):
        app.config['TESTMONGO_DBNAME'] = cls.db_name
        mongo.init_app(app, config_prefix='TESTMONGO')


    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            mongo.cx.drop_database(cls.db_name)


    def setUp(self):
        app.config['TESTING'] = True
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 


    def tearDown(self):
        #clear activities after each test
        with app.app_context():
            mongo.db.activities.remove()


    def test_good_and_bad(self):
        """Post array of 2 json objects to /post. First object a good one, second a bad one.
        Then verify /get."""
        data = [{'uid': self.good_uid, 'name': self.good_name, 'date': datetime.datetime.now().isoformat()},
                {'uid': self.bad_uid, 'name': self.bad_name, 'date': datetime.datetime.now().isoformat()}]
        md5checksum = md5.new(json.dumps(data[0])).hexdigest()
        #good one
        data[0]['md5checksum'] = md5checksum
        #wrong one
        data[1]['md5checksum'] = md5checksum
        rv = self.app.post('/post',
            data=json.dumps(data),
            content_type = 'application/json')
        response = json.loads(rv.data)
        assert '0' in response and response['0'] == "OK", "Wrong result for good record"
        assert '1' in response and response['1'] == "FAIL", "Wrong result for bad record"
        #now GET
        uid = self.good_uid
        date = datetime.date.today()
        request = {'uid': uid, 'date': date}
        rv = self.app.get('/get?{0}'.format(urllib.urlencode(request)))
        response = json.loads(rv.data)
        assert response['uid'] == uid, "Wrong uid in response"
        assert response['status'] == "OK", "Wrong status in response"
        assert response['count'] == 1, "Wrong count in response"


    def test_non_array_post(self):
        """Post 10 objects one by one (not in array).
        Then verify /get."""
        uid = self.good_uid
        name = self.good_name
        for i in xrange(10):
            data = {'uid': uid, 'name': name, 'date': datetime.datetime.now().isoformat()}
            md5checksum = md5.new(json.dumps(data)).hexdigest()
            data['md5checksum'] = md5checksum
            rv = self.app.post('/post',
                data=json.dumps(data),
                content_type = 'application/json')
            response = json.loads(rv.data)
            assert '0' in response and response['0'] == "OK", "Wrong result for good record"
        #now GET
        date = datetime.date.today()
        request = {'uid': uid, 'date': date}
        rv = self.app.get('/get?{0}'.format(urllib.urlencode(request)))
        response = json.loads(rv.data)
        assert response['uid'] == uid, "Wrong uid in response"
        assert response['status'] == "OK", "Wrong status in response"
        assert response['count'] == 10, "Wrong count in response"


    def test_bad_input_data_in_get(self):
        """Send bad data to /get"""
        #wrong format
        request = {'some': 1, 'thing': 2}
        rv = self.app.get('/get?{0}'.format(urllib.urlencode(request)))
        response = json.loads(rv.data)
        assert response['status'] == 400, "Application does not check presence of needed args"
        #wrong data
        request = {'uid': 1, 'date': "2016-03-191"}
        rv = self.app.get('/get?{0}'.format(urllib.urlencode(request)))
        response = json.loads(rv.data)
        assert response['status'] == "FAIL", "Application does not check values of args"


    def test_bad_input_data_in_post(self):
        """Send bad data to /post"""
        #without content_type header
        data = [{'uid': self.good_uid, 'name': self.good_name, 'date': datetime.datetime.now().isoformat()}]
        rv = self.app.post('/post',
            data=json.dumps(data))
        response = json.loads(rv.data)
        assert response['status'] == 400, "Application accepts POST without proper content_type"
        #POST data is not JSON
        data = "hello there"
        rv = self.app.post('/post',
            data=data,
            content_type = 'application/json')
        response = json.loads(rv.data)
        assert response['status'] == 400, "Application accepts non JSON data"
        #wrong format
        data = [{'uid': self.good_uid, 'name': self.good_name}]
        rv = self.app.post('/post',
            data=json.dumps(data),
            content_type = 'application/json')
        response = json.loads(rv.data)
        assert response['0'] == "FAIL", "Application does not check presence of needed fields"
        #wrong data
        data = {'uid': self.good_name, 'name': self.good_name, 'date': datetime.datetime.now().isoformat()}
        md5checksum = md5.new(json.dumps(data)).hexdigest()
        data['md5checksum'] = md5checksum
        rv = self.app.post('/post',
            data=json.dumps(data),
            content_type = 'application/json')
        response = json.loads(rv.data)
        assert response['0'] == "FAIL", "Application does not check values of args"


if __name__ == '__main__':
    unittest.main()
