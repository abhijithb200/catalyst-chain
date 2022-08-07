# https://pypi.org/project/sqlitedict/



from sqlitedict import SqliteDict


db = SqliteDict("ex.sqlite",autocommit=True)


for key, item in db.items():
    print("%s=%s" % (key, item))

