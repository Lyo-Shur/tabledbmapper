from tabledbmapper.engine import Engine
from tabledbmapper.manager.manager import Manager
from tabledbmapper.manager.mvc.dao import DAO
from tabledbmapper.manager.mvc.service import Service
from tabledbmapper.manager.xml_config import parse_config_from_string, parse_config_from_file


class SQLSession:

    # session pool
    _session_pool = None

    # use index
    _index = -1

    # sql engine
    _engine = None

    def __init__(self, session_pool, index: int, engine: Engine):
        """
        Init SQLSession
        :param engine: sql engine
        """
        self._session_pool = session_pool
        self._index = index
        self._engine = engine

    def close(self):
        """
        Close the session
        """
        self._session_pool.give_back_session(self._index)

    def service(self, config: dict):
        """
        Assemble upward as a service
        :param config XmlConfig
        :return: service
        """
        return Service(self.dao(config))

    def service_by_string(self, config_string: str):
        """
        Assemble upward as a service
        :param config_string xml string
        :return: service
        """
        return Service(self.dao_by_string(config_string))

    def service_by_file(self, config_file: str):
        """
        Assemble upward as a service
        :param config_file xml file
        :return: service
        """
        return Service(self.dao_by_file(config_file))

    def dao(self, config: dict):
        """
        Assemble upward as a dao
        :param config XmlConfig
        :return: dao
        """
        return DAO(self.manager(config))

    def dao_by_string(self, config_string: str):
        """
        Assemble upward as a dao
        :param config_string xml string
        :return: dao
        """
        return DAO(self.manager_by_string(config_string))

    def dao_by_file(self, config_file: str):
        """
        Assemble upward as a dao
        :param config_file xml file
        :return: dao
        """
        return DAO(self.manager_by_file(config_file))

    def manager(self, config: dict):
        """
        Assemble upward as a manager
        :param config XmlConfig
        :return: manager
        """
        return Manager(self.engine(), config)

    def manager_by_string(self, config_string: str):
        """
        Assemble upward as a manager
        :param config_string xml string
        :return: manager
        """
        config = parse_config_from_string(config_string)
        return Manager(self.engine(), config)

    def manager_by_file(self, config_file: str):
        """
        Assemble upward as a manager
        :param config_file xml file
        :return: manager
        """
        config = parse_config_from_file(config_file)
        return Manager(self.engine(), config)

    def engine(self):
        """
        Assemble upward as a template engine
        :return: TemplateEngine
        """
        return self._engine.up_to_template_engine()
