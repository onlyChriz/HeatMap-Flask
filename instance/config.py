
from db_connection import db_connection
from db_con import db_con


database = db_connection(db_con())
SQLALCHEMY_DATABASE_URI = database.connection_string  
SQLALCHEMY_TRACKNITIFICATIONS = False