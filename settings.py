from cat.mad_hatter.decorators import plugin
from pydantic import BaseModel, Field
from enum import Enum
from cat.log import log

connections = {
    "PostgreSQL" : "postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}",
    "MySQL": "mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}",
    "Oracle": "oracle://{username}:{password}@{host}:{port}/{database}",
    "Microsoft SQL Server": "mssql+pymssql://scott:{host}@{host}:{port}/{database}",
    "Microsoft SQL Server ODBC": "mssql+pyodbc://{username}:{password}@{database}",
    "SQLite": "sqlite:///{host}"
}

#DatabaseType = Enum("DatabaseType", list(connections.keys()))
DatabaseType = Enum("DatabaseType", [(str(hash(key)), key) for key, value in connections.items()])


'''# Create dynamic enum
class DatabaseType(Enum):
    pass
for index, (key, value) in enumerate(connections.items()):
    setattr(DatabaseType, chr(ord('a') + index), value)'''


class MySettings(BaseModel):
    database_type: DatabaseType
    host: str = Field(
        title="host",
        default=""
    )
    port: int = Field(
        title="port",
        default=""
    )
    username: str = Field(
        title="username",
        default=""
    )
    password: str = Field(
        title="password",
        default=""
    )
    database: str = Field(
        title="database",
        default=""
    )


@plugin
def settings_schema():
    return MySettings.schema()
