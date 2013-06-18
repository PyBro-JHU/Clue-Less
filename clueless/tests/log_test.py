import logging
import unittest

from clueless import log


class WhenTestingGetLogger(unittest.TestCase):

    def test_get_logger_returns_logger_instance(self):
        logger = log.get_logger(__name__)

        #assert the object return is an instance of the
        # python built-in logging.Logger
        self.assertIsInstance(logger, logging.Logger)

        #assert that the logger was created with the specified name
        self.assertEqual(__name__, logger.name)
