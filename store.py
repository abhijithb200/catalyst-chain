# https://pypi.org/project/sqlitedict/



# from sqlitedict import SqliteDict


# db = SqliteDict("ex.sqlite",autocommit=True)


# for key, item in db.items():
#     print("%s=%s" % (key, item))

import yaml

with open('settings.yaml') as file:
    try:
        data = yaml.safe_load(file)
        print(data)
        for i in data[0]['master']:
            print(i['ip'],i['port'])
    except yaml.YAMLError as exception:
        print(exception)