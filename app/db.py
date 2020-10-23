from app import fields
from .tables import Tables
from psycopg2 import pool,Error
from psycopg2.extras import DictCursor

class dbs:
    # static so that tables class can access it
    db_conn_pool = None 
    def __init__(self,min_conn,max_conn,*args,**kwargs) -> None:
        """
        Initialize the database ,create a connection pool
        """
        # dict for all tables in database
        # key:table name ,value Table class
        self.db_tables = {}
        dbs.db_conn_pool = self._create_connection_pool(min_conn,max_conn,*args,**kwargs)
        if not dbs.db_conn_pool:
            raise Exception('Couldn\'t able to create connection pool for given arguments')
        
        self.get_schema_info()

    def get_schema_info(self):
        con = self.get_a_connection()
        cur = None
        try:
            cur = con.cursor(cursor_factory=DictCursor)
            q = "SELECT * FROM information_schema.tables where table_schema='public'"
            cur.execute(q)
            all_tables = cur.fetchall()
            #print(all_tables)
            for table in all_tables:
                table_data = {
                    'table_name': table['table_name'],
                    'table_type': table['table_type'],
                    'table_schema': table['table_schema'],
                    'db_name': table['table_catalog'] 
                }
                #print('All tables are ',table_data)
                new_table ={
                    table['table_name']: Tables(**table_data)
                } 
                self.db_tables.update(new_table)

        except (Error,Exception) as e:
            print('error ::',e)
            #rollback the transaction if error occur
            con.rollback()
            return False
        finally:
            if con:
                cur.close()
                self.put_up_a_connection(con)

    @staticmethod
    def get_a_connection():
        '''
        Get a database connection from connection pool by calling db_conn_pool.getconn()
        It will loop untill a connection found and then return it
        '''
        #keep loping untill you get a connection object 
        while True:
            #getting a conection from pool
            con = dbs.db_conn_pool.getconn()
            if con:
                #connection found return it to the fucntion that is being called
                return con

    @staticmethod
    def put_up_a_connection(con):
        """
        Put up a database connection con back to the pool
        """
        dbs.db_conn_pool.putconn(con)

    def _create_connection_pool(self,min_conn,max_conn,*args,**kwargs):
        """
        minconn: Minimum connection
        maxconn: Maximum connection
        Kwargs ::
        database : Database Name
        user : User of the database you want to connect as
        Password : Password for DB
        Host : Ip address such as 127.0.0.1
        port : 5433
        """
        try:
            return pool.ThreadedConnectionPool(min_conn,max_conn,*args,**kwargs)
        except Exception as e:
            print('ERROR in create_connection_pool ',e)
            return False
