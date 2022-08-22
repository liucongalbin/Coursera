#!/usr/bin/python
# -*- coding: utf-8 -*-


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # 打印输入数据的尺寸
    # 1.node_count: 50,edge_count: 350 （7 point：8）
    # 2.node_count: 70,edge_count: 1678 （7 point：20）
    # 3.node_count: 100,edge_count: 2502 （7 point：21）
    # 4.node_count: 250,edge_count: 28046 （7 point：95）
    # 5.node_count: 500,edge_count: 12565 （7 point：18）
    # 6.node_count: 1000,edge_count: 249482 （7 point：124）
    print("node_count: " + str(node_count) + ",edge_count: " + str(edge_count))

    # build a trivial solution
    # every node has its own color
    solution = range(0, node_count)

    # 调用方法求解
    if node_count == 70:
        num_colors, solution = CP_3(node_count, edge_count, edges)
    else:
        num_colors, solution = CP_3(node_count, edge_count, edges)

    # prepare the solution in the specified output format
    output_data = str(num_colors) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data



# 1.node_count: 50,edge_count: 350 （7 point：8） 9
# 2.node_count: 70,edge_count: 1678 （7 point：20） 21
# 3.node_count: 100,edge_count: 2502 （7 point：21） 21
# 4.node_count: 250,edge_count: 28046 （7 point：95） 96
# 5.node_count: 500,edge_count: 12565 （7 point：18） 19
# 6.node_count: 1000,edge_count: 249482 （7 point：124） 121
# 采用了简单的启发式：每个节点，统计其关联节点数，从大到小排序，按此顺序赋值
def CP_1(node_count, edge_count, edges):

    # 顶点表1 key：顶点， value：表：相关的顶点
    # 顶点表2 key：顶点， value：节点数
    v_table1 = {}
    v_table2 = {}
    for edge in edges:
        v1, v2 = edge[0], edge[1]
        t1_v1, t1_v2 = [], [] # 相关节点list

        # 从顶点表1、2中取2个顶点对应的子表
        if v1 in v_table1:
            t1_v1 = v_table1[v1]
        if v2 in v_table1:
            t1_v2 = v_table1[v2]

        # 互相添加到对方的相关节点list中
        t1_v1.append(v2)
        t1_v2.append(v1)

        # 保存相关节点list到总表
        v_table1[v1] = t1_v1
        v_table1[v2] = t1_v2

        # 相关节点数，各自累加1次
        if v1 in v_table2:
            v_table2[v1] += 1
        else:
            v_table2[v1] = 1

        if v2 in v_table2:
            v_table2[v2] += 1
        else:
            v_table2[v2] = 1

    # 顶点表2 key-value交换，并按节点数排序
    v_t2_rank = sorted(v_table2.items(), key = lambda kv: kv[1], reverse = True)

    # 初始化，颜色表，key：每个顶点， value：颜色
    # 初始化，相邻颜色表，key：顶点， value：相邻节点颜色set?
    t_color = {}
    t_adj_color = {}

    # 按节点数 从多到少，给相邻节点赋值（颜色）
    for key in v_t2_rank:
        vertice = key[0]
        # 取相邻节点的颜色集合（根据相邻颜色，先给自己赋值，并记录颜色）
        if vertice in t_adj_color:
            v_adj_color = t_adj_color[vertice]
        else:
            v_adj_color = set()

        # 默认自身颜色是0
        v_color = 0

        # 遍历寻找最小自然数（相邻节点未使用的最小颜色）
        for i in range(0, len(v_adj_color) + 2):
            if i not in v_adj_color:
                v_color = i
                break

        # 记录下自身的颜色
        t_color[vertice] = v_color

        # 把自己的颜色，更新到相邻节点的“相邻节点颜色set”中
        # 取相邻节点，遍历
        adj_v_list = v_table1[vertice]
        for adj_v in adj_v_list:

            # 取相邻节点的“相邻节点颜色set”
            # 如果相邻节点尚未赋值，则添加进对方的“相邻节点颜色set”中
            if adj_v not in t_color:
                if adj_v in t_adj_color:
                    adj_color_set = t_adj_color[adj_v]
                else:
                    adj_color_set = set()

                adj_color_set.add(v_color)
                t_adj_color[adj_v] = adj_color_set # TODO 这个需要吗？

    # 拼接结果
    solution = []
    solution_set = set()
    for v in sorted(t_color):
        solution.append(t_color[v])
        solution_set.add(t_color[v])

    num_colors = len(solution_set)

    return num_colors, solution

