from app import dbs

db = dbs(1,5,database='testdb',user='postgres',password='12345',host='127.0.0.1',port=5433)


if __name__ == "__main__":
    while True:
        if db:
            print(db.db_tables['testing'].db_name)
            returned_values = db.db_tables['testing'].create({'reqid':21,'name':'Toomy','status':True})
            print(returned_values)
        userin = int(input('Enter 1 to exit'))
        if userin == 1:
            break