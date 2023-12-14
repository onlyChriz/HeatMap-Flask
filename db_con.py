class db_con():
    def __init__(self):
        self.DRIVER_NAME = 'db'
        self.SERVER_NAME = 'server'
        self.DATABASE_NAME = 'database'

        self.connection_string = f"mssql+pyodbc://{self.SERVER_NAME}/{self.DATABASE_NAME}?driver={self.DRIVER_NAME}"
