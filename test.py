
# x={'a':1,'b':2,'c':3,'d':4}

# y={'a':2,'d':5}

# d=set(y.keys()).difference(set(x.keys()))
# if d:
#     print('keys dont exist')
# else:
#     print(d)
from app import fields
import re

# class ColumnNotFoundException(Exception):
#     def __init__(self,list_of_columns) -> None:
#         if not type(list_of_columns) == list:
#             raise Exception(f'ColumnNotFoundException Args must be a list Given {type(list_of_columns)}')
#         self.message = ' ,'.join(list_of_columns)
#         super().__init__(self.message)

#     def __str__(self) -> str:
#         return f"ColumnNotFoundException : {self.message} "

# def okk():
#     try:
#         x=['a','b']
#         y=1
#         if y==1:
#             raise ColumnNotFoundException(x)
#     except ColumnNotFoundException as e:
#         return e
#     except (Exception) as e:
#         print('error ',e)

# s=okk()
# print(s,type(s))
# if s:
#     print('Inserted')
# else:
#     print('failed')

# def xc(**kwargs):
#     print(kwargs.get('x',False))

# xc(s=0)
# xc(x=[1,2])
# sep = ['%s']*4
# print(sep)

# x={'1':1,'2':2}
# y=[ q+'=%s' for q in x.keys()]
# print(y)
# y=tuple(x.values())
# print(len(x),y)

# x={'1':1,'2':2}

# y=[q+'=%s' for q in x.keys()]
# print(y,','.join(y))

def unwarp_tuple(search_tuple):
    print(search_tuple)

# def search(fields_to_add,search_list):
#     #: received a big list with conditions
#     if type(search_list) != list:
#         return False
#     condition_columns = []
#     condition_query = []
#     count=0
#     i=len(search_list)-1
#     while i>=0:
#     #for i in range(len(search_list)-1,-1,-1):
#         operator = search_list[i-2]
#         operandA = search_list[i-1]
#         operandB = search_list[i]
#         if type(search_list[i]==tuple):
#             condition_query.append()
#         if type(operandA) != tuple or type(operandB) != tuple or \
#             len(operandB) != 3 or len(operandA)!=3:
#             return False
        
#         condition_columns_1 = f"{operandA[0]} {operandA[1]} %s"
#         condition_columns_2 = f"{operandB[0]} {operandB[1]} %s"
#         #print(condition_columns_1,condition_columns_2)
#         condition_query = f"( {condition_columns_1} {operator} {condition_columns_2} ){condition_query}"
#         # print(condition_query)
#         # count = count+1
#         i=i-3
#         #search_list[i] = condition_columns
#         #condition_query.insert(0,condition_columns)

#     #print(condition_query)

#     return condition_query
#     #condition_list.append(' '.join(list(t)))
#     #print(' and '.join(condition_list),)

#     # fields = [ q+'=%s' for q in fields_to_add.keys()]
#     # #print(type(fields),fields)
#     # query = f"UPDATE testing SET {','.join(fields)} WHERE {condition_columns}"
#     #print(query)


def make_query(search_params):
    def convert_to_condition(operand):
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
        # print(search_params)
        return f"({search_params[0]})",condition_values

    condition_count = len(list(filter(lambda c: type(c) == tuple or type(c) == list ,search_params)))
    for i in range(0,(condition_count*2)-3,2):
        if not search_params[i] in ['&','|']:
            search_params.insert(i,'|')

    # print(search_params)
    whole_query, values = query_conversion(search_params)
    return whole_query ,values
    # print(whole_query)


def search(search_params):
    full_query, values = make_query(search_params)
    print(full_query,values)
    

print(search(['&',('city','like','%%usa'),('reqid','=',12)]))