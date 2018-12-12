#requires python3.7.0
from typing import *
import pandas as pd
import psycopg2 as pg
import json


class DbCaller:
    """
    Object used to call a database connector and make requests.
    Store results in  a dataframe and keep in memory the last request.
    """
    host: str
    password: str
    db_name: str
    user: str
    conn: Any = None
    data: Any = None
    dataList: Dict[Any] = dict()

    def __init__(self, host, pwd, user, database):
        self.host = host
        self.password = pwd
        self.user = user
        self.db_name = database
        self.setup()

    def __call__(self, sql_query, json_query=False):
        if self.conn is not None:
            self.raw_request(sql_query)
            return self.data
        else:
            print("Connection not initialized")

    def setup(self):
        """
        Initialize connection to database
        :return: Nothing
        """
        try:
            self.conn = pg.connect(host=self.host,
                                   dbname=self.db_name,
                                   user=self.user,
                                   password=self.password)
        except ConnectionError as e:
            print(e)

    def raw_request(self, sql_query: str):
        """
        Make a query with a raw query
        :param sql_query: your sql query ( string )
        :return: pandas dataframe containing query response
        """
        try:
            self.data = pd.read_sql_query(sql_query, con=self.conn)
            return self.data
        except ConnectionError as e:
            print(e)

    def json_request(self, path: str):
        """
        Makes request(S) from JSON.
        :param path: Path to JSON file
        :return: A Dict of dataframes containing the responses.
        """
        try:
            with open(path, "r") as file:
                data = json.load(file)
        except FileNotFoundError as e:
            print(e, " at path %s" % path)
            return 0

        try:
            for i, query in enumerate(data["queries"]):
                cols = ','.join(query["columns"])
                tables = ','.join(query["table"])
                where = ' AND '.join(query["WHERE"])
                sql_query = "SELECT %s FROM %s WHERE %s" % (cols, tables, where)
                self.dataList[i] = self.raw_request(sql_query)
                return self.dataList

        except KeyError as e:
            print(e, "Wrong shape")
