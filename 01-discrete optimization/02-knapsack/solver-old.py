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

    # for item in items:
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight

    # 调用动态规划求解
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
        col0[str(k)] = ({"value": 0, "weight": 0, "idx": []})

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
                "value": left_cell["value"],
                "weight": left_cell["weight"],
                "idx": left_cell["idx"]
            }

            # 如果取当前列新增元素
            if k >= item.weight: # 容量满足才取
                # 取左上角对应元素
                left_up_cell = left_col[str(k - item.weight)]

                # 如果取当前元素后，融合值大于左侧元素，则取，否则不取
                if (left_up_cell["value"] + item.value) > left_cell["value"] \
                        and (left_up_cell["weight"] + item.weight) <= k:

                    # 把新元素各熟悉融合进去
                    idx = left_up_cell["idx"].copy()
                    idx.append(col_idx - 1)
                    cell = {
                        "value": left_up_cell["value"] + item.value,
                        "weight": left_up_cell["weight"] + item.weight,
                        "idx": idx
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
    value, weight = final_cell["value"], final_cell["weight"]
    for idx in final_cell["idx"]:
        taken[idx] = 1

    return value, weight, taken


# 动态规划求解2（只记录上一列）
def dy_pro2(item_count, capacity, items, taken):
       # 初始化第0列
    left_col = {}
    for k in range(0, capacity + 1):
        left_col[str(k)] = ({"value": 0, "weight": 0, "idx": []})

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
            cell = {
                "value": left_cell["value"],
                "weight": left_cell["weight"],
                "idx": left_cell["idx"]
            }

            # 如果取当前列新增元素
            if k >= item.weight: # 容量满足才取
                # 取左上角对应元素
                left_up_cell = left_col[str(k - item.weight)]

                # 如果取当前元素后，融合值大于左侧元素，则取，否则不取
                if (left_up_cell["value"] + item.value) > left_cell["value"] \
                        and (left_up_cell["weight"] + item.weight) <= k:

                    # 把新元素各熟悉融合进去
                    idx = left_up_cell["idx"].copy()
                    idx.append(col_idx - 1)
                    cell = {
                        "value": left_up_cell["value"] + item.value,
                        "weight": left_up_cell["weight"] + item.weight,
                        "idx": idx
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
    value, weight = final_cell["value"], final_cell["weight"]
    for idx in final_cell["idx"]:
        taken[idx] = 1

    return value, weight, taken


# 动态规划求解3（只记录上一列）（计算仅从）
def dy_pro3(item_count, capacity, items, taken):
       # 初始化第0列
    left_col = {}
    for k in range(0, capacity + 1):
        left_col[str(k)] = ({"value": 0, "weight": 0, "idx": []})

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
            cell = {
                "value": left_cell["value"],
                "weight": left_cell["weight"],
                "idx": left_cell["idx"]
            }

            # 如果取当前列新增元素
            if k >= item.weight: # 容量满足才取
                # 取左上角对应元素
                left_up_cell = left_col[str(k - item.weight)]

                # 如果取当前元素后，融合值大于左侧元素，则取，否则不取
                if (left_up_cell["value"] + item.value) > left_cell["value"] \
                        and (left_up_cell["weight"] + item.weight) <= k:

                    # 把新元素各熟悉融合进去
                    idx = left_up_cell["idx"].copy()
                    idx.append(col_idx - 1)
                    cell = {
                        "value": left_up_cell["value"] + item.value,
                        "weight": left_up_cell["weight"] + item.weight,
                        "idx": idx
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
    value, weight = final_cell["value"], final_cell["weight"]
    for idx in final_cell["idx"]:
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

