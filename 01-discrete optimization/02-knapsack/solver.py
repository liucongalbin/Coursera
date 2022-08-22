#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import json
Item = namedtuple("Item", ['index', 'value', 'weight'])


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    # 打印当前数据集的size和capacity
    print("size: " + str(item_count) + ", capacity: " + str(capacity))

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = [0]*len(items)

    # TODO 如果是题目1~4，调用动态规划求解，否则调用贪心算法求解
    # 调用动态规划求解
    if capacity > 350000:
        # default提供的贪心法
        for item in items:
            if weight + item.weight <= capacity:
                taken[item.index] = 1
                value += item.value
                weight += item.weight
    else:
        value, weight, taken = dy_pro3(item_count, capacity, items, taken)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


# 动态规划求解
def dy_pro(item_count, capacity, items, taken):
    # 初始化表 横、纵坐标都从0开始
    dy_table = {}

    # TODO item元素从小到大排序？（应该不需要）

    # 初始化第0列
    col0 = {}
    for k in range(0, capacity + 1):
        col0[str(k)] = ({"v": 0, "w": 0, "i": []})

    dy_table[str(0)] = col0

    # 遍历矩阵 - 列
    # for item, idx in items:
    for col_idx in range(1, item_count + 1):

        col = {} # 初始化列
        # col.append(Cell(0, 0, [])) # 容量为0时的元素
        item = items[col_idx - 1] # 当前元素
        left_col = dy_table[str(col_idx - 1)] # 上一列元素（整列）

        # 遍历容量
        for k in range(0, capacity + 1):

            left_cell = left_col[str(k)]
            # 默认取左侧元素的值
            cell = {
                "v": left_cell["v"],
                "w": left_cell["w"],
                "i": left_cell["i"]
            }

            # 如果取当前列新增元素
            if k >= item.weight: # 容量满足才取
                # 取左上角对应元素
                left_up_cell = left_col[str(k - item.weight)]

                # 如果取当前元素后，融合值大于左侧元素，则取，否则不取
                if (left_up_cell["v"] + item.value) > left_cell["v"] \
                        and (left_up_cell["w"] + item.weight) <= k:

                    # 把新元素各熟悉融合进去
                    idx = left_up_cell["i"].copy()
                    idx.append(col_idx - 1)
                    cell = {
                        "v": left_up_cell["v"] + item.value,
                        "w": left_up_cell["w"] + item.weight,
                        "i": idx
                    }

            # 把 单元 添加到 列 里面
            col[str(k)] = cell

        # 把 列 添加到 表 里面
        dy_table[str(col_idx)] = col

    # 调试用
    # print(json.dumps(dy_table))
    with open('res.json', 'w') as f:
        json.dump(dy_table, f)

    # 得最大值
    final_cell = dy_table[str(item_count)][str(capacity)]
    print(final_cell)

    # 反推解
    value, weight = final_cell["v"], final_cell["w"]
    for idx in final_cell["i"]:
        taken[idx] = 1

    return value, weight, taken


# 动态规划求解2（只记录上一列）
def dy_pro2(item_count, capacity, items, taken):
       # 初始化第0列
    left_col = {}
    for k in range(0, capacity + 1):
        left_col[str(k)] = ({"v": 0, "w": 0, "i": []})

    # 遍历矩阵 - 列
    # for item, idx in items:
    for col_idx in range(1, item_count + 1):

        col = {} # 初始化列
        # col.append(Cell(0, 0, [])) # 容量为0时的元素
        item = items[col_idx - 1] # 当前元素

        # 遍历容量
        for k in range(0, capacity + 1):

            left_cell = left_col[str(k)]
            # 默认取左侧元素的值
            cell = left_cell

            # 如果取当前列新增元素
            if k >= item.weight: # 容量满足才取
                # 取左上角对应元素
                left_up_cell = left_col[str(k - item.weight)]

                # 如果取当前元素后，融合值大于左侧元素，则取，否则不取
                if (left_up_cell["v"] + item.value) > left_cell["v"] \
                        and (left_up_cell["w"] + item.weight) <= k:

                    # 把新元素各熟悉融合进去
                    idx = left_up_cell["i"].copy()
                    idx.append(col_idx - 1)
                    cell = {
                        "v": left_up_cell["v"] + item.value,
                        "w": left_up_cell["w"] + item.weight,
                        "i": idx
                    }

            # 把 单元 添加到 列 里面
            col[str(k)] = cell

        # 把 左列替换
        left_col = col

    # 调试用
    # print(json.dumps(dy_table))
    with open('res.json', 'w') as f:
        json.dump(left_col, f)

    # 得最大值
    final_cell = left_col[str(capacity)]
    print(final_cell)

    # 反推解
    value, weight = final_cell["v"], final_cell["w"]
    for idx in final_cell["i"]:
        taken[idx] = 1

    return value, weight, taken


