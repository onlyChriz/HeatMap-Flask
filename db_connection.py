class db_connection:
    def __init__(self, database):
        self.database = database
        self.connection_string = database.connection_string
    
