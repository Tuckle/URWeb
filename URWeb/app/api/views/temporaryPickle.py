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
