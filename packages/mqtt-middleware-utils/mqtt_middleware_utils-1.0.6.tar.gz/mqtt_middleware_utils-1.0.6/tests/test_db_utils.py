import pytest

from unittest import TestCase
from unittest.mock import patch, Mock

import mqtt_middlware_utils.db_utils as utils


def simple_function_for_decorator_testing():
    pass


class TestDbUtils(TestCase):

    @patch('mqtt_middlware_utils.db_utils.redis.Redis', autospec=True)
    def test_get_new_connection(self, mock_redis_class):
        # mock redis.Redis in get_new_connection() in order to return a fake connection
        self.assertIs(utils.redis.Redis, mock_redis_class)
        mock_redis_class.return_value = "Connected"

        host = "localhost"
        username = "user"
        password = "user"

        redis_conn = utils.get_new_connection(host, username, password)

        assert redis_conn == "Connected"

    @patch('mqtt_middlware_utils.db_utils.redis.Redis', autospec=True)
    def test_get_new_connection_exception(self, mock_redis_class):
        with pytest.raises(utils.DatabaseConnectionError) as e:

            self.assertIs(utils.redis.Redis, mock_redis_class)
            mock_redis_class.side_effect = ValueError(
                "Something went wrong during connection")

            host = "localhost"
            username = "user"
            password = "user"

            utils.get_new_connection(host, username, password)
        assert "The following error occurred trying to connect to database" in str(
            e)
        assert "Something went wrong during connection" in str(e)

    @patch('mqtt_middlware_utils.db_utils.redis.Redis', autospec=True)
    def test_get_new_connection_no_login(self, mock_redis_class):
        # mock redis.Redis in get_new_connection() in order to return a fake connection
        self.assertIs(utils.redis.Redis, mock_redis_class)
        mock_redis_class.return_value = "Connected"

        host = "localhost"

        redis_conn = utils.get_new_connection_no_login(
            host)

        assert redis_conn == "Connected"

    @patch('mqtt_middlware_utils.db_utils.redis.Redis', autospec=True)
    def test_get_new_connection_no_login_exception(self, mock_redis_class):
        with pytest.raises(utils.DatabaseConnectionError) as e:

            self.assertIs(utils.redis.Redis, mock_redis_class)
            mock_redis_class.side_effect = ValueError(
                "Something went wrong during connection")

            host = "localhost"

            utils.get_new_connection_no_login(host)
        assert "The following error occurred trying to connect to database" in str(
            e)
        assert "Something went wrong during connection" in str(e)

    # TODO implement this test
    def test_get_new_connection_ssl(self):
        pass

    # TODO implement this test
    def test_get_new_connection_ssl_exception(self):
        pass

    # TODO implement this test
    def test_get_new_connection_no_login_ssl(self):
        pass

    # TODO implement this test
    def test_get_new_connection_no_login_ssl_exception(self):
        pass

    @patch('mqtt_middlware_utils.db_utils.retrieve_object', autospec=True)
    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_persist_new_object(self, mocked_get_new_connection, mocked_retrieve_object):
        object_to_persist = {"name": "John", "age": 30}

        mocked_connection = Mock()
        mocked_connection.json().set.return_value = "OK"
        mocked_get_new_connection.return_value = mocked_connection

        mocked_retrieve_object.return_value = object_to_persist

        host = "localhost"
        username = "test"
        password = "test"

        object_name = "test_object"

        # get a new connection
        connection = utils.get_new_connection(
            host=host, username=username, password=password)

        persisted_object = utils.persist_new_object(
            connection, object_name, object_to_persist)

        assert persisted_object == object_to_persist
        mocked_connection.json().set.assert_called_once_with(
            object_name, '$', object_to_persist)
        mocked_retrieve_object.assert_called_once_with(
            connection, object_name)

    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_persist_new_object_json_set_exception(self, mocked_get_new_connection):
        object_name = "test_object"
        with pytest.raises(utils.DatabasePersistenceError) as e:
            object_to_persist = {"name": "John", "age": 30}

            mocked_connection = Mock()
            mocked_connection.json().set.side_effect = ValueError("A generic error occurred")
            mocked_get_new_connection.return_value = mocked_connection

            # get a new connection
            connection = utils.get_new_connection(
                host="host", username="username", password="password")

            utils.persist_new_object(
                connection, object_name, object_to_persist)

        assert "The following error occurred trying to persist the object" in str(
            e)
        assert object_name in str(e)
        assert "A generic error occurred" in str(e)

    @patch('mqtt_middlware_utils.db_utils.persist_new_object', side_effect=utils.DatabasePersistenceError("A generic error occurred"), autospec=True)
    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_persist_new_object_generic_exception(self, mocked_get_new_connection, mocked_persist_new_object):
        with pytest.raises(utils.DatabasePersistenceError):
            mocked_connection = Mock()
            mocked_connection.json().set.return_value = "OK"
            mocked_get_new_connection.return_value = mocked_connection

            # get a new connection
            connection = utils.get_new_connection(
                host="localhost", username="test", password="test")

            # keep the decorator for the mocked function
            mocked_persist_new_object(connection, "test_object", {
                                      "name": "John", "age": 30})

    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_retrieve_object(self, mocked_get_new_connection):

        object_to_retrieve = {"name": "John", "age": 30}
        object_name = "test_object"

        mocked_connection = Mock()
        mocked_connection.json().get.return_value = object_to_retrieve
        mocked_get_new_connection.return_value = mocked_connection

        # get a new connection
        connection = utils.get_new_connection(
            host="localhost", username="test", password="test")

        retrieved_object = utils.retrieve_object(
            connection, object_name)

        assert retrieved_object == object_to_retrieve
        mocked_connection.json().get.assert_called_once_with(
            object_name)

    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_retrieve_object_object_path(self, mocked_get_new_connection):

        object_to_retrieve = {"name": "John", "age": 30}
        object_name = "test_object"
        object_path = '$'

        mocked_connection = Mock()
        mocked_connection.json().get.return_value = object_to_retrieve
        mocked_get_new_connection.return_value = mocked_connection

        # get a new connection
        connection = utils.get_new_connection(
            host="localhost", username="test", password="test")

        retrieved_object = utils.retrieve_object(
            connection, object_name, object_path)

        assert retrieved_object == object_to_retrieve

    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_retrieve_object_generic_exception(self, mocked_get_new_connection):
        with pytest.raises(utils.DatabaseObjectRetrieveError) as e:
            mocked_connection = Mock()
            mocked_connection.json().get.side_effect = ValueError("A generic error occurred")
            mocked_get_new_connection.return_value = mocked_connection

            # get a new connection
            connection = utils.get_new_connection(
                host="localhost", username="test", password="test")

            object_name = "test_object"

            utils.retrieve_object(connection, object_name)
        assert "The following error occurred trying to retrieve the object" in str(
            e)
        assert "A generic error occurred" in str(e)
        assert object_name in str(e)

    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_create_index(self, mocked_get_new_connection):
        mocked_index = Mock()
        mocked_index.create_index.return_value = "OK"

        mocked_connection = Mock()
        mocked_connection.ft.return_value = mocked_index
        mocked_get_new_connection.return_value = mocked_connection

        # get a new connection
        connection = utils.get_new_connection(
            host="localhost", username="test", password="test")

        index_name = "test_index"
        schema = "test_schema"
        definition = "test_definition"

        created_idx = utils.create_index(connection, index_name,
                                         schema, definition)

        assert created_idx == mocked_index
        mocked_connection.ft.assert_called_once_with(index_name)
        mocked_index.create_index.assert_called_once_with(
            schema, definition=definition)

    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_create_index_generic_exception(self, mocked_get_new_connection):
        with pytest.raises(utils.DatabaseCreateIndexError) as e:
            mocked_index = Mock()
            mocked_index.create_index.side_effect = ValueError(
                "A generic error occurred")

            mocked_connection = Mock()
            mocked_connection.ft.return_value = mocked_index
            mocked_get_new_connection.return_value = mocked_connection

            # get a new connection
            connection = utils.get_new_connection(
                host="localhost", username="test", password="test")

            index_name = "test_index"
            schema = "test_schema"
            definition = "test_definition"

            utils.create_index(connection, index_name,
                               schema, definition)
        error_string = str(e.value)
        assert "The following error occurred trying to create the index" in error_string
        assert "A generic error occurred" in error_string
        assert index_name in error_string
        assert schema in error_string
        assert definition in error_string

    def test_search_from_index(self):
        expected_search_result = "test_search_result"

        mocked_index = Mock()
        mocked_index.search.return_value = expected_search_result

        mocked_connection = Mock()
        mocked_connection.ft.return_value = mocked_index

        index_name = "test_index"

        search_result = utils.search_from_index(
            mocked_connection, index_name)

        assert search_result == expected_search_result
        mocked_connection.ft.assert_called_with(index_name)

    def test_search_from_index_exception(self):
        with pytest.raises(utils.DatabaseIndexSearchError) as e:
            index_name = "test_index"
            query_string = "@test_column:test_value"

            mocked_index = Mock()
            mocked_index.search.side_effect = ValueError(
                "A generic error occurred")

            mocked_connection = Mock()
            mocked_connection.ft.return_value = mocked_index

            utils.search_from_index(
                mocked_connection, index_name, query_string)
        error_string = str(e.value)
        assert "The following error occurred trying to search the index" in error_string
        assert "A generic error occurred" in error_string
        assert index_name in error_string
        assert query_string in error_string
        mocked_connection.ft.assert_called_once_with(index_name)

    @patch('mqtt_middlware_utils.db_utils.persist_new_object', autospec=True)
    @patch('mqtt_middlware_utils.db_utils.retrieve_object', autospec=True)
    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_update_object(self, mocked_get_new_connection, mocked_retrieve_object, mocked_persist_new_object):
        mocked_connection = Mock()
        mocked_get_new_connection.return_value = mocked_connection

        # should be not null
        mocked_retrieve_object.return_value = "test_object"

        object_to_persist = {"name": "John", "age": 30}
        object_name = "test_object"

        mocked_persist_new_object.return_value = object_to_persist

        # get a new connection
        connection = utils.get_new_connection(
            host="localhost", username="test", password="test")

        updated_object = utils.update_object(
            connection, object_name, object_to_persist)

        assert updated_object == object_to_persist
        mocked_retrieve_object.assert_called_once_with(connection, object_name)
        mocked_persist_new_object.assert_called_once_with(
            connection, object_name, object_to_persist)

    @patch('mqtt_middlware_utils.db_utils.persist_new_object', autospec=True)
    @patch('mqtt_middlware_utils.db_utils.retrieve_object', autospec=True)
    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_update_object_object_not_found(self, mocked_get_new_connection, mocked_retrieve_object, mocked_persist_new_object):
        with pytest.raises(utils.DatabaseObjectNotFoundError) as e:
            mocked_connection = Mock()
            mocked_get_new_connection.return_value = mocked_connection

            # should be null
            mocked_retrieve_object.return_value = None

            object_to_persist = {"name": "John", "age": 30}
            object_name = "test_object"

            mocked_persist_new_object.return_value = object_to_persist

            # get a new connection
            connection = utils.get_new_connection(
                host="localhost", username="test", password="test")

            utils.update_object(
                connection, object_name, object_to_persist)

        assert "No object to update can be found with name " + str(object_name)
        mocked_retrieve_object.assert_called_once_with(
            connection, object_name)
        mocked_persist_new_object.assert_not_called()

    @patch('mqtt_middlware_utils.db_utils.persist_new_object', autospec=True)
    @patch('mqtt_middlware_utils.db_utils.retrieve_object', autospec=True)
    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_update_object_exception(self, mocked_get_new_connection, mocked_retrieve_object, mocked_persist_new_object):
        with pytest.raises(utils.DatabaseUpdateError) as e:
            mocked_connection = Mock()
            mocked_get_new_connection.return_value = mocked_connection

            # should be not null
            mocked_retrieve_object.return_value = "Test_object"

            object_to_update = {"name": "John", "age": 30}
            object_name = "test_object"

            mocked_persist_new_object.side_effect = ValueError(
                "A generic error occurred")

            # get a new connection
            connection = utils.get_new_connection(
                host="localhost", username="test", password="test")

            utils.update_object(
                connection, object_name, object_to_update)
        error_string = str(e.value)
        assert "The following error occurred trying to update the object" in error_string
        assert object_name in error_string
        assert str(object_to_update) in error_string
        mocked_retrieve_object.assert_called_once_with(connection, object_name)
        mocked_persist_new_object.assert_called_once_with(
            connection, object_name, object_to_update)

    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_delete_object(self, mocked_get_new_connection):
        mocked_connection = Mock()
        mocked_connection.json().delete.return_value = 1

        mocked_get_new_connection.return_value = mocked_connection

        # get a new connection
        connection = utils.get_new_connection(
            host="localhost", username="test", password="test")

        object_name = "test_object"

        deleted_objects = utils.delete_object(connection, object_name)

        assert deleted_objects == 1
        mocked_connection.json().delete.assert_called_once_with(object_name)

    @patch('mqtt_middlware_utils.db_utils.get_new_connection', autospec=True)
    def test_delete_object_exception(self, mocked_get_new_connection):
        with pytest.raises(utils.DatabaseDeleteError) as e:
            mocked_connection = Mock()
            mocked_connection.json().delete.side_effect = ValueError("A generic error occurred")

            mocked_get_new_connection.return_value = mocked_connection

            # get a new connection
            connection = utils.get_new_connection(
                host="localhost", username="test", password="test")

            object_name = "test_object"

            utils.delete_object(connection, object_name)

        error_string = str(e.value)
        assert "The following error occurred trying to delete the object" in error_string
        assert object_name in error_string
        mocked_connection.json().delete.assert_called_once_with(object_name)

    @patch('tests.test_db_utils.simple_function_for_decorator_testing', autospec=True)
    def test_function_wrapper_generic_exception(self, mocked_test_function):
        with pytest.raises(utils.DatabaseError) as e:
            mocked_test_function.side_effect = ValueError(
                "A generic error occurred")
            decorated_function = utils.db_exceptions_decorator(
                mocked_test_function)
            decorated_function()
        error_string = str(e.value)
        assert "The following error occurred while operating on the database" in error_string
        assert "A generic error occurred" in error_string
        mocked_test_function.assert_called_once()

    @patch('tests.test_db_utils.simple_function_for_decorator_testing', autospec=True)
    def test_function_wrapper_object_not_found_exception(self, mocked_test_function):
        with pytest.raises(utils.DatabaseObjectNotFoundError) as e:
            mocked_test_function.side_effect = utils.DatabaseObjectNotFoundError(
                "Can't find the object")
            decorated_function = utils.db_exceptions_decorator(
                mocked_test_function)
            decorated_function()
        error_string = str(e.value)
        assert "Can't find the object" in error_string
        mocked_test_function.assert_called_once()

    @patch('tests.test_db_utils.simple_function_for_decorator_testing', autospec=True)
    def test_function_wrapper_connection_exception(self, mocked_test_function):
        with pytest.raises(utils.DatabaseConnectionError) as e:
            mocked_test_function.side_effect = utils.DatabaseConnectionError(
                "An error occurred while connecting to the database")
            decorated_function = utils.db_exceptions_decorator(
                mocked_test_function)
            decorated_function()
        error_string = str(e.value)
        assert "An error occurred while connecting to the database" in error_string
        mocked_test_function.assert_called_once()

    @patch('tests.test_db_utils.simple_function_for_decorator_testing', autospec=True)
    def test_function_wrapper_persistence_exception(self, mocked_test_function):
        with pytest.raises(utils.DatabasePersistenceError) as e:
            mocked_test_function.side_effect = utils.DatabasePersistenceError(
                "An error occurred while persisting an object")
            decorated_function = utils.db_exceptions_decorator(
                mocked_test_function)
            decorated_function()
        error_string = str(e.value)
        assert "An error occurred while persisting an object" in error_string
        mocked_test_function.assert_called_once()

    @patch('tests.test_db_utils.simple_function_for_decorator_testing', autospec=True)
    def test_function_wrapper_update_exception(self, mocked_test_function):
        with pytest.raises(utils.DatabaseUpdateError) as e:
            mocked_test_function.side_effect = utils.DatabaseUpdateError(
                "An error occurred while updating an object")
            decorated_function = utils.db_exceptions_decorator(
                mocked_test_function)
            decorated_function()
        error_string = str(e.value)
        assert "An error occurred while updating an object" in error_string
        mocked_test_function.assert_called_once()

    @patch('tests.test_db_utils.simple_function_for_decorator_testing', autospec=True)
    def test_function_wrapper_delete_exception(self, mocked_test_function):
        with pytest.raises(utils.DatabaseDeleteError) as e:
            mocked_test_function.side_effect = utils.DatabaseDeleteError(
                "An error occurred while deleting an object")
            decorated_function = utils.db_exceptions_decorator(
                mocked_test_function)
            decorated_function()
        error_string = str(e.value)
        assert "An error occurred while deleting an object" in error_string
        mocked_test_function.assert_called_once()

    @patch('tests.test_db_utils.simple_function_for_decorator_testing', autospec=True)
    def test_function_wrapper_create_index_exception(self, mocked_test_function):
        with pytest.raises(utils.DatabaseCreateIndexError) as e:
            mocked_test_function.side_effect = utils.DatabaseCreateIndexError(
                "An error occurred while creating an index")
            decorated_function = utils.db_exceptions_decorator(
                mocked_test_function)
            decorated_function()
        error_string = str(e.value)
        assert "An error occurred while creating an index" in error_string
        mocked_test_function.assert_called_once()

    @patch('tests.test_db_utils.simple_function_for_decorator_testing', autospec=True)
    def test_function_wrapper_object_retrieve_exception(self, mocked_test_function):
        with pytest.raises(utils.DatabaseObjectRetrieveError) as e:
            mocked_test_function.side_effect = utils.DatabaseObjectRetrieveError(
                "An error occurred while retrieving an object")
            decorated_function = utils.db_exceptions_decorator(
                mocked_test_function)
            decorated_function()
        error_string = str(e.value)
        assert "An error occurred while retrieving an object" in error_string
        mocked_test_function.assert_called_once()

    @patch('tests.test_db_utils.simple_function_for_decorator_testing', autospec=True)
    def test_function_wrapper_index_search_exception(self, mocked_test_function):
        with pytest.raises(utils.DatabaseIndexSearchError) as e:
            mocked_test_function.side_effect = utils.DatabaseIndexSearchError(
                "An error occurred while searching an index")
            decorated_function = utils.db_exceptions_decorator(
                mocked_test_function)
            decorated_function()
        error_string = str(e.value)
        assert "An error occurred while searching an index" in error_string
        mocked_test_function.assert_called_once()
