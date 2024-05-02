import pytest

from mqtt_middlware_utils import utils
from unittest.mock import patch, Mock


class TestUtilsModule:

    def test_generate_uuid(self):
        uuid = utils.generate_uuid()
        assert (len(uuid) == 36)

    def test_generate_uuid_string_type(self):
        uuid = utils.generate_uuid()
        assert (isinstance(uuid, str))

    @patch('mqtt_middlware_utils.utils.uuid.uuid4')
    def test_generate_uuid_exception_raise(self, mocked_uuid4):
        with pytest.raises(utils.UuidGenerationError) as e:
            mocked_uuid4.side_effect = ValueError('A generic error occurred')
            utils.generate_uuid()
        error_string = str(e.value)
        assert "The following error occurred while generating a new UUID" in error_string
        assert "A generic error occurred" in error_string
        mocked_uuid4.assert_called_once()

    @patch('mqtt_middlware_utils.utils.init_remote_ssh_connection')
    def test_execute_ssh_command(self, mocked_init_remote_ssh_connection):
        cmd = "echo test"
        cmd_stdout = "test"

        mocked_result = Mock(ok=True, stdout=cmd_stdout)
        mocked_connection = Mock()
        mocked_connection.run.return_value = mocked_result

        mocked_init_remote_ssh_connection.return_value = mocked_connection

        # first get connection
        ssh_connection = utils.init_remote_ssh_connection(
            "test_host", "user", connection_kwargs={"password": "password"})

        cmd_result = utils.execute_ssh_command(ssh_connection, cmd)

        assert cmd_result == cmd_stdout
        mocked_connection.run.assert_called_once_with(cmd)

    @patch('mqtt_middlware_utils.utils.init_remote_ssh_connection')
    def test_execute_ssh_command_result_not_ok(self, mocked_init_remote_ssh_connection):
        with pytest.raises(utils.SshCommandExecutionError) as e:
            cmd = "echo test"
            cmd_stdout = "test"

            mocked_result = Mock(ok=False, stdout=cmd_stdout)
            mocked_connection = Mock()
            mocked_connection.run.return_value = mocked_result

            mocked_init_remote_ssh_connection.return_value = mocked_connection

            # first get connection
            ssh_connection = utils.init_remote_ssh_connection(
                "test_host", "user", connection_kwargs={"password": "password"})

            utils.execute_ssh_command(ssh_connection, cmd)

        error_string = str(e.value)
        assert "The following error occurred with the remote execution of the command" in error_string
        assert cmd in error_string
        mocked_connection.run.assert_called_once_with(cmd)

    @patch('mqtt_middlware_utils.utils.init_remote_ssh_connection')
    def test_execute_ssh_command_exception_raise(self, mocked_init_remote_ssh_connection):
        with pytest.raises(utils.SshCommandExecutionError) as e:
            cmd = "echo test"

            mocked_connection = Mock()
            mocked_connection.run.side_effect = ValueError(
                'A generic error occurred')

            mocked_init_remote_ssh_connection.return_value = mocked_connection

            # first get connection
            ssh_connection = utils.init_remote_ssh_connection(
                "test_host", "user", connection_kwargs={"password": "password"})

            utils.execute_ssh_command(ssh_connection, cmd)

        error_string = str(e.value)
        assert "The following error occurred with the remote execution of the command" in error_string
        assert "A generic error occurred" in error_string
        assert cmd in error_string
        mocked_connection.run.assert_called_once_with(cmd)

    @patch('mqtt_middlware_utils.utils.Connection', autospec=True)
    def test_init_remote_ssh_connection(self, mocked_connection):
        connect_return = Mock()
        connect_return.is_connected.return_value = True
        mocked_connection.return_value = connect_return

        host = "test_host"
        user = "test_user"
        connection_kwargs = {"password": "test_password"}

        conn = utils.init_remote_ssh_connection(
            host, user, connection_kwargs=connection_kwargs)

        assert conn.is_connected() == True
        mocked_connection.assert_called_once_with(
            host, user, connect_kwargs=connection_kwargs)

    @patch('mqtt_middlware_utils.utils.Connection', autospec=True)
    def test_init_remote_ssh_connection_not_connected(self, mocked_connection):
        connect_return = Mock()
        connect_return.is_connected.return_value = False
        mocked_connection.return_value = connect_return

        host = "test_host"
        user = "test_user"
        connection_kwargs = {"password": "test_password"}

        conn = utils.init_remote_ssh_connection(
            host, user, connection_kwargs=connection_kwargs)

        assert conn.is_connected() == False
        mocked_connection.assert_called_once_with(
            host, user, connect_kwargs=connection_kwargs)

    @patch('mqtt_middlware_utils.utils.Connection', autospec=True, side_effect=ValueError("Error establishing connection"))
    def test_init_remote_ssh_connection_exception(self, mocked_connection):
        with pytest.raises(utils.SshRemoteError) as e:

            host = "test_host"
            user = "test_user"
            connection_kwargs = {"password": "test_password"}

            utils.init_remote_ssh_connection(
                host, user, connection_kwargs=connection_kwargs)

        error_string = str(e.value)
        assert "The following error occurred while establishing a remote ssh connection with the host" in error_string
        assert "Error establishing connection" in error_string
        assert host in error_string
        mocked_connection.assert_called_once_with(
            host, user, connect_kwargs=connection_kwargs)

    def test_middlware_instance_init(self):
        instance_id = "test-test1"
        customer_id = "0001"
        tenant_id = "0002"
        status = "offline"
        name = "test_instance"
        mid_instance = utils.middlware_instance(
            instance_id, customer_id, tenant_id, name, status)

        assert mid_instance.instance_id == "test-test1"
        assert mid_instance.customer_id == "0001"
        assert mid_instance.status == "offline"
        assert mid_instance.name == "test_instance"
        assert mid_instance.type == "MQTT"
        assert mid_instance.tenant_id == "0002"

    def test_mqtt_middleware_configuration_init(self):
        instance_id = "test-test1"
        sub_host = "host1"
        sub_port = 8080
        sub_topic = "test_topic"
        source_client_id = "TEST-CLIENT"
        source_auth = {"username": "user", "password": "user"}
        pub_host = "host2"
        pub_port = 8080
        pub_topic = "test_topic2"
        devices_auth_list = {
            "0": {
                "clientid": "test_id",
                "username": "user",
                "password": "user"
            },
            "1": {
                "clientid": "test_id",
                "username": "user",
                "password": "user"
            }}
        logger_name = "logger"
        logger_level = "DEBUG"
        logger_dest = "test/path/to/logs"

        mid_config = utils.mqtt_middleware_configuration(instance_id, sub_host, sub_port, sub_topic, source_client_id, source_auth, pub_host,
                                                         pub_port, pub_topic, devices_auth_list, logger_name, logger_level, logger_dest)

        assert mid_config.mid_instance_id == "test-test1"
        assert mid_config.sub_host == "host1"
        assert mid_config.sub_port == 8080
        assert mid_config.sub_topic == "test_topic"
        assert mid_config.source_client_id == "TEST-CLIENT"
        assert mid_config.source_auth["username"] == "user"
        assert mid_config.source_auth["password"] == "user"
        assert mid_config.pub_host == "host2"
        assert mid_config.pub_port == 8080
        assert mid_config.pub_topic == "test_topic2"
        assert mid_config.devices_auth_list["0"]["clientid"] == "test_id"
        assert mid_config.devices_auth_list["0"]["username"] == "user"
        assert mid_config.devices_auth_list["0"]["password"] == "user"
        assert mid_config.devices_auth_list["1"]["clientid"] == "test_id"
        assert mid_config.devices_auth_list["1"]["username"] == "user"
        assert mid_config.devices_auth_list["1"]["password"] == "user"
        assert mid_config.logger_name == "logger"
        assert mid_config.logger_level == "DEBUG"
        assert mid_config.logger_dest == "test/path/to/logs"

    def test_mqtt_middleware_configuration_dictionary_init(self):
        config_dict = {}
        config_dict["mid_instance_id"] = "test-test1"
        config_dict["sub_host"] = "host1"
        config_dict["sub_port"] = 8080
        config_dict["sub_topic"] = "test_topic"
        config_dict["source_client_id"] = "TEST-CLIENT"
        config_dict["source_auth"] = {"username": "user", "password": "user"}
        config_dict["pub_host"] = "host2"
        config_dict["pub_port"] = 8080
        config_dict["pub_topic"] = "test_topic2"
        config_dict["devices_auth_list"] = {
            "0": {
                "clientid": "test_id",
                "username": "user",
                "password": "user"
            },
            "1": {
                "clientid": "test_id",
                "username": "user",
                "password": "user"
            }}
        config_dict["logger_name"] = "logger"
        config_dict["logger_level"] = "DEBUG"
        config_dict["logger_dest"] = "test/path/to/logs"

        mid_config = utils.mqtt_middleware_configuration(
            dictionary=config_dict)

        assert mid_config.mid_instance_id == "test-test1"
        assert mid_config.sub_host == "host1"
        assert mid_config.sub_port == 8080
        assert mid_config.sub_topic == "test_topic"
        assert mid_config.source_client_id == "TEST-CLIENT"
        assert mid_config.source_auth["username"] == "user"
        assert mid_config.source_auth["password"] == "user"
        assert mid_config.pub_host == "host2"
        assert mid_config.pub_port == 8080
        assert mid_config.pub_topic == "test_topic2"
        assert mid_config.devices_auth_list["0"]["clientid"] == "test_id"
        assert mid_config.devices_auth_list["0"]["username"] == "user"
        assert mid_config.devices_auth_list["0"]["password"] == "user"
        assert mid_config.devices_auth_list["1"]["clientid"] == "test_id"
        assert mid_config.devices_auth_list["1"]["username"] == "user"
        assert mid_config.devices_auth_list["1"]["password"] == "user"
        assert mid_config.logger_name == "logger"
        assert mid_config.logger_level == "DEBUG"
        assert mid_config.logger_dest == "test/path/to/logs"

    def test_mqtt_middleware_configuration_dictionary_init_double_constructor(self):
        config_dict = {}
        config_dict["mid_instance_id"] = "test-test1"
        config_dict["sub_host"] = "host1"
        config_dict["sub_port"] = 8080
        config_dict["sub_topic"] = "test_topic"
        config_dict["source_client_id"] = "TEST-CLIENT"
        config_dict["source_auth"] = {"username": "user", "password": "user"}
        config_dict["pub_host"] = "host2"
        config_dict["pub_port"] = 8080
        config_dict["pub_topic"] = "test_topic2"
        config_dict["devices_auth_list"] = {
            "0": {
                "clientid": "test_id",
                "username": "user",
                "password": "user"
            },
            "1": {
                "clientid": "test_id",
                "username": "user",
                "password": "user"
            }}
        config_dict["logger_name"] = "logger"
        config_dict["logger_level"] = "DEBUG"
        config_dict["logger_dest"] = "test/path/to/logs"

        # these should be different from the final config
        instance_id = "test-test2"
        sub_host = "host2"
        sub_port = 8081
        sub_topic = "test_topic_2"
        source_client_id = "TEST-CLIENT-2"
        source_auth = {"username": "user2", "password": "user22"}
        pub_host = "host3"
        pub_port = 8082
        pub_topic = "test_topic3"
        devices_auth_list = {
            "0": {
                "clientid": "test_id_1",
                "username": "user",
                "password": "user"
            },
            "1": {
                "clientid": "test_id_2",
                "username": "user",
                "password": "user"
            }}
        logger_name = "logger_2"
        logger_level = "NOT_DEBUG"
        logger_dest = "test/path/to/logs_different"

        mid_config = utils.mqtt_middleware_configuration(instance_id, sub_host, sub_port, sub_topic, source_client_id, source_auth, pub_host,
                                                         pub_port, pub_topic, devices_auth_list, logger_name, logger_level, logger_dest, dictionary=config_dict)

        assert mid_config.mid_instance_id == "test-test1"
        assert mid_config.sub_host == "host1"
        assert mid_config.sub_port == 8080
        assert mid_config.sub_topic == "test_topic"
        assert mid_config.source_client_id == "TEST-CLIENT"
        assert mid_config.source_auth["username"] == "user"
        assert mid_config.source_auth["password"] == "user"
        assert mid_config.pub_host == "host2"
        assert mid_config.pub_port == 8080
        assert mid_config.pub_topic == "test_topic2"
        assert mid_config.devices_auth_list["0"]["clientid"] == "test_id"
        assert mid_config.devices_auth_list["0"]["username"] == "user"
        assert mid_config.devices_auth_list["0"]["password"] == "user"
        assert mid_config.devices_auth_list["1"]["clientid"] == "test_id"
        assert mid_config.devices_auth_list["1"]["username"] == "user"
        assert mid_config.devices_auth_list["1"]["password"] == "user"
        assert mid_config.logger_name == "logger"
        assert mid_config.logger_level == "DEBUG"
        assert mid_config.logger_dest == "test/path/to/logs"

    def test_mqtt_middleware_configuration_bad_config(self):
        with pytest.raises(utils.MiddlewareConfigurationException):
            sub_host = "host1"
            sub_port = 8080

            utils.mqtt_middleware_configuration(
                sub_host=sub_host, sub_port=sub_port)

    def test_mqtt_middleware_configuration_dictionary_bad_configuration(self):
        with pytest.raises(utils.MiddlewareConfigurationException):
            config_dict = {}
            config_dict["mid_instance_id"] = "test-test1"
            config_dict["sub_host"] = "host1"
            config_dict["sub_port"] = 8080

            utils.mqtt_middleware_configuration(
                dictionary=config_dict)

    def test_read_configuration(self):
        config_file = "tests/files/config.ini"
        mid_instance_id = "instance-test"
        mid_config = utils.read_configuration(mid_instance_id, config_file)

        assert mid_config.mid_instance_id == "instance-test"
        assert mid_config.sub_host == "host"
        assert mid_config.sub_port == 8080
        assert mid_config.sub_topic == "test_topic"
        assert mid_config.source_client_id == "CLIENT-TEST"
        assert mid_config.source_auth["username"] == "user"
        assert mid_config.source_auth["password"] == "user"
        assert mid_config.pub_host == "host_2"
        assert mid_config.pub_port == 8080
        assert mid_config.pub_topic == "test_topic"
        assert mid_config.devices_auth_list["0"]["clientid"] == "client-1"
        assert mid_config.devices_auth_list["0"]["username"] == "user"
        assert mid_config.devices_auth_list["0"]["password"] == "user"
        assert mid_config.devices_auth_list["1"]["clientid"] == "client-2"
        assert mid_config.devices_auth_list["1"]["username"] == "user"
        assert mid_config.devices_auth_list["1"]["password"] == "user"
        assert mid_config.logger_name == "mqtt_integration"
        assert mid_config.logger_level == "DEBUG"
        assert mid_config.logger_dest == "/var/log/test/test.log"

    def test_read_configuration_exception_raise(self):
        with pytest.raises(utils.MiddlewareConfigurationException):
            config_file = "tests/files/wrong_config.ini"
            mid_instance_id = "instance-test"
            utils.read_configuration(mid_instance_id, config_file)
