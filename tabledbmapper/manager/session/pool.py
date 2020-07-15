from threading import Lock


from tabledbmapper.engine import Engine
from tabledbmapper.manager.session.sql_session import SQLSession


# Session Pool Init Config
class SessionInit:

    # conn
    _conn = None

    # Lazy loading
    lazy_init = True

    # Maximum number of connections
    max_conn_number = 10

    def init_engine(self):
        """
        Gets the database connection method
        """
        return Engine(self._conn)

    def test_engine(self, engine: Engine):
        """
        Test whether the connection is available, and reconnect
        :param engine: database sql engine
        """
        pass


_lock = Lock()


class SessionPool:

    # Current number of connections
    _number = 0

    # conn engines
    _engines = None

    # use flag
    _flags = None

    # SessionInit
    _sessionInit = None

    def __init__(self, session_init: SessionInit):
        """
        Init session pool
        :param session_init: SessionInit
        """
        # save session init model
        self._sessionInit = session_init
        # db conn
        self._engines = []
        # used conn
        self._flags = []
        # lazy loading
        if not session_init.lazy_init:
            self._number = session_init.max_conn_number
            for i in range(self._number):
                self._engines.append(session_init.init_engine())
                self._flags.append(i)

    def get_session(self, auto_commit=True):
        """
        Get SQL Session from Session Pool
        :param auto_commit: auto_commit
        :return: SQL Session
        """
        _lock.acquire()
        while True:
            length = len(self._flags)
            # When connections are exhausted and 
            # the maximum number of connections is not exceeded
            if length == 0 and len(self._engines) < self._number:
                # init new engine
                engine = self._sessionInit.init_engine()
                engine.set_auto_commit(auto_commit)
                self._engines.append(engine)
                print("create")
                _lock.release()
                return SQLSession(self, len(self._engines), engine)
            if length > 0:
                index = self._flags[0]
                # get engine
                engine = self._engines[index]
                engine.set_auto_commit(auto_commit)
                # test engine
                self._sessionInit.test_engine(engine)
                # set use flag
                self._flags = self._flags[1:]
                print("have")
                _lock.release()
                return SQLSession(self, index, engine)

    def give_back_session(self, index):
        """
        Return the session to the session pool
        :param index: The index of the session in the Session pool
        """
        print(index)
        self._flags.append(index)
