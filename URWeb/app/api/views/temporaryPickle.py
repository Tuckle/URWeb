import pickle

path = r'pluginsList'


def load(path):
    try:
        with open(path, "rb") as f:
            data = pickle.load(f)
    except Exception:
        return ''
    return data


def dump(path, data):
    try:
        with open(path, "wb") as f:
            pickle.dump(data, f)
    except Exception:
        pass

# data = load(path)
# data[0]['path'] = 'findNearbyPlaces'
# print(data)
# dump(path, data)
data = load(path)
new = {
    'name': 'searchLocationByName',
    'description': 'Searches location based on input text',
    'path': 'searchLocationByName'
}

print(data)
data = data[:3]
print(data)
#exit(1)
#data.append(new)
dump(path, data)

