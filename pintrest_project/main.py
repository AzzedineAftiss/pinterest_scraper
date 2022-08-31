import json

# Opening JSON file
f = open('C:/Users/hp/PycharmProjects/PinterestProject/pintrest_project/pintrest_project/file.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
# list
print(f"length of data is {len(data)}")
data1 = []
for d in data:
    data1.append(d["pin"])
    print(not "board" in d.keys())
    # print(d["tot"])
    break
# print(f"length of data is {len(set(data1))}")

# Closing file
f.close()