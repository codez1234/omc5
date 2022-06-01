import geopy.distance
# [(55.123521, 85.123455), (55.223521, 85.123455), (55.223521, 85.223455), (55.223521, 85.223455), (55.223521, 85.223455)]
# 0.0037300889901033065
data = [(22.504, 88.300),
        (22.500, 88.300)]


def total_distance(lst):
    if len(lst) == 1:
        return None
    x = len(lst) - 1
    i = 0
    d = 0
    while x:
        coords_1 = lst[i]
        coords_2 = lst[i+1]
        i += 1
        x -= 1
        d += geopy.distance.distance(coords_1, coords_2).km
        # print(d)

    return d


# print(total_distance(data))


# print(cal([(55.123521, 85.123455), (55.223521, 85.123455), (55.223521,
#       85.223455), (55.223521, 55.223455), (55.223521, 95.223455)]))
