import unittest
import time
import random
from datetime import datetime

from flask import Flask

from app import create_app 
from app.cache import cache

class TestFlaskCache(unittest.TestCase):
    def setUp(self):
        self.app = create_app()

        with self.app.app_context(): 
            cache.clear()

    def test_set_get(self):
        with self.app.app_context():
            cache.set('key', 'value')
            self.assertEqual(cache.get('key'), 'value')

    def test_set_timeout(self):
        with self.app.app_context(): 
            cache.set('key', 'value', timeout=1)
            time.sleep(2)

            self.assertEqual(cache.get('key'), None)
        
    def test_memoize(self):
        with self.app.app_context(): 
            @cache.memoize(timeout=50)
            def rand(x, y):
                return random.randrange(0, 100)

            random.seed(datetime.now())
            ret = rand(1, 2)
            print('ret = {}'.format(ret))

            ret2 = rand(1, 2)
            self.assertEqual(ret, ret2)            

if __name__ == "__main__":
    unittest.main()

