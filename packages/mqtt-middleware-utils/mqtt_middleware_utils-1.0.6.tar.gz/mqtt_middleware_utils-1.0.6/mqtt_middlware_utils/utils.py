import uuid
import configparser
import json

from fabric import Connection
from mqtt_middlware_utils.exceptions.mqtt_middleware_exceptions import MiddlewareConfigurationException, UuidGenerationError, SshRemoteError, SshCommandExecutionError


def generate_uuid():
    try:
        # generate uuid using random uuid generator
        new_instance_id = uuid.uuid4()
        return str(new_instance_id)
    except Exception as e:
        raise UuidGenerationError(
            "The following error occurred while generating a new UUID\n"+str(e))


def execute_ssh_command(conn, command) -> str:
    try:
        result = conn.run(command)
        if (result.ok):
            return result.stdout.strip()
        else:
            raise SshCommandExecutionError(
                "The following error occurred with the remote execution of the command ["+command+"]" + result.sterr.strip())
    except SshCommandExecutionError:
        raise
    except Exception as e:
        raise SshCommandExecutionError(
            "The following error occurred with the remote execution of the command ["+command+"]\n"+str(e))


def init_remote_ssh_connection(host, user, connection_kwargs):
    try:
        # TODO USE A SSH KEY INSTEAD! THIS IS NOT SAFE FOR PRODUCTION
        return Connection(host, user, connect_kwargs=connection_kwargs)
    except Exception as e:
        raise SshRemoteError(
            "The following error occurred while establishing a remote ssh connection with the host ["+host+"]\n"+str(e))


class middlware_instance:

    def __init__(self, instance_id, customer_id, tenant_id, name, status="offline", type="MQTT") -> None:
        self.instance_id = instance_id
        self.customer_id = customer_id
        self.tenant_id = tenant_id
        self.name = name
        self.status = status
        self.type = type


class mqtt_middleware_configuration:

    def __init__(self, instance_id="", sub_host="", sub_port=0, sub_topic="", source_client_id="", source_auth={}, pub_host="",
                 pub_port=0, pub_topic="", devices_auth_list={}, logger_name="", logger_level="", logger_dest="", *, dictionary={}) -> None:

        try:
            if not dictionary:
                self.mid_instance_id = instance_id
                self.sub_host = sub_host
                self.sub_port = sub_port
                self.sub_topic = sub_topic
                self.source_client_id = source_client_id
                self.source_auth = source_auth
                self.pub_host = pub_host
                self.pub_port = pub_port
                self.pub_topic = pub_topic
                self.devices_auth_list = devices_auth_list
                self.logger_name = logger_name
                self.logger_level = logger_level
                self.logger_dest = logger_dest
            else:
                self.__from_dictionary(dictionary)

            self.__checkValidConfiguration()
        except Exception as e:
            raise MiddlewareConfigurationException(
                "The following error occurred while creating mqtt_middleware_configuration: "
                + "\n"+str(e))

    def __from_dictionary(self, dictionary):
        "Create class from Python dictionary"
        self.mid_instance_id = dictionary["mid_instance_id"]
        self.sub_host = dictionary["sub_host"]
        self.sub_port = dictionary["sub_port"]
        self.sub_topic = dictionary["sub_topic"]
        self.source_client_id = dictionary["source_client_id"]
        self.source_auth = dictionary["source_auth"]
        self.pub_host = dictionary["pub_host"]
        self.pub_port = dictionary["pub_port"]
        self.pub_topic = dictionary["pub_topic"]
        self.devices_auth_list = dictionary["devices_auth_list"]
        self.logger_name = dictionary["logger_name"]
        self.logger_level = dictionary["logger_level"]
        self.logger_dest = dictionary["logger_dest"]

    def __checkValidConfiguration(self):
        def RaiseConfigurationException(config_line):
            raise MiddlewareConfigurationException("Invalid configuration provided" +
                                                   str(config_line)+" not set. Please check configuration")

        if not self.mid_instance_id:
            RaiseConfigurationException("Middleware Instance ID")
        if not self.sub_host:
            RaiseConfigurationException("Subscriber Host")
        if not self.sub_port:
            RaiseConfigurationException("Subscriber Port")
        if not self.sub_topic:
            RaiseConfigurationException("Subscriber Topic")
        if not self.source_client_id:
            RaiseConfigurationException("Subscriber Client_ID")
        if not self.source_auth:
            RaiseConfigurationException("Subscriber Auth Params")
        if not self.pub_host:
            RaiseConfigurationException("Publisher Host")
        if not self.pub_port:
            RaiseConfigurationException("Publisher Port")
        if not self.pub_topic:
            RaiseConfigurationException("Publisher Topic")
        if not self.devices_auth_list:
            RaiseConfigurationException("Publisher Auth Params")

    def debugPrintConfiguration(self):
        print("Issued Configuration")
        print("Logger level: " + self.logger_level)
        print("Logger name: "+self.logger_name)
        print("Logger destination: "+self.logger_dest)
        print("Subscriber Host: " + self.sub_host)
        print("Subscriber Port: " + str(self.sub_port))
        print("Subscriber Topic: " + self.sub_topic)
        print("Subscriber Client_ID: " + self.source_client_id)
        print("Subscriber Auth Params: " + str(self.source_auth))
        print("Publisher Host: "+self.pub_host)
        print("Publisher Port: "+str(self.pub_port))
        print("Publisher Topic: "+self.pub_topic)
        print("Publisher Auth Params: "+str(self.devices_auth_list))


def read_configuration(instance_id, config_file):
    conf_parser = configparser.ConfigParser()
    if not config_file:
        raise MiddlewareConfigurationException("Configuration file not issued")

    try:
        # read configuration file
        conf_parser.read(config_file)

        # get params from config file
        server_sub_config = conf_parser['SERVER.SUB']
        sub_host = server_sub_config["hostname"].strip()
        sub_port = server_sub_config.getint("port")
        sub_topic = server_sub_config["topic"].strip()
        source_client_id = server_sub_config["clientid"].strip()
        source_auth = json.loads(server_sub_config["auth"])

        server_pub_config = conf_parser["SERVER.PUB"]
        pub_host = server_pub_config["hostname"].strip()
        pub_port = server_pub_config.getint("port")
        pub_topic = server_pub_config["topic"].strip()
        devices_auth_list = json.loads(server_pub_config["auth"])

        server_sys_config = conf_parser["SYSTEM"]
        logger_name = server_sys_config["logname"]
        logger_level = server_sys_config["loglevel"]
        logger_dest = server_sys_config["logdestination"]

        return mqtt_middleware_configuration(instance_id, sub_host, sub_port, sub_topic, source_client_id,
                                             source_auth, pub_host, pub_port, pub_topic, devices_auth_list,
                                             logger_name, logger_level, logger_dest)
    except MiddlewareConfigurationException as e:
        raise
    except Exception as e:
        raise MiddlewareConfigurationException(
            "The following error occurred while reading configuration from file. Please check the provided configuration keys\n"+str(e))
