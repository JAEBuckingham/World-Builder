"""sql connections"""
from tkinter import filedialog

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tables.base import Base


def connection_string(db_type, database, host='localhost', port=None, username=None, password=None):
    """creates the connection string"""
    if db_type == 'mysql':
        if port:
            return f"mysql://{username}:{password}@{host}:port/{database}"
        else:
            return f"mysql://{username}:{password}@{host}/{database}"

    if db_type == 'sqlite':
        return f'sqlite:///{database}'


class Connection:
    """connects to the sql database"""

    def __init__(self, db_type, database, host='localhost', port=None, username=None,
                 password=None):
        self.connection_string = connection_string(db_type, database, host, port, username,
                                                   password)
        self.engine = create_engine(self.connection_string, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def new_session(self):
        """returns a new session"""
        return self.Session()


class DataBase:
    def __init__(self):
        self.connection = None
        self.session = None

    def new_sqlite_connection(self):
        """get the file path for a new sql db"""
        filename = filedialog.asksaveasfilename(title="New",
                                                filetypes=(("Database files", "*.db"),))
        if filename:
            if '.db' != filename[-3:]:
                filename += '.db'
            self.connection = Connection('sqlite', filename)
            self.session = self.connection.new_session()

    def open_sqlite_connection(self):
        """get the file path for a sql db"""
        filename = filedialog.askopenfilename(title="Open", filetypes=(("Database files", "*.db"),))
        if filename:
            self.connection = Connection('sqlite', filename)
            self.session = self.connection.new_session()

    def commit(self):
        if self.session:
            self.session.commit()


def character_list(table, session):
    for instance in session.query(table.name).order_by(table.name):
        yield instance.name


def add_item(session, rows):
    session.add_all(rows)


if __name__ == '__main__':
    DataBase().open_sqlite_connection()
