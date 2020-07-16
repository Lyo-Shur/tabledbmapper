from typing import Callable

from tabledbmapper.manager.session.sql_session import SQLSession

from tabledbmapper.logger import DefaultLogger, Logger

from tabledbmapper.engine import ConnHandle, ExecuteEngine
from tabledbmapper.manager.session.pool import SessionPool


class SQLSessionFactory:

    # Database connection pool
    _session_pool = None

    _logger = None

    def __init__(self, conn_handle: ConnHandle, execute_engine: ExecuteEngine,
                 lazy_init=True, max_conn_number=10, logger=DefaultLogger()):
        """
        Init session pool
        :param conn_handle: ConnHandle
        :param execute_engine: ExecuteEngine
        :param lazy_init: lazy_init
        :param max_conn_number: max_conn_number
        :param logger: Logger
        """
        self._session_pool = SessionPool(conn_handle, execute_engine, lazy_init, max_conn_number)
        self._logger = logger

    def open_simple_session(self, handle: Callable[[SQLSession], None]) -> bool:
        """
        Open a session
        :param handle: session operation
        :return: SQL Session
        """
        def _error_handle(e: BaseException):
            self._logger.print_error(e)
        return self.open_session(handle, _error_handle)

    def open_session(self, handle: Callable[[SQLSession], None], error_handle: Callable[[BaseException], None]) -> bool:
        """
        Open a session
        :param handle: session operation
        :param error_handle: error handle
        :return: SQL Session
        """
        with self._session_pool.get_session(False) as session:
            try:
                handle(session)
                session.commit()
                return True
            except Exception as e:
                session.rollback()
                error_handle(e)
        return False


class SQLSessionFactoryBuild:

    _conn_handle = None
    _execute_engine = None

    _lazy_init = True
    _max_conn_number = 10

    _logger = None

    def __init__(self, conn_handle: ConnHandle, execute_engine: ExecuteEngine):
        """
        Init session pool
        :param conn_handle: ConnHandle
        :param execute_engine: ExecuteEngine
        """
        self._conn_handle = conn_handle
        self._execute_engine = execute_engine

        self._logger = DefaultLogger()

    def set_logger(self, logger: Logger):
        """
        Set Logger
        :param logger: log printing
        :return self
        """
        self._logger = logger
        return self

    def set_lazy_loading(self, lazy: bool):
        """
        Set thread pool lazy loading
        :param lazy: bool
        :return: SQLSessionFactoryBuild
        """
        self._lazy_init = lazy
        return self

    def set_max_conn_number(self, number):
        """
        Sets the maximum number of connections to the thread pool
        :param number: max number
        :return: SQLSessionFactoryBuild
        """
        self._max_conn_number = number
        return self

    def build(self) -> SQLSessionFactory:
        return SQLSessionFactory(self._conn_handle, self._execute_engine, self._lazy_init, self._max_conn_number)
