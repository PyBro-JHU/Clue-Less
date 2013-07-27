"""
This _init__ code implements the DatabaseHandler as a Singelton by
instantiating the handler once to establish a single db connection pool
and then allowing modules to import the handler with the get_db_handler()
function
"""
from clueless.datastore.handler import DatabaseHandler

_DB_HANDLER = DatabaseHandler()


def get_db_handler():
    return _DB_HANDLER
