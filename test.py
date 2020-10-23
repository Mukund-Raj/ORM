
# x={'a':1,'b':2,'c':3,'d':4}

# y={'a':2,'d':5}

# d=set(y.keys()).difference(set(x.keys()))
# if d:
#     print('keys dont exist')
# else:
#     print(d)
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

def xc(**kwargs):
    print(kwargs.get('x',False))

xc(s=0)
xc(x=[1,2])
sep = ['%s']*4
print(sep)

x={'1':1,'2':2}
y=tuple(x.values())
print(len(x),y)