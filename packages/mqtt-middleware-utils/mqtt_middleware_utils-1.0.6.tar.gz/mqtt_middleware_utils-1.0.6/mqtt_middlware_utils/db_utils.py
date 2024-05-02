import redis

from redis.commands.json.path import Path
from redis.commands.search.query import Query
from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType

from mqtt_middlware_utils.exceptions.mqtt_middleware_exceptions import DatabaseError, DatabaseObjectNotFoundError, DatabaseConnectionError, DatabasePersistenceError, DatabaseCreateIndexError, DatabaseUpdateError, DatabaseDeleteError, DatabaseObjectRetrieveError, DatabaseIndexSearchError


def db_exceptions_decorator(func):
    '''
    This decorator function avoids code duplication between database functions for error handling.

    @param func: the function to be decorated   

    @returns: the return value of the decorated function

    @raise DatabaseObjectNotFoundError if the desired database object is not found.
    @raise DatabaseConnectionError if an error occurrs during database connection.
    @raise DatabasePersistenceError if an error occurrs during database persistence.
    @raise DatabaseUpdateError if an error occurrs during database update.
    @raise DatabaseDeleteError if an error occurrs during database deletion.
    @raise DatabaseCreateIndexError if an error occurrs during database creation of an index.
    @raise DatabaseObjectRetrieveError if an error occurrs during database retrieval of an object.
    @raise DatabaseIndexSearchError if an error occurrs during database search of an index.s
    @raise DatabaseError if a generic error occurrs during database operations.

    '''
    def function_wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseObjectNotFoundError:
            raise
        except DatabaseConnectionError:
            raise
        except DatabasePersistenceError:
            raise
        except DatabaseUpdateError:
            raise
        except DatabaseDeleteError:
            raise
        except DatabaseCreateIndexError:
            raise
        except DatabaseObjectRetrieveError:
            raise
        except DatabaseIndexSearchError:
            raise
        except Exception as e:
            raise DatabaseError(
                "The following error occurred while operating on the database: \n"+str(e))
    return function_wrapper


@db_exceptions_decorator
def get_new_connection(host, username, password, port=6379, db=0, ssl=False, ssl_certfile=None,
                       ssl_keyfile=None, ssl_ca_certs=None, decode_responses=False):
    '''
    Get a new connection to a redis server using the provided credentials.

    @param host: the hostname of the redis server
    @param username: the username to connect to the redis server
    @param password: the password to connect to the redis server
    @param port: the port to connect to the redis server
    @param db: the database to connect to
    @param ssl: whether or not to use ssl
    @param ssl_certfile: the path to the ssl certificate file
    @param ssl_keyfile: the path to the ssl key file
    @param ssl_ca_certs: the path to the ssl certificate authority file
    @param decode_responses: whether or not to decode responses from the redis server

    @return: a new redis connection

    @raise DatabaseConnectionError if an error occurrs during database connection.  
    '''
    try:
        conn = None
        if (ssl):
            conn = redis.Redis(host=host, port=port, username=username, password=password, db=db,
                               ssl=ssl, ssl_certfile=ssl_certfile, ssl_keyfile=ssl_keyfile,
                               ssl_ca_certs=ssl_ca_certs, decode_responses=decode_responses)
        else:
            conn = redis.Redis(host=host, port=port, username=username, password=password, db=db,
                               decode_responses=decode_responses)
        return conn
    except Exception as e:
        raise DatabaseConnectionError(
            "The following error occurred trying to connect to database with params [ (host: " +
            str(host)+") (port: " + str(port) + ") (username: " + str(username) + ") (password: "+str(password) +
            ") (db: "+str(db)+") (ssl: "+str(ssl)+") (ssl_certfile: "+str(ssl_certfile)+") (ssl_keyfile: "+str(ssl_keyfile) +
            ") (ssl_ca_certs: "+str(ssl_ca_certs)+") (decode_responses: "+str(decode_responses)+") ]: "+str(e))


@db_exceptions_decorator
def get_new_connection_no_login(host, port=6379, db=0, ssl=False, ssl_certfile=None,
                                ssl_keyfile=None, ssl_ca_certs=None, decode_responses=False):
    '''
    Get a new connection to a redis server using the default credentials.

    @param host: the hostname of the redis server
    @param port: the port to connect to the redis server
    @param db: the database to connect to
    @param ssl: whether or not to use ssl
    @param ssl_certfile: the path to the ssl certificate file  
    @param ssl_keyfile: the path to the ssl key file
    @param ssl_ca_certs: the path to the ssl certificate authority file
    @param decode_responses: whether or not to decode responses from the redis server 

    @return: a new redis connection 

    @raise DatabaseConnectionError if an error occurrs during database connection.
    '''
    try:
        conn = None
        if (ssl):
            conn = redis.Redis(host=host, port=port, db=db, ssl=ssl, ssl_certfile=ssl_certfile,
                               ssl_keyfile=ssl_keyfile, ssl_ca_certs=ssl_ca_certs,
                               decode_responses=decode_responses)
        else:
            conn = redis.Redis(host=host, port=port, db=db,
                               decode_responses=decode_responses)
        return conn
    except Exception as e:
        raise DatabaseConnectionError(
            "The following error occurred trying to connect to database with params [ (host: " +
            str(host)+") (port: " + str(port) + ") (db: "+str(db)+") (ssl: "+str(ssl)+") (ssl_certfile: "+str(ssl_certfile) +
            ") (ssl_keyfile: "+str(ssl_keyfile) + ") (ssl_ca_certs: " +
            str(ssl_ca_certs)+") (decode_responses: " + str(decode_responses)+") ]: \n"+str(e))


