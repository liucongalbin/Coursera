import random
import sys


def t_list():
    l = []
    print(l)

    # [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    s = [0] * 10
    print(s)


def t_for():
    for k in range(0, 4):
        print(k)

def t_plus():
    num = 1
    print(num)
    num += 1
    print(num)


def t_table():
    t = {'name': {}, 'age': {}, 'sex': {}}
    print('name' in t)
    print('name1' in t)
    # print(t.has_key('name'))

    t_n = t['name']
    print('name:')
    print(t_n)

    # t_n1 = t['name1']
    # print(t_n1)
    t2 =  {'name': 'liuc', 'age': 33, 'sex': 'male'}
    t2_reverse = {value: key for key, value in t2.items()}
    print(t2_reverse)


def t_table2():
    key_value = {2: 56, 1: 2, 5: 12, 4: 24, 6: 18 , 3: 323}
    for key in sorted(key_value):
        print("key:" + str(key) + ", value: " + str(key_value[key]))

    print("------------------")

    # https://www.runoob.com/python3/python-sort-dictionaries-by-key-or-value.html
    key_value_by_value = sorted(key_value.items(), key = lambda kv: (kv[1], kv[0]))
    for key, value in key_value_by_value:
        print("key:" + str(key) + ", value: " + str(value))

    print("------------------")

    key_value_by_value = sorted(key_value.items(), key = lambda kv: kv[1])
    for key, value in key_value_by_value:
        print("key:" + str(key) + ", value: " + str(value))

    print("------------------")

    key_value_by_value = sorted(key_value.items(), key = lambda kv: kv[1], reverse = True)
    for key, value in key_value_by_value:
        print("key:" + str(key) + ", value: " + str(value))


def t_table3():
    map1 = {2: 56, 1: 2, 5: 12, 4: 24, 6: 18 , 3: 323}

    # 找最大值
    res = max(map1, key= lambda x: map1[x])
    print(res)

    for key in map1:
        print("key:" + str(key) + ", value: " + str(map1[key]))

    # 当字典不为空
    # 移除最大值
    map1.pop(res)
    print("------------------")

    for key in map1:
        print("key:" + str(key) + ", value: " + str(map1[key]))

    print("------------------")

    while(len(map1) > 0):
        res = max(map1, key=lambda x: map1[x])
        print(res, map1[res])
        map1.pop(res)


def t_lambda():
    a = lambda x, y: x + y + 3
    print(a(3,5))

def t_random():
    r = random.random()
    print(r)

def t_list2str():
    l = [1,2,3,4,5,6]
    s = str(l)
    s2 = ''.join([str(i) for i in l])
    print(s)
    print(s2)

def t_int():
    r = sys.maxsize
    print(r)

def t_var():
    a = False
    print(a)

    a = "123456678"
    print(a)

def t_shuffle():
    s = list(range(0, 51))
    random.shuffle(s)
    print(s)
    random.shuffle(s)
    print(s)
    random.shuffle(s)
    print(s)

def t_range():
    l1 = range(0, 8)
    # print(l1)
    #
    # print("----------------")

    l2 = list(l1)
    print("l2:", end=" ")
    print(l2)

    print("----------------")

    l4 = l2
    print("l4[1: 3]:", end=" ")
    print(l4[1: 3])
    # print(l2[1: 3: -1])

    print("list(reversed(l2[1: 3])):", end=" ")
    print(list(reversed(l2[1: 3])))
    # print(reversed(l2[1: 3]))
    # print(l2[: : -1])
    l4[1: 3] = list(reversed(l2[1: 3]))
    print("l4:", end=" ")
    print(l4)

    # print("----------------")
    #
    # l4 = l2.copy()
    # l4[0: 8] = list(reversed(l2[0: 8]))
    # print(l4)
    # l4[0: 9] = list(reversed(l2[0: 9]))
    # print(l4)

def t_list2():
    l = [1,2,3,4,5,6,11,34]
    print(l)
    print(l[-1])
    l.remove(11)
    print(l)


# t_list()
t_list2()

