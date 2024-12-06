#!/usr/bin/env python3
import multiprocessing
import time
import unittest
import urllib.error
import urllib.request

import web_server, web_server_async


def check_ok(case):
    r = urllib.request.urlopen('http://localhost:8000')
    case.assertEqual(r.status, 200)
    case.assertEqual(r.read().decode('utf8'), '200 OK')

def check_not_found(case):
    with case.assertRaises(urllib.error.HTTPError) as cm:
        urllib.request.urlopen('http://localhost:8000/not-found')
    case.assertEqual(str(cm.exception), 'HTTP Error 404: Not Found')


class AsyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = multiprocessing.Process(target=web_server_async.run)
        cls.p.start()

    @classmethod
    def tearDownClass(cls):
        cls.p.terminate()

    def test_ok(self):
        check_ok(self)

    def test_not_found(self):
        check_not_found(self)


class WebServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = multiprocessing.Process(target=web_server.main)
        cls.p.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.p.terminate()

    def test_ok(self):
        check_ok(self)

    def test_not_found(self):
        check_not_found(self)


if __name__ == '__main__':
    unittest.main()
