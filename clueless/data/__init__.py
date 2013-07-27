"""
This _init__ code implements the DatabaseHandler as a Singelton by
instantiating the handler once to establish a single db connection pool
and then allowing modules to import the handler with the get_db_handler()
function
"""
from clueless.data import datastore

_DB_HANDLER = datastore.DatabaseHandler()


def get_db_handler():
    """
    returns a reference to the instantiated DatabaseHandler object
    """

    #if the handler does not have a live connection, connect to the datastore
    if _DB_HANDLER.status != datastore.STATUS_CONNECTED:
        _DB_HANDLER.connect()

    return _DB_HANDLER