@db_exceptions_decorator
def persist_new_object(connection, object_name, new_object, source='$'):
    '''
    Persist a new object in the database using the provided connection.

    @param connection: the redis connection to use
    @param object_name: the name of the object to persist
    @param new_object: the object to persist
    @param source: the source of the object to persist

    @return: the persisted object

    @raise DatabasePersistenceError if an error occurrs during the persist operation.
    '''

    try:
        result = connection.json().set(object_name, source, new_object)
        # get the newly persisted object from the database
        return retrieve_object(connection, object_name)
    except Exception as e:
        raise DatabasePersistenceError(
            "The following error occurred trying to persist the object [(object_name: " +
            str(object_name) + ") (source: "+str(source)+")]: \n"+str(e))


@db_exceptions_decorator
def retrieve_object(connection, object_name, object_path=None):
    '''
    Retrieves an object from the database using the provided connection.

    @param connection: the redis connection to use
    @param object_name: the name of the object to retrieve
    @param object_path: the path to the object to retrieve

    @return: the retrieved object

    @raise DatabaseObjectRetrieveError if an error occurrs during the retrieve operation.
    '''
    try:
        result = None
        if (object_path is not None):
            result = connection.json().get(object_name, Path('.'+object_path))
        else:
            result = connection.json().get(object_name)
        return result
    except Exception as e:
        raise DatabaseObjectRetrieveError(
            "The following error occurred trying to retrieve the object [(object_name: " + str(object_name) + ")]: \n"+str(e))


@db_exceptions_decorator
def create_index(conn, index_name, schema, definition):
    '''
    Creates an index using the provided connection.

    @param connection: the redis connection to use
    @param index_name: the name of the index to create
    @param schema: the schema of the index to create
    @param definition: the definition of the index to create

    @return: the created index

    @raise DatabaseCreateIndexError if an error occurrs during the create index operation.
    '''
    try:
        idx = conn.ft(index_name)
        idx.create_index(schema, definition=definition)
        return idx
    except Exception as e:
        raise DatabaseCreateIndexError(
            "The following error occurred trying to create the index [(index_name: " +
            str(index_name) + ") (schema: "+str(schema)+") (definition: "+str(definition) +
            ")]: \n"+str(e))


@db_exceptions_decorator
def search_from_index(connection, index_name, query_string="*", offset=None, num=None):
    '''
    Performs a search on the index using the provided query string

    @param connection: the database connection (mandatory)
    @param index_name: the name of the index to search on (mandatory)
    @param query_string: the query string to use, if default searches all index (mandatory)
    @param offset: the offset from where to start returning results (optional)
    @param num: the number of results to return (optional)

    @return: the results of the search

    @raise DatabaseIndexSearchError if an error occurrs during the search operation on the index.
    '''
    try:
        query = Query(query_string)
        if offset is not None and num is not None:
            query.paging(offset, num)
        return connection.ft(index_name).search(query)
    except Exception as e:
        raise DatabaseIndexSearchError(
            "The following error occurred trying to search the index [(index_name: " +
            str(index_name) + ") (query_string: "+str(query_string)+")]: \n"+str(e))


@db_exceptions_decorator
def update_object(connection, object_name, to_update_object):
    '''
    Updates the object with the given name from the database using the provided connection.

    @param connection: the redis connection to use
    @param object_name: the name of the object to update
    @param to_update_object: the object to update

    @return: the updated object

    @raise DatabaseUpdateError if an error occurrs during the update operation.
    '''
    try:
        # try to find the object first
        obj_found = retrieve_object(connection, object_name)
        # if no object is found raise an exception
        if (obj_found == None):
            raise DatabaseObjectNotFoundError(
                "No object to update can be found with name %s" % object_name)
        # update otherwise
        return persist_new_object(connection, object_name, to_update_object)
    except DatabaseObjectNotFoundError:
        raise
    except Exception as e:
        raise DatabaseUpdateError(
            "The following error occurred trying to update the object [(object_name: " + object_name +
            ") (to_update_object: "+str(to_update_object)+")]: \n"+str(e))


@db_exceptions_decorator
def delete_object(connection, object_name):
    '''
    Deletes the object with the given name from the database using the provided connection.

    @param connection: the redis connection to use
    @param object_name: the name of the object to delete    

    @return: the number of deleted objects

    @raise DatabaseError if an error occurrs during the delete operation.
    '''
    try:
        return connection.json().delete(object_name)
    except Exception as e:
        raise DatabaseDeleteError(
            "The following error occurred trying to delete the object [(object_name: " + str(object_name) +
            ")]: \n"+str(e))
