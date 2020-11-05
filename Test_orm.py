from app import dbs
db=None

def Test1():
    returned_values = db.db_tables['testing'].create({'reqid':14,'name':'mukund raj','status':True},['reqid'])
    if returned_values[0]:
        print('ROW been created')
        print(f"Returned values are {returned_values[1]['reqid']},{returned_values[1]['status']}")
    returned_values = db.db_tables['testing'].create({'reqid':14,'name':'Raj','status':False})
    print(returned_values)
    returned_values = db.db_tables['testing'].create({'reqid':15,'name':'Akash','status':True})
    print(returned_values)
    returned_values = db.db_tables['testing'].create({'reqid':16,'name':'AB devilliars','status':False})
    print(returned_values)
    returned_values = db.db_tables['testing'].create({'reqid':17,'name':'mukund raj','status':True})
    print(returned_values)
    returned_values = db.db_tables['testing'].create({'reqid':18,'name':'Ak gupta','status':False})
    print(returned_values)

if __name__ == "__main__":
    db = dbs(1,5,database='testdb',user='postgres',password='12345',host='127.0.0.1',port=5433)