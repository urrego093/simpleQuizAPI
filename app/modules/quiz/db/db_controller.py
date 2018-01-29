from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import consult,update,delete, insert

_instances = {}


class Singleton(type):

    def __init__(cls,name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        else:
            cls._instances[cls].__init__(*args, **kwargs)

        return cls.instance


class DbController(object):
    __metaclass__ = Singleton

    def __init__(self):

        self.__engine = create_engine('sqlite:///:memory:', echo=False)  # set to false to disable generated sql printing
        self.__Session = sessionmaker(bind=self.__engine)
        self.__session = self.__Session()

        self.consult = consult.Consult(self.__session)
        self.insert = insert.Insert(self.__session)
        self.update = update.Update(self.__session)

    def create_tables(self, base):
        try:
            base.metadata.create_all(self.__engine)
        except RuntimeError:
            print ("It was impossible to create all tables")

    def commit(self):
        self.__session.commit()
