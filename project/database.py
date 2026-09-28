import sqlmodel

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = sqlmodel.create_engine(sqlite_url)


def create_db_and_tables():
    sqlmodel.SQLModel.metadata.create_all(engine)