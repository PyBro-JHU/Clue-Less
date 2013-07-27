from pymongo import MongoClient


class DatabaseHandler():
    """
    An handler class to provide CRUD operations using MongoDB
    """

    def __init__(self):
        """
        Sets the address of the mongo server, specifies the database to use
        and connects to the server
        """
        self.server = 'localhost:27017'
        self.database_name = 'clueless'
        self._connect()

    def _connect(self):
        """
        Creates a connection with the MongoDB server and database
        """
        self.connection = MongoClient(self.server)
        self.database = self.connection[self.database_name]

    def close(self):
        """
        Closes the connection to the MongoDB server
        """
        self.connection.close()

    def insert_document(self, object_name, document=None):
        """
        inserts a new document into the specified collection
        """
        if document is None:
            document = dict()
        self.database[object_name].insert(document)

    def get_document(self, object_name, query_filter=None):
        """
        Retrieves a document from the MongoDB database using the
        specified collection and query filter
        """
        if query_filter is None:
            query_filter = dict()
        document = self.database[object_name].find_one(query_filter)
        #remove the mongodb _id form the document
        document.pop("_id")
        return document

    def update_document(self, object_name, document, query_filter=None):
        '''
        Updates an existing document that matches the query filter
        '''
        if query_filter is None:
            query_filter = dict()

        self.database[object_name].update(
            query_filter, document)

    def delete_document(self, object_name, query_filter=None, limit_one=False):
        """
        deletes all documents that match the query filter
        """
        if query_filter is None:
            query_filter = dict()
        self.database[object_name].remove(query_filter, True)
