from tabledbmapper.manager.session.pool import SessionInit, SessionPool


class SQLSessionFactoryBuild:

    # SessionInit
    _session_init = None

    def __init__(self, session_init: SessionInit):
        """
        Init session pool
        :param session_init: SessionInit
        """
        # save session init model
        self._session_init = session_init

    def set_lazy_loading(self, lazy: bool):
        """
        Set thread pool lazy loading
        :param lazy: bool
        :return: SQLSessionFactoryBuild
        """
        self._session_init.lazy_init = lazy
        return self

    def set_max_conn_number(self, number):
        """
        Sets the maximum number of connections to the thread pool
        :param number: max number
        :return: SQLSessionFactoryBuild
        """
        self._session_init.max_conn_number = number
        return self

    def build(self):
        return SQLSessionFactory(self._session_init)


class SQLSessionFactory:

    # Database connection pool
    _session_pool = None

    def __init__(self, session_init: SessionInit):
        """
        Init session pool
        :param session_init: SessionInit
        """
        self._session_pool = SessionPool(session_init)

    def open_session(self, auto_commit=True):
        """
        Open a session
        :param auto_commit: auto_commit
        :return: SQL Session
        """
        return self._session_pool.get_session(auto_commit)