# 动态规划求解3（只记录上一列）（当前所有物品都放入后，下一项复制当前项）
def dy_pro3(item_count, capacity, items, taken):
    # 初始化第0列
    left_col = {}
    for k in range(0, capacity + 1):
        left_col[str(k)] = ({"v": 0, "w": 0, "i": []})

    # 当前所有元素的最大值
    weight_total = 0

    # 遍历矩阵 - 列
    # for item, idx in items:
    for col_idx in range(1, item_count + 1):

        if col_idx % 50 == 0:
            print("遍历列，当前为第%d列。" % col_idx)

        col = {} # 初始化列
        item = items[col_idx - 1] # 当前元素

        # 用于判断某一列，是否已经取到了最大值（最大值：当前列对应元素及此前所有列对应的元素的weight之和）
        weight_total = weight_total + item.weight # 每列对应一个元素

        # 遍历容量
        for k in range(0, capacity + 1):

            # if k % 5000 == 0:
            #     print("遍历行，当前为第%d行。" % k)

            # 如果 当前背包容量 已经大于 当前所有元素的weight之和，说明后续结果都一样
            if k > weight_total:
                col[str(k)] = col[str(k - 1)]
                continue

            # 左侧元素

            left_cell = left_col[str(k)]

            # 默认取左侧元素的值（因为不修改，可以直接引用，避免浪费内存）
            cell = left_cell

            # 如果取当前列新增元素
            if k >= item.weight: # 容量满足才取
                # 取左上角对应元素
                left_up_cell = left_col[str(k - item.weight)]

                # 如果取当前元素后，融合值大于左侧元素，则取，否则不取
                if (left_up_cell["v"] + item.value) > left_cell["v"] \
                        and (left_up_cell["w"] + item.weight) <= k:

                    # 把新元素各熟悉融合进去
                    idx = left_up_cell["i"].copy()
                    idx.append(col_idx - 1)
                    cell = {
                        "v": left_up_cell["v"] + item.value,
                        "w": left_up_cell["w"] + item.weight,
                        "i": idx
                    }

            # 把 单元 添加到 列 里面
            col[str(k)] = cell

        # 把 左列替换
        left_col = col

    # 调试用
    # print(json.dumps(dy_table))
    with open('res.json', 'w') as f:
        json.dump(left_col, f)

    # 得最大值
    final_cell = left_col[str(capacity)]
    print(final_cell)

    # 反推解
    value, weight = final_cell["v"], final_cell["w"]
    for idx in final_cell["i"]:
        taken[idx] = 1

    return value, weight, taken


# 动态规划求解4（只记录上一列）（当前所有物品都放入后，标记索引，打破循环）
def dy_pro4(item_count, capacity, items, taken):
    # 初始化第0列
    left_col = {}
    for k in range(0, capacity + 1):
        left_col[str(k)] = ({"v": 0, "w": 0, "i": []})

    # 上一列 所有元素的最大值 对应的索引
    left_idx_total = 0

    # 当前所有元素的最大值
    weight_total = 0

    # 遍历矩阵 - 列
    # for item, idx in items:
    for col_idx in range(1, item_count + 1):

        if col_idx % 50 == 0:
            print("遍历列，当前为第%d列。" % col_idx)

        col = {} # 初始化列
        item = items[col_idx - 1] # 当前元素

        # 用于判断某一列，是否已经取到了最大值（最大值：当前列对应元素及此前所有列对应的元素的weight之和）
        weight_total = weight_total + item.weight # 每列对应一个元素

        # 遍历容量
        for k in range(0, capacity + 1):

            # if k % 5000 == 0:
            #     print("遍历行，当前为第%d行。" % k)

            # 如果 当前背包容量 已经大于 当前所有元素的weight之和，说明后续结果都一样
            if k > weight_total:
                col[str(k)] = col[str(k - 1)]
                left_idx_total = weight_total
                break

            # 左侧元素
            if k > left_idx_total:
                left_cell = left_col[str(left_idx_total)]
            else:
                left_cell = left_col[str(k)]

            # 默认取左侧元素的值（因为不修改，可以直接引用，避免浪费内存）
            cell = left_cell

            # 如果取当前列新增元素
            if k >= item.weight: # 容量满足才取
                # 取左上角对应元素
                left_up_cell = left_col[str(k - item.weight)]

                # 如果取当前元素后，融合值大于左侧元素，则取，否则不取
                if (left_up_cell["v"] + item.value) > left_cell["v"] \
                        and (left_up_cell["w"] + item.weight) <= k:

                    # 把新元素各熟悉融合进去
                    idx = left_up_cell["i"].copy()
                    idx.append(col_idx - 1)
                    cell = {
                        "v": left_up_cell["v"] + item.value,
                        "w": left_up_cell["w"] + item.weight,
                        "i": idx
                    }

            # 把 单元 添加到 列 里面
            col[str(k)] = cell

        # 把 左列替换
        left_col = col

    # 调试用
    # print(json.dumps(dy_table))
    with open('res.json', 'w') as f:
        json.dump(left_col, f)

    # 得最大值
    final_cell = left_col[str(capacity)]
    print(final_cell)

    # 反推解
    value, weight = final_cell["v"], final_cell["w"]
    for idx in final_cell["i"]:
        taken[idx] = 1

    return value, weight, taken

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

