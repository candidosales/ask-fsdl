"""Functions to connect to a document store and fetch documents from it."""
CONFIG = {"MONGO_DATABASE": "fsdl", "MONGO_COLLECTION": "ask-fsdl"}


def get_documents(collection=None, db=None, client=None, query=None):
    """Fetches a collection of documents from a document database."""
    collection = get_collection(collection, db, client)

    query = query or {"metadata.ignore": False}
    docs = collection.find(query)

    return docs


def drop(collection=None, db=None, client=None):
    """Drops a collection from the database."""
    collection = get_collection(collection, db, client)

    collection.drop()


def query(query, projection=None, collection=None, db=None):
    """Runs a query against the document db and returns a list of results."""
    import docstore

    collection = docstore.get_collection(collection, db)

    return list(collection.find(query, projection))


def query_one(query, projection=None, collection=None, db=None):
    """Runs a query against the document db and returns the first result."""
    import docstore

    collection = docstore.get_collection(collection, db)

    return collection.find_one(query, projection)


def get_collection(collection=None, db=None, client=None):
    """Accesses a specific collection in the document store."""
    import pymongo

    db = get_database(db, client)

    collection = collection or CONFIG["MONGO_COLLECTION"]

    if isinstance(collection, pymongo.collection.Collection):
        return collection
    else:
        collection = db.get_collection(collection)
        return collection


def get_database(db=None, client=None):
    """Accesses a specific database in the document store."""
    import pymongo

    client = client or connect()

    db = db or CONFIG["MONGO_DATABASE"]
    if isinstance(db, pymongo.database.Database):
        return db
    else:
        db = client.get_database(db)
        return db


def connect(user=None, password=None, uri=None):
    """Connects to the document store, here MongoDB."""
    import os
    import urllib

    import pymongo

    mongodb_user = user or os.environ["MONGODB_USER"]
    mongodb_user = urllib.parse.quote_plus(mongodb_user)

    mongodb_password = password or os.environ["MONGODB_PASSWORD"]
    mongodb_password = urllib.parse.quote_plus(mongodb_password)

    mongodb_host = uri or os.environ["MONGODB_HOST"]

    connection_string = f"mongodb+srv://{mongodb_user}:{mongodb_password}@{mongodb_host}/?retryWrites=true&w=majority"

    client = pymongo.MongoClient(connection_string, connect=True, appname="ask-fsdl")

    return client
