import pyodbc
import mysql.connector
import psycopg2
import cx_Oracle
import pymongo


class DatabaseConnector:
    def __init__(self, db_type, **kwargs):
        self.db_type = db_type
        self.connection = None
        self.connection_params = kwargs

    def connect(self):
        if self.db_type == 'mysql':
            self.connection = mysql.connector.connect(**self.connection_params)
        elif self.db_type == 'postgresql':
            self.connection = psycopg2.connect(**self.connection_params)
            self.connection.autocommit = True
        elif self.db_type == 'mssql':
            self.connection = pyodbc.connect(**self.connection_params)
            self.connection.autocommit = True
        elif self.db_type == 'oracle':  # not being tested.
            dsn_tns = cx_Oracle.makedsn(**self.connection_params)
            self.connection = cx_Oracle.connect(dsn=dsn_tns)
        elif self.db_type == 'mongodb':
            mongo_uri = f"mongodb://{self.connection_params['username']}:{self.connection_params['password']}@" \
                        f"{self.connection_params['host']}:{self.connection_params['port']}/"
            self.connection = pymongo.MongoClient(mongo_uri)
            self.connection_params['client'] = self.connection
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query):
        if not self.connection:
            raise Exception("Connection not established.")

        if self.db_type == 'mongodb':
            db_name = self.connection_params.get('db', None)
            if not db_name:
                raise ValueError("Database name not provided for MongoDB.")
            db = self.connection[db_name]
            return db
        else:
            cursor = self.connection.cursor()
            try:
                cursor.execute(query)
                if cursor.description is not None:  # Check if the query produces any result set
                    result = cursor.fetchall()
                else:
                    result = "Query executed successfully."  # Success message for non-result queries
            finally:
                cursor.close()

        return result

