import unittest                                                                 
import json                     
import logging
import logging.config                                                
import os
                                                                                
from app import create_app                                                      
                                                                                
class TestLogger(unittest.TestCase):
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    info_log_filepath = '/tmp/info.log' # in logging.json              
    special_log_filepath = '/tmp/special.log' # in logging.json 

    def setup_logging(self):
        log_config_filepath = os.path.join(self.static_folder, 'logging.json')

        with open(log_config_filepath, "r", encoding="utf-8") as fd:          
            logging.config.dictConfig(json.load(fd))

    def setUp(self):         
        try:
            os.unlink(self.info_log_filepath)                                       
        except:
            pass

        try:
            os.unlink(self.special_log_filepath) 
        except:
            pass

        self.setup_logging()

    def test_log_special(self):
        message = 'hello special'

        logger = logging.getLogger('special')
        logger.info('hello special')

        info_content = ''
        with open(self.info_log_filepath) as f:
            info_content = f.read()

        special_content = ''                                                       
        with open(self.special_log_filepath) as f:                                 
            special_content = f.read()

        # propogate is false
        self.assertTrue(message not in info_content)
        self.assertTrue(message in special_content)

                                                                                
