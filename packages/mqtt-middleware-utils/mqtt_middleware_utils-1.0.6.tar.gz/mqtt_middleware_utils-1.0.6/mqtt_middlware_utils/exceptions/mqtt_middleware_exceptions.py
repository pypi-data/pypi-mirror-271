
class MiddlewareConfigurationException(Exception):
    '''
    Raised when the provided configuration in not valid
    '''
    pass


class UuidGenerationError(Exception):
    '''
    Raised when an error occurs with the creation of an UUID
    '''
    pass


class SshRemoteError(Exception):
    '''
    Raised when an error occurs with a remote ssh connection session
    This can occurr while establishing a new connection or with the exection of a remote command
    '''
    pass


class SshCommandExecutionError(Exception):
    '''
    Raised when the execution of a remote ssh command fails
    '''
    pass


class DatabaseError(Exception):
    '''
    Generic database exception raised when an error occurs while interacting with the database
    '''
    pass


class DatabaseConnectionError(Exception):
    '''
    Raised when an error occurs while connecting to the database server
    '''
    pass


class DatabasePersistenceError(Exception):
    '''
    Raised when an error occurs while persisting an object to the database
    '''
    pass


class DatabaseUpdateError(Exception):
    '''
    Raised when an error occurs while updating an object
    '''
    pass


class DatabaseDeleteError(Exception):
    '''
    Raised when an error occurs while deleting an object
    '''
    pass


class DatabaseCreateIndexError(Exception):
    '''
    Raised when an error occurs when creating an index on the database
    '''
    pass


class DatabaseObjectNotFoundError(Exception):
    '''
    Raised when the requested object is not found in the database
    '''
    pass


class DatabaseObjectRetrieveError(Exception):
    '''
    Raised when an error occurs when retrieving an object from the database
    '''
    pass


class DatabaseIndexSearchError(Exception):
    '''
    Raised when an error occurs when searching the requested indexes
    '''
    pass


class LoggerInitException(Exception):
    '''
    Raised when an error occurs when initializing the logger
    '''
    pass


class LoggerException(Exception):
    '''
    Raised when a generic error occurs when logging.
    '''
    pass
