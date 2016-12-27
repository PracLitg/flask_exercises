# -*- coding:utf-8 -*-

import os
import tempfile
import unittest

import sys
sys.path.append("..")
from flaskr import flaskr

class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        # mkstemp: 返回一个文件句柄和一个随机文件名,句柄用来关闭文件
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.client = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])


    def test_empty_db(self):
        rv = self.client.get('/')
        assert b'No entries here so far' in rv.data


    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)


    def test_login_logout(self):
        rv = self.login(flaskr.app.config['USERNAME'],
                        flaskr.app.config['PASSWORD'])
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login(flaskr.app.config['USERNAME'] + 'x',
                    flaskr.app.config['PASSWORD'])
        assert b'Invalid username' in rv.data
        rv = self.login(flaskr.app.config['USERNAME'],
                    flaskr.app.config['PASSWORD'] + 'x')
        assert b'Invalid password' in rv.data


    def test_messages(self):
        self.login(flaskr.app.config['USERNAME'],
                flaskr.app.config['PASSWORD'])
        rv = self.client.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert b'No entries here so far' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data
    #'''


if __name__ == '__main__':
    unittest.main()
