import math

def get_data(name):
    with open(name,"r") as f:
        data = f.readlines()
    length = 0
    for i in range(len(data)):
        data[i] = data[i].strip()
        length += len(data[i])
    return data,length

if __name__ == '__main__':
    name = "watermelon_3a.csv"
    data , length = get_data(name)
    all = {}
    for i in data:
        for j in i:
            if not j in all.keys():
                all[j] = 0
            else:
                all[j] += 1
    Ent = 0
    for i in all.keys():
        if all[i]/length == 0:
            Ent += 0
        else:
            Ent += -all[i]/length * math.log(all[i]/length) / math.log(2)
    print(Ent)