# 1.node_count: 50,edge_count: 350 （7 point：8） 7
# 2.node_count: 70,edge_count: 1678 （7 point：20） 21
# 3.node_count: 100,edge_count: 2502 （7 point：21） 20
# 4.node_count: 250,edge_count: 28046 （7 point：95） 91
# 5.node_count: 500,edge_count: 12565 （7 point：18） 18
# 6.node_count: 1000,edge_count: 249482 （7 point：124） 120
# 相比CP_1：当某个点被赋值后，更新一遍关联节点表，当前点相关的节点，其关联节点数-1
def CP_2(node_count, edge_count, edges):

    # 顶点表1 key：顶点， value：表：相关的顶点
    # 顶点表2 key：顶点， value：节点数
    v_table1 = {}
    v_table2 = {}
    for edge in edges:
        v1, v2 = edge[0], edge[1]
        t1_v1, t1_v2 = [], [] # 相关节点list

        # 从顶点表1、2中取2个顶点对应的子表
        if v1 in v_table1:
            t1_v1 = v_table1[v1]
        if v2 in v_table1:
            t1_v2 = v_table1[v2]

        # 互相添加到对方的相关节点list中
        t1_v1.append(v2)
        t1_v2.append(v1)

        # 保存相关节点list到总表
        v_table1[v1] = t1_v1
        v_table1[v2] = t1_v2

        # 相关节点数，各自累加1次
        if v1 in v_table2:
            v_table2[v1] += 1
        else:
            v_table2[v1] = 1

        if v2 in v_table2:
            v_table2[v2] += 1
        else:
            v_table2[v2] = 1

    # 顶点表2 key-value交换，并按节点数排序
    v_t2_rank = v_table2.copy()

    # v_table2排个序，做调试参考
    v_t2_ranker = sorted(v_table2.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    # 初始化，颜色表，key：每个顶点， value：颜色
    # 初始化，相邻颜色表，key：顶点， value：相邻节点颜色set?
    t_color = {}
    t_adj_color = {}

    # 按节点数 从多到少，给相邻节点赋值（颜色）
    # 每一轮结束，更新节点的相邻关系，重新开始
    while len(v_t2_rank) > 0:
        vertice = max(v_t2_rank, key=lambda x: v_t2_rank[x])
        # 取相邻节点的颜色集合（根据相邻颜色，先给自己赋值，并记录颜色）
        if vertice in t_adj_color:
            v_adj_color = t_adj_color[vertice]
        else:
            v_adj_color = set()

        # 默认自身颜色是0
        v_color = 0

        # 遍历寻找最小自然数（相邻节点未使用的最小颜色）
        for i in range(0, len(v_adj_color) + 2):
            if i not in v_adj_color:
                v_color = i
                break

        # 记录下自身的颜色
        t_color[vertice] = v_color

        # 把自己的颜色，更新到相邻节点的“相邻节点颜色set”中
        # 取相邻节点，遍历
        adj_v_list = v_table1[vertice]
        for adj_v in adj_v_list:

            # 取相邻节点的“相邻节点颜色set”
            # 如果相邻节点尚未赋值，则添加进对方的“相邻节点颜色set”中
            if adj_v not in t_color:
                if adj_v in t_adj_color:
                    adj_color_set = t_adj_color[adj_v]
                else:
                    adj_color_set = set()

                adj_color_set.add(v_color)
                t_adj_color[adj_v] = adj_color_set # TODO 这个需要吗？

            # 更新v_table2（节点数）表格
            if adj_v in v_t2_rank:
                v_t2_rank[adj_v] -= 1

        # 移除当前key
        v_t2_rank.pop(vertice)

    # 拼接结果
    solution = []
    solution_set = set()
    for v in sorted(t_color):
        solution.append(t_color[v])
        solution_set.add(t_color[v])

    num_colors = len(solution_set)

    return num_colors, solution

# 1.node_count: 50,edge_count: 350 （7 point：8） 7 （10 point：6）
# 2.node_count: 70,edge_count: 1678 （7 point：20） 20 （10 point：17）
# 3.node_count: 100,edge_count: 2502 （7 point：21） 19 （10 point：16）
# 4.node_count: 250,edge_count: 28046 （7 point：95） 94 （10 point：78）
# 5.node_count: 500,edge_count: 12565 （7 point：18） 17 （10 point：16）
# 6.node_count: 1000,edge_count: 249482 （7 point：124） 119 （10 point：100）
# 相比CP_2：在value值相同时，增加了对key值的排序，key小的优先（原因：存在大量value值相同的key）
def CP_3(node_count, edge_count, edges):

    # 顶点表1 key：顶点， value：表：相关的顶点
    # 顶点表2 key：顶点， value：节点数
    v_table1 = {}
    v_table2 = {}
    for edge in edges:
        v1, v2 = edge[0], edge[1]
        t1_v1, t1_v2 = [], [] # 相关节点list

        # 从顶点表1、2中取2个顶点对应的子表
        if v1 in v_table1:
            t1_v1 = v_table1[v1]
        if v2 in v_table1:
            t1_v2 = v_table1[v2]

        # 互相添加到对方的相关节点list中
        t1_v1.append(v2)
        t1_v2.append(v1)

        # 保存相关节点list到总表
        v_table1[v1] = t1_v1
        v_table1[v2] = t1_v2

        # 相关节点数，各自累加1次
        if v1 in v_table2:
            v_table2[v1] += 1
        else:
            v_table2[v1] = 1

        if v2 in v_table2:
            v_table2[v2] += 1
        else:
            v_table2[v2] = 1

    # 顶点表2 key-value交换，并按节点数排序
    v_t2_rank = v_table2.copy()

    # v_table2排个序，做调试参考
    # v_t2_ranker = sorted(v_table2.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)

    # 初始化，颜色表，key：每个顶点， value：颜色
    # 初始化，相邻颜色表，key：顶点， value：相邻节点颜色set?
    t_color = {}
    t_adj_color = {}

    # 按节点数 从多到少，给相邻节点赋值（颜色）
    # 每一轮结束，更新节点的相邻关系，重新开始
    while len(v_t2_rank) > 0:
        v_t2_ranker = sorted(v_t2_rank.items(), key=lambda kv: (kv[1], -kv[0]), reverse=True)
        vertice = v_t2_ranker[0][0]
        # 取相邻节点的颜色集合（根据相邻颜色，先给自己赋值，并记录颜色）
        if vertice in t_adj_color:
            v_adj_color = t_adj_color[vertice]
        else:
            v_adj_color = set()

        # 默认自身颜色是0
        v_color = 0

        # 遍历寻找最小自然数（相邻节点未使用的最小颜色）
        for i in range(0, len(v_adj_color) + 2):
            if i not in v_adj_color:
                v_color = i
                break

        # 记录下自身的颜色
        t_color[vertice] = v_color

        # 把自己的颜色，更新到相邻节点的“相邻节点颜色set”中
        # 取相邻节点，遍历
        adj_v_list = v_table1[vertice]
        for adj_v in adj_v_list:

            # 取相邻节点的“相邻节点颜色set”
            # 如果相邻节点尚未赋值，则添加进对方的“相邻节点颜色set”中
            if adj_v not in t_color:
                if adj_v in t_adj_color:
                    adj_color_set = t_adj_color[adj_v]
                else:
                    adj_color_set = set()
                    t_adj_color[adj_v] = adj_color_set # （这个需要吗？） 是的，需要的

                adj_color_set.add(v_color)
                # t_adj_color[adj_v] = adj_color_set # （这个需要吗？） 不需要，value是set，此次是引用，修改引用的内容

            # 更新v_table2（节点数）表格
            if adj_v in v_t2_rank:
                v_t2_rank[adj_v] -= 1

        # 移除当前key
        v_t2_rank.pop(vertice)

    # 拼接结果
    solution = []
    solution_set = set()
    for v in sorted(t_color):
        solution.append(t_color[v])
        solution_set.add(t_color[v])

    num_colors = len(solution_set)

    return num_colors, solution

import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

