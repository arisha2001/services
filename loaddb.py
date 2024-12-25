import json

path = r'/Users/arina/Documents/service/database/descriptions.json'

with open(path, 'w') as t:
    data = {}
    for i in range(int(input("quantity of object's"))):
        data[input('id:')] = input('data:')
    json.dump(data, t)