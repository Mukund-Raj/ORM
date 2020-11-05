from threading import setprofile
from psycopg2.extras import DictCursor
from psycopg2 import Error,DatabaseError
from app import db,fields,formatter


class ColumnNotFoundException(Exception):
    def __init__(self,list_of_columns) -> None:
        '''
        list_of_columns is of type list
        '''
        if not type(list_of_columns) == list:
            raise Exception(f'ColumnNotFoundException Args must be a list Given {type(list_of_columns)}')
        self.message = ' ,'.join(list_of_columns)
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"ColumnNotFoundException : {self.message}, columns are not in the table "

class Tables:
    def __init__(self,**kwargs) -> None:
        self.db_name = kwargs.get('db_name')
        self.table_name = kwargs.get('table_name')
        self.table_type = kwargs.get('table_type')
        self.table_schema = kwargs.get('table_schema')
        #get the all the fields for this table
        self.initialize_fields()

    def create(self, fields_data,return_fields=None):
        '''
        Takes {'column_name':value} like dictionary
        self is the current table,creates a new row in a table
        if return_fields given which should be => []
        it will return (True/False,{coulmn_name:value})
        '''
        con = db.dbs.get_a_connection()
        con.autocommit=False
        cur = None
        try:
            #print('table name is ',self.table_name)
            #: check if received column names exist in this table
            #: set of received column names - set of all column names
            #: if received column names are in the set of all column names then
            #: resulting set will be empty otherwise
            #: it will contain the column name which do not exist in all cokumn names
            #: EX:- x={1,2}  and y={1,2,3,4}
            #: x.difference(y) => x={1,2} - {1,2,3,4} => x={}
            #: if x={1,2,5} and y={1,2,3,4}
            #: x.difference(y) => x={1,2,5} - {1,2,3,4} => x={5}
            #: 5 does not exist in the set y    
            cur = con.cursor(cursor_factory=DictCursor)
            column_names = set(fields_data.keys()).difference(set(self.fields.keys()))
            if column_names:
                raise ColumnNotFoundException(column_names)
            
            insert_query = f"INSERT INTO {self.table_name} ({','.join(fields_data.keys())}) VALUES({','.join(formatter*len(fields_data))})"

            #: if user wants to return some value from the record that just get created
            #: maybe a auto-increment column value then add below RETURNING keyword
            if return_fields:
                insert_query = insert_query + " RETURNING " + ','.join(return_fields)

            insert_values = tuple(fields_data.values())
            print("INSERT query is ",insert_query,insert_values)
            cur.execute(insert_query,insert_values)
            values_to_return = {} 
            if cur.rowcount == 1:
                if return_fields:
                    returned_values = cur.fetchone()
                    for column in return_fields:
                        print(returned_values[column])
                        values_to_return.update({column:returned_values[column]})
                con.commit()
                #: if returning values specified then this
                if return_fields:
                    return True,values_to_return
                #: if simple create query then this
                return True
            
        except (Error,DatabaseError,Exception) as e:
            print('Error in tables ::',e)
            #rollback the transaction if error occur
            con.rollback()
            if return_fields:
                return False,None 
            return False
        finally:
            if con:
                cur.close()
                db.dbs.put_up_a_connection(con)
    
    def write(self, fields_to_write,condition):
        '''
        Takes fields_to_write ==>{'column_name':value} like dictionary
        self is the current table,updates an old row in a table
        condition is also a dict type , tells which row you want to update simply 
        where clause condition
        '''
        con = db.dbs.get_a_connection()
        con.autocommit=False
        cur = None
        try:
            #print('table name is ',self.table_name)
            #: check if received column names exist in this table
            #: set of received column names - set of all column names
            #: if received column names are in the set of all column names then
            #: resulting set will be empty otherwise
            #: it will contain the column name which do not exist in all cokumn names
            #: EX:- x={1,2}  and y={1,2,3,4}
            #: x.difference(y) => x={1,2} - {1,2,3,4} => x={}
            #: if x={1,2,5} and y={1,2,3,4}
            #: x.difference(y) => x={1,2,5} - {1,2,3,4} => x={5}
            #: 5 does not exist in the set y    
            cur = con.cursor(cursor_factory=DictCursor)
            column_names = set(fields_to_write.keys()).difference(set(self.fields.keys()))
            if column_names:
                raise ColumnNotFoundException(column_names)
            
            coulmns_to_update = [ col + '=%s' for col in fields_to_write.keys()]

            insert_query = f"UPDATE {self.table_name} SET ({','.join(coulmns_to_update)}) "

            insert_values = tuple(fields_to_write.values())
            print("INSERT query is ",insert_query,insert_values)
            cur.execute(insert_query,insert_values)
            values_to_return = {} 
            if cur.rowcount == 1:
                con.commit()
                #: if simple create query then this
                return True
            
        except (Error,DatabaseError,Exception) as e:
            print('Error in tables ::',e)
            #rollback the transaction if error occur
            con.rollback()
            return False
        finally:
            if con:
                cur.close()
                db.dbs.put_up_a_connection(con)

    def _make_query(self,params):
        def convert_to_condition(operand):
            """
            Convert ('age','=',12) to age = %s
            """
            return f"{operand[0]} {operand[1]} %s"

        def query_conversion(search_params):
            condition_values = list()
            while True:
                # print(i,search_params[i-1],search_params[i])
                operandB = search_params.pop()
                operandA = search_params.pop()
                operator = 'AND' if search_params.pop() == '&' else 'OR'

                whole_condition = ''
                if type(operandB) == tuple:
                    condition_values.insert(0,operandB[2])
                    operandB = convert_to_condition(operandB)
                elif type(operandB) == list:
                    operandB,new_condition_values = query_conversion(operandB)
                    new_condition_values.extend(condition_values)
                    condition_values = new_condition_values

                if type(operandA) == tuple:
                    condition_values.insert(0,operandA[2])
                    operandA = convert_to_condition(operandA)

                elif type(operandA) == list:
                    operandA,new_condition_values = query_conversion(operandA)
                    new_condition_values.extend(condition_values)
                    condition_values = new_condition_values

                whole_condition = f"{operandA} {operator} {operandB}"
                search_params.append(whole_condition)
                if len(search_params) == 1:
                    break
            return f"({search_params[0]})",condition_values

        condition_count = len(list(filter(lambda c: type(c) == tuple or type(c) == list ,params)))
        for i in range(0,(condition_count*2)-3,2):
            if not params[i] in ['&','|']:
                params.insert(i,'|')
        #: Return full where clause and values associated with the query 
        complete_query, values = query_conversion(params)
        return complete_query, values

    def search(self,search_params):
        complete_query, values = self._make_query(params=search_params)

    def initialize_fields(self):
        # contains all the fields that are in database
        self.fields = {}
        con = db.dbs.get_a_connection()
        cur = None
        try:
            cur = con.cursor(cursor_factory=DictCursor)
            #print('table name is ',self.table_name)
            q = f"select column_name,data_type,is_nullable,character_maximum_length,numeric_precision from information_schema.columns where table_name='{self.table_name}'"
            #print(q)
            cur.execute(q)
            columns = cur.fetchall()
            for column in columns:
                column_data = {
                    'name': column['column_name'],
                    'type': column['data_type'],
                    'is_nullable': column['is_nullable'],
                    'char_length': column['character_maximum_length'],
                    'num_precision': column['numeric_precision']  
                }
                new_field = {
                    column_data['name']: fields.Fields(**column_data)
                }
                self.fields.update(new_field)
            # for field in self.fields:
            #     print('Column data is', self.fields[field].name)

        except (Error,Exception) as e:
            print('Error in tables ::',e)
            #rollback the transaction if error occur
            con.rollback()
        finally:
            if con:
                cur.close()
                db.dbs.put_up_a_connection(con)

    def __str__(self) -> str:
        return f"Table is {self.table_name} of {self.db_name}"