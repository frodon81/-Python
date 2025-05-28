import json

with open("russian-cities.json", "r+",encoding="UTF-8") as f:
    js = json.load(f)
print(len(js))
data = {}
for i in js:
    name = i.get("name")
    print(name)
    coords = i.get("coords")
    data[name] = coords

with open("cities.json","w+",encoding="utf-8") as f:
    json.dump(data,f,ensure_ascii=False)