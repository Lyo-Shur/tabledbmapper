from tabledbmapper.logger import DefaultLogger, Logger
from tabledbmapper.sql_builder import builder


class Engine:
    """
    SQL Execution Engine
    """

    # Database connection
    conn = None
    _auto_commit_function = None

    # Logger
    _logger = None

    def __init__(self, conn, auto_commit=True):
        """
        Init SQL Execution Engine
        :param conn: database conn
        :param auto_commit: auto_commit
        """
        self.conn = conn
        self.set_auto_commit(auto_commit)
        self._logger = DefaultLogger()

    def set_logger(self, logger: Logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._logger = logger
        return self

    def query(self, sql: str, parameter):
        """
        Query list information
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        pass

    def count(self, sql: str, parameter):
        """
        Query quantity information
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Query results
        """
        pass

    def exec(self, sql: str, parameter):
        """
        Execute SQL statement
        :param sql: SQL statement to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        pass

    def set_auto_commit(self, auto_commit: bool):
        """
        Set the auto commit method
        :param auto_commit: bool
        """
        if auto_commit:
            def commit():
                self.commit()
            self._auto_commit_function = commit
        else:
            def without_commit():
                pass
            self._auto_commit_function = without_commit

    def commit(self):
        """
        Submit query modification
        """
        pass

    def up_to_template_engine(self):
        """
        Assemble upward as a template engine
        :return: TemplateEngine
        """
        return TemplateEngine(self)


class TemplateEngine:
    """
    SQL template execution engine
    Using the jinja2 template engine
    """

    # SQL Execution Engine
    _engine = None

    def __init__(self, engine: Engine):
        """
        Init SQL Execution Engine
        :param engine: SQL Execution Engine
        """
        self._engine = engine

    def set_logger(self, logger: Logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._engine.set_logger(logger)
        return self

    def query(self, sql_template: str, parameter):
        """
        Query list information
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        sql, param = builder(sql_template, parameter)
        return self._engine.query(sql, param)

    def count(self, sql_template: str, parameter):
        """
        Query quantity information
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Query results
        """
        sql, param = builder(sql_template, parameter)
        return self._engine.count(sql, param)

    def exec(self, sql_template: str, parameter):
        """
        Execute SQL statement
        :param sql_template: SQL template to be executed
        :param parameter: parameter
        :return: Last inserted ID, affecting number of rows
        """
        sql, param = builder(sql_template, parameter)
        return self._engine.exec(sql, param)

    def commit(self):
        """
        Submit query modification
        """
        self._engine.commit()
