import pickle

def sort_all(data):

    for i in range(len(data)):
        for j in range(0, len(data) - i - 1):
            if data[j][1] > data[j+1][1] :
                data[j], data[j+1] = data[j+1], data[j]
    return data

with open("last_trace.data", "rb") as fp:
    data = pickle.load(fp)
    data = sort_all(data)
    print(data)
    print(len(data))