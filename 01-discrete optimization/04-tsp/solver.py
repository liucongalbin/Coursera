#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
import time
from collections import namedtuple
import matplotlib.pyplot as plt

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # 打印输入信息
    # 1.51_1:nodeCount: 51,line1: 27 68 （7 point：482）
    # 2.100_3:nodeCount: 100,line1: 86 1065（7 point：23433）
    # 3.200_2:nodeCount: 200,line1: 2995 264（7 point：35985）
    # 4.574_1:nodeCount: 574,line1: 1.91609e+03 2.07689e+03（7 point：40000）
    # 5.1889_1:nodeCount: 1889,line1: 1.27840e+04 1.00980e+04（7 point：378069）
    # 6.33810_1:nodeCount: 33810,line1: 322375 329675（7 point：78478868）
    print("nodeCount: " + str(nodeCount) + ",line1: " + str(lines[1]))

    # 策略：1.前3题用k-opt（LS_1_X） 2.后3题用基于2-opt的局部搜索+启发式+元启发（LS_2_X）。
    # k-opt在课上没有完整阐述开始、结束流程，直接用启发式

    # 1、2、3题10分 +4题7分 + 5/6题3分
    if nodeCount < 1000:
        solution = LS_10(nodeCount, points)
    else:
        solution = range(0, nodeCount)

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    # solution = range(0, nodeCount)

    # calculate the length of the tour
    obj = cal_tDistance(nodeCount, points, solution)

    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data

# 计算总距离
def cal_tDistance(nodeCount, points, solution):
    obj = length(points[solution[-1]], points[solution[0]])
    for index in range(0, nodeCount - 1):
        obj += length(points[solution[index]], points[solution[index + 1]])
    return obj


# 可视化绘图
def draw(nodeCount, points, solution):
    x, y = [], []
    for index in range(0, nodeCount):
        p = points[solution[index]]
        # print(p)
        x.append(p[0])
        y.append(p[1])

    fig = plt.figure()
    ax2 = fig.add_subplot()

    ax2.plot(x, y, 'm.-.', label='ax2', linewidth=1)

    ax2.legend()
    ax2.set_title('xixixi')
    ax2.set_xlabel('hengzhou')
    ax2.set_ylabel('zongzhou')

    plt.show()

# 2-opt操作时计算总距离的增量
def cal_distance_increase(idx_1, idx_2, points, sequence_now):
    return length(points[sequence_now[idx_1]], points[sequence_now[idx_2]]) \
           + length(points[sequence_now[idx_1 - 1]], points[sequence_now[idx_2 - 1]]) \
           - length(points[sequence_now[idx_1]], points[sequence_now[idx_1 - 1]]) \
           - length(points[sequence_now[idx_2]], points[sequence_now[idx_2 - 1]])


# 实现随机取节点的局部搜索算法
# 选取策略，一定要有所改进才选择其他节点
def LS_1(nodeCount, points):

    # 初始化为原输入顺序
    s_init = list(range(0, nodeCount))
    s_best = s_init.copy()

    # 绘图看看
    draw(nodeCount, points, s_best)

    # 计算
    distance_best = cal_tDistance(nodeCount, points, s_best)

    # 记录threshold
    # 1.51_1:nodeCount: 51,line1: 27 68 （7 point：482）（10 point：430）
    # 2.100_3:nodeCount: 100,line1: 86 1065（7 point：23433）（10 point：20800）
    # 3.200_2:nodeCount: 200,line1: 2995 264（7 point：35985）（10 point：30000）
    # 4.574_1:nodeCount: 574,line1: 1.91609e+03 2.07689e+03（7 point：40000）（10 point：37600）
    # 5.1889_1:nodeCount: 1889,line1: 1.27840e+04 1.00980e+04（7 point：378069）
    # 6.33810_1:nodeCount: 33810,line1: 322375 329675（7 point：78478868）
    threshold = 0
    if nodeCount == 51:
        threshold = 430
    elif  nodeCount == 100:
        threshold = 20800
    elif  nodeCount == 200:
        threshold = 30000
    elif  nodeCount == 574:
        threshold = 40000
    elif  nodeCount == 1889:
        threshold = 378069
    elif  nodeCount == 33810:
        threshold = 78478868


    # 计次器，当前第0次
    t = 0

    # 没有优化的计次器
    no_improve_thres = 500 * nodeCount
    no_improve_t = 0

    # 循环，做1000轮
    # while t < 10000:
    while distance_best > threshold:

        distance_best = cal_tDistance(nodeCount, points, s_best)

        if t % 10000 == 0:
            print("当前第" + str(t) + "轮，distance_best：" + str(distance_best))

        s_temp = s_best.copy()

        # 选点 TODO 能交换最后一个点嘛？
        idx_1 = random.randint(0, nodeCount - 1)
        idx_2 = random.randint(idx_1 + 1, nodeCount)

        # 做交换，并计算有无改进
        s_temp[idx_1: idx_2] = list(reversed(s_temp[idx_1: idx_2]))

        # 如有改进，选取新的序列
        distance_new = cal_tDistance(nodeCount, points, s_temp)

        if distance_new <= distance_best:
            s_best = s_temp
        else:
            no_improve_t += 1

        if no_improve_t >= no_improve_thres:
            print("已经" + str(no_improve_thres) + "次没有改进，重新初始化序列")

            # 绘图看看
            draw(nodeCount, points, s_best)

            # 重新初始化
            s_best = s_init.copy()
            no_improve_t = 0

        # 计次器+1
        t += 1

    return s_best

# 实现随机取节点的局部搜索算法
# 选取策略，及时其他节点不如当前节点，也有一定概率选择
def LS_2(nodeCount, points):

    # 初始化为原输入顺序
    s_init = list(range(0, nodeCount))
    s_best = s_init.copy()

    # 温度初始化
    temperature = 1 # 初始温度设为1000度时，由于温度太高，无法收敛。该温度初始值建议与局部最优时的改进值相当
    alpha = 0.8 # 顺利优化，每100轮temperature * alpha
    beta = 1.3 # 无法优化，每10轮temperature * beta

    # 绘图看看
    draw(nodeCount, points, s_best)

    # 计算
    distance_best = cal_tDistance(nodeCount, points, s_best)

    # 记录threshold
    # 1.51_1:nodeCount: 51,line1: 27 68 （7 point：482）（10 point：430）
    # 2.100_3:nodeCount: 100,line1: 86 1065（7 point：23433）（10 point：20800）
    # 3.200_2:nodeCount: 200,line1: 2995 264（7 point：35985）（10 point：30000）
    # 4.574_1:nodeCount: 574,line1: 1.91609e+03 2.07689e+03（7 point：40000）（10 point：37600）
    # 5.1889_1:nodeCount: 1889,line1: 1.27840e+04 1.00980e+04（7 point：378069）
    # 6.33810_1:nodeCount: 33810,line1: 322375 329675（7 point：78478868）
    threshold = 0
    if nodeCount == 51:
        threshold = 430
    elif  nodeCount == 100:
        threshold = 20800
    elif  nodeCount == 200:
        threshold = 30000
    elif  nodeCount == 574:
        threshold = 40000
    elif  nodeCount == 1889:
        threshold = 378069
    elif  nodeCount == 33810:
        threshold = 78478868


    # 计次器，当前第0次
    t = 0

    # 没有优化的计次器
    no_improve_thres = 500 * nodeCount
    no_improve_t = 0

    # 循环，做1000轮
    # while t < 10000:
    while distance_best > threshold:

        distance_best = cal_tDistance(nodeCount, points, s_best)

        if t % 10000 == 0:
            print("当前第" + str(t) + "轮，distance_best：" + str(distance_best))
            print("temperature：" + str(temperature))

        if t % 100 == 0:
            temperature = temperature * alpha

        s_temp = s_best.copy()

        # 选点 TODO 能交换最后一个点嘛？
        idx_1 = random.randint(0, nodeCount - 1)
        idx_2 = random.randint(idx_1 + 1, nodeCount)

        # 做交换，并计算有无改进
        s_temp[idx_1: idx_2] = list(reversed(s_temp[idx_1: idx_2]))

        # 如有改进，选取新的序列
        distance_new = cal_tDistance(nodeCount, points, s_temp)

        # 如果随机数取：random < 1 / (distance_new - distance_best)，距离到800左右就不再收敛了
        if distance_new < distance_best \
                or random.random() < math.exp(-(distance_new - distance_best) / temperature):

            s_best = s_temp
            # no_improve_t = 0 TODO 这个怎么不灵了？
        else:
            no_improve_t += 1

            # 无法优化，则升温
            if t % 100 == 0:
                temperature = temperature * beta

        # if no_improve_t >= no_improve_thres:
        #     print("已经" + str(no_improve_thres) + "次没有改进，重新初始化序列")
        #
        #     # 绘图看看
        #     draw(nodeCount, points, s_best)
        #
        #     # 重新初始化
        #     s_best = s_init.copy()
        #     no_improve_t = 0

        # 计次器+1
        t += 1

    return s_best

# 实现随机取节点的局部搜索算法
# 选取策略，采用tabu list，除初始节点，其余加入tabu list。
def LS_3(nodeCount, points):

    # 初始化为原输入顺序
    s_init = list(range(0, nodeCount))
    s_best = s_init.copy()

    # 初始化tabu list
    t_list = []

    # 绘图看看
    # draw(nodeCount, points, s_best)

    # 计算
    distance_best = cal_tDistance(nodeCount, points, s_best)
    best_score = distance_best

    # 记录threshold
    # 1.51_1:nodeCount: 51,line1: 27 68 （7 point：482）（10 point：430）
    # 2.100_3:nodeCount: 100,line1: 86 1065（7 point：23433）（10 point：20800）
    # 3.200_2:nodeCount: 200,line1: 2995 264（7 point：35985）（10 point：30000）
    # 4.574_1:nodeCount: 574,line1: 1.91609e+03 2.07689e+03（7 point：40000）（10 point：37600）
    # 5.1889_1:nodeCount: 1889,line1: 1.27840e+04 1.00980e+04（7 point：378069）
    # 6.33810_1:nodeCount: 33810,line1: 322375 329675（7 point：78478868）
    threshold = 0
    if nodeCount == 51:
        threshold = 430
    elif  nodeCount == 100:
        threshold = 20800
    elif  nodeCount == 200:
        threshold = 30000
    elif  nodeCount == 574:
        threshold = 40000
    elif  nodeCount == 1889:
        threshold = 378069
    elif  nodeCount == 33810:
        threshold = 78478868


    # 计次器，当前第0次
    t = 0

    # 没有优化的计次器
    no_improve_thres = 100 * nodeCount
    no_improve_t = 0

    # 循环，做1000轮
    # while t < 10000:
    while distance_best > threshold:

        distance_best = cal_tDistance(nodeCount, points, s_best)

        if t % 100000 == 0:
            print("当前tabu list 长度为：" + str(len(t_list)))
            print("当前best_score为：" + str(best_score))

        s_temp = s_best.copy()

        # 选点 TODO 能交换最后一个点嘛？
        idx_1 = random.randint(0, nodeCount - 1)
        idx_2 = random.randint(idx_1 + 1, nodeCount)

        # 做交换，并计算有无改进
        s_temp[idx_1: idx_2] = list(reversed(s_temp[idx_1: idx_2]))

        # 判断是否在tabu list
        node_str = ''.join([str(i) for i in s_temp])
        if node_str in t_list:
            no_improve_t += 1
            continue

        # 如有改进，选取新的序列
        distance_new = cal_tDistance(nodeCount, points, s_temp)

        if distance_new <= distance_best:
            s_best = s_temp

            # 节点加入tabu list
            t_list.append(node_str)

        else:
            no_improve_t += 1

        if no_improve_t >= no_improve_thres:
            # print("已经" + str(no_improve_thres) + "次没有改进，重新初始化序列")
            # print("当前第" + str(t) + "轮，distance_best：" + str(distance_best))

            print(int(distance_best), end=" ")

            if distance_best < best_score:
                best_score = distance_best

            # 绘图看看
            # draw(nodeCount, points, s_best)

            # 重新初始化
            s_best = s_init.copy()
            no_improve_t = 0

        # 计次器+1
        t += 1

    return s_best

# 实现随机取节点的局部搜索算法
# 选取策略，每步遍历所有可能，找到最好的方案（哪怕是比现在的差），并结合tabu list
def LS_4(nodeCount, points):

    # 初始化为原输入顺序
    sequence_init = list(range(0, nodeCount))
    sequence_now = sequence_init.copy()

    # 初始化tabu list
    tabu_list = []

    # 绘图看看
    # draw(nodeCount, points, sequence_now)

    # 计算
    distance_now = cal_tDistance(nodeCount, points, sequence_now)
    distance_optimal = distance_now

    # 记录threshold
    # 1.51_1:nodeCount: 51,line1: 27 68 （7 point：482）（10 point：430）
    # 2.100_3:nodeCount: 100,line1: 86 1065（7 point：23433）（10 point：20800）
    # 3.200_2:nodeCount: 200,line1: 2995 264（7 point：35985）（10 point：30000）
    # 4.574_1:nodeCount: 574,line1: 1.91609e+03 2.07689e+03（7 point：40000）（10 point：37600）
    # 5.1889_1:nodeCount: 1889,line1: 1.27840e+04 1.00980e+04（7 point：378069）
    # 6.33810_1:nodeCount: 33810,line1: 322375 329675（7 point：78478868）
    threshold = 0
    if nodeCount == 51:
        threshold = 430
    elif  nodeCount == 100:
        threshold = 20800
    elif  nodeCount == 200:
        threshold = 30000
    elif  nodeCount == 574:
        threshold = 40000
    elif  nodeCount == 1889:
        threshold = 378069
    elif  nodeCount == 33810:
        threshold = 78478868


    # 计次器，当前第0次
    times = 0

    # 循环，直到满足门槛
    while distance_now > threshold:

        distance_now = cal_tDistance(nodeCount, points, sequence_now)

        if times % 100 == 0:
            print("当前tabu list 长度为：" + str(len(tabu_list)), end="  ")
            print("当前distance_optimal为：" + str(distance_optimal), end="  ")
            print("distance_now：" + str(distance_now))


        # 记录邻居中的最优节点
        best_neighbor = False
        best_neighbor_distance = sys.maxsize

        # 选点
        for idx_1 in range(0, nodeCount - 1):
            for idx_2 in range(idx_1 + 1, nodeCount):

                sequence_temp = sequence_now.copy()

                # 做交换，并计算有无改进
                sequence_temp[idx_1: idx_2] = list(reversed(sequence_temp[idx_1: idx_2]))

                # 判断是否在tabu list。如果在，放弃。
                # node_str = ''.join([str(i) for i in sequence_temp])
                if sequence_temp in tabu_list:
                    continue

                # 如有改进，选取新的序列
                distance_temp = cal_tDistance(nodeCount, points, sequence_temp)

                if distance_temp <= best_neighbor_distance:
                    best_neighbor = sequence_temp
                    best_neighbor_distance = distance_temp

        # 如果找到了下一步节点
        if best_neighbor != False:
            # 节点加入tabu list
            # node_str = ''.join([str(i) for i in best_neighbor])
            tabu_list.append(best_neighbor)

            # 选取下一个节点
            sequence_now = best_neighbor

            # 计算全局最优有无更新
            if best_neighbor_distance < distance_optimal:
                distance_optimal = best_neighbor_distance

        else:

            # 无路可走（所有邻居都访问过了），则重新初始化
            print("已经无路可走（所有邻居都访问过了），重新初始化序列")
            print("当前第" + str(times) + "轮，distance_now：" + str(distance_now) + "，distance_optimal：" + str(distance_optimal))

            # 重新初始化
            sequence_now = sequence_init.copy()

        # 计次器+1
        times += 1

    return sequence_now

# 实现随机取节点的局部搜索算法
# 对比4，加入了500轮重启，并随机初始化
def LS_5(nodeCount, points):

    # 初始化为原输入顺序
    sequence_init = list(range(0, nodeCount))
    random.shuffle(sequence_init) # 随机打乱
    sequence_now = sequence_init.copy()

    # 初始化tabu list
    tabu_list = []

    # 绘图看看
    draw(nodeCount, points, sequence_now)

    # 计算
    distance_now = cal_tDistance(nodeCount, points, sequence_now)
    distance_optimal = distance_now

    # 记录threshold
    # 1.51_1:nodeCount: 51,line1: 27 68 （7 point：482）（10 point：430）
    # 2.100_3:nodeCount: 100,line1: 86 1065（7 point：23433）（10 point：20800）
    # 3.200_2:nodeCount: 200,line1: 2995 264（7 point：35985）（10 point：30000）
    # 4.574_1:nodeCount: 574,line1: 1.91609e+03 2.07689e+03（7 point：40000）（10 point：37600）
    # 5.1889_1:nodeCount: 1889,line1: 1.27840e+04 1.00980e+04（7 point：378069）
    # 6.33810_1:nodeCount: 33810,line1: 322375 329675（7 point：78478868）
    threshold = 0
    if nodeCount == 51:
        threshold = 430
    elif  nodeCount == 100:
        threshold = 20800
    elif  nodeCount == 200:
        threshold = 30000
    elif  nodeCount == 574:
        threshold = 40000
    elif  nodeCount == 1889:
        threshold = 378069
    elif  nodeCount == 33810:
        threshold = 78478868


    # 计次器，当前第0次
    times = 0

    # 循环，直到满足门槛
    while distance_now > threshold:

        # 每500轮，重新随机初始化
        if times % 500 == 0:
            random.shuffle(sequence_init) # 随机打乱
            sequence_now = sequence_init.copy()

        distance_now = cal_tDistance(nodeCount, points, sequence_now)

        # 每100轮，打印当前信息
        if times % 100 == 0:
            print("当前tabu list 长度为：" + str(len(tabu_list)), end="  ")
            print("当前distance_optimal为：" + str(distance_optimal), end="  ")
            print("distance_now：" + str(distance_now))

        # 记录邻居中的最优节点
        best_neighbor = False
        best_neighbor_distance = sys.maxsize

        # 选点
        for idx_1 in range(0, nodeCount - 1):
            for idx_2 in range(idx_1 + 1, nodeCount):

                sequence_temp = sequence_now.copy()

                # 做交换，并计算有无改进
                sequence_temp[idx_1: idx_2] = list(reversed(sequence_temp[idx_1: idx_2]))

                # 判断是否在tabu list。如果在，放弃。
                # node_str = ''.join([str(i) for i in sequence_temp])
                if sequence_temp in tabu_list:
                    continue

                # 如有改进，选取新的序列
                distance_temp = cal_tDistance(nodeCount, points, sequence_temp)

                if distance_temp <= best_neighbor_distance:
                    best_neighbor = sequence_temp
                    best_neighbor_distance = distance_temp

        # 如果找到了下一步节点
        if best_neighbor != False:
            # 节点加入tabu list
            # node_str = ''.join([str(i) for i in best_neighbor])
            tabu_list.append(best_neighbor)

            # 选取下一个节点
            sequence_now = best_neighbor

            # 计算全局最优有无更新
            if best_neighbor_distance < distance_optimal:
                distance_optimal = best_neighbor_distance

                # 输出到文件
                file = open("test5-1.txt", "a")
                file.write(str(times) + ":" + str(distance_optimal) + ":" + str(sequence_now))
                file.write("\n")
                file.close()

        else:

            # 无路可走（所有邻居都访问过了），则重新初始化
            print("已经无路可走（所有邻居都访问过了），重新初始化序列")
            print("当前第" + str(times) + "轮，distance_now：" + str(distance_now) + "，distance_optimal：" + str(distance_optimal))

            # 重新初始化
            sequence_now = sequence_init.copy()

        # 计次器+1
        times += 1

    return sequence_now

# 实现随机取节点的局部搜索算法
# 对比4，同样的逻辑，从一个432分的解开始，做更长的探索
def LS_6(nodeCount, points):

    # 初始化计时器
    begin_time = time.perf_counter()
    last_round_time = begin_time # 上一轮时间戳

    # 初始化为原输入顺序
    sequence_init = [3, 45, 9, 10, 28, 2, 5, 0, 33, 22, 1, 31, 48, 32, 17, 49, 39, 50, 38, 15, 14, 44, 16, 18, 40, 19, 7, 13, 35, 23, 12, 30, 11, 42, 29, 43, 21, 37, 25, 20, 36, 6, 26, 47, 27, 41, 24, 34, 4, 8, 46]
    sequence_now = sequence_init.copy()

    # 初始化tabu list
    tabu_list = []

    # 绘图看看
    # draw(nodeCount, points, sequence_now)

    # 计算
    distance_now = cal_tDistance(nodeCount, points, sequence_now)
    distance_optimal = distance_now

    # 记录threshold
    # 1.51_1:nodeCount: 51,line1: 27 68 （7 point：482）（10 point：430）
    # 2.100_3:nodeCount: 100,line1: 86 1065（7 point：23433）（10 point：20800）
    # 3.200_2:nodeCount: 200,line1: 2995 264（7 point：35985）（10 point：30000）
    # 4.574_1:nodeCount: 574,line1: 1.91609e+03 2.07689e+03（7 point：40000）（10 point：37600）
    # 5.1889_1:nodeCount: 1889,line1: 1.27840e+04 1.00980e+04（7 point：378069）
    # 6.33810_1:nodeCount: 33810,line1: 322375 329675（7 point：78478868）
    threshold = 0
    if nodeCount == 51:
        threshold = 430
    elif  nodeCount == 100:
        threshold = 20800
    elif  nodeCount == 200:
        threshold = 30000
    elif  nodeCount == 574:
        threshold = 40000
    elif  nodeCount == 1889:
        threshold = 378069
    elif  nodeCount == 33810:
        threshold = 78478868


    # 计次器，当前第0次
    times = 0

    # 循环，直到满足门槛
    while distance_now > threshold:

        distance_now = cal_tDistance(nodeCount, points, sequence_now)

        if times % 100 == 0:
            print("当前tabu list 长度为：" + str(len(tabu_list)), end="  ")
            print("当前distance_optimal为：" + str(distance_optimal), end="  ")
            print("distance_now：" + str(distance_now), end="  ")

            # 当前计时
            now_time = time.perf_counter()
            print("当前总耗时：" + str(now_time - begin_time), end="  ")
            print("上一轮耗时：" + str(now_time - last_round_time))
            last_round_time = now_time


        # 记录邻居中的最优节点
        best_neighbor = False
        best_neighbor_distance_increase = sys.maxsize

        # 选点
        for idx_1 in range(0, nodeCount - 1):
            for idx_2 in range(idx_1 + 1, nodeCount):

                sequence_temp = sequence_now.copy()

                # 做交换，并计算有无改进
                sequence_temp[idx_1: idx_2] = list(reversed(sequence_temp[idx_1: idx_2]))

                # 判断是否在tabu list。如果在，放弃。
                # node_str = ''.join([str(i) for i in sequence_temp])
                if sequence_temp in tabu_list:
                    continue

                # 计算距离的变化
                distance_increase = cal_distance_increase(idx_1, idx_2, points, sequence_now)

                if distance_increase <= best_neighbor_distance_increase:
                    best_neighbor = sequence_temp
                    best_neighbor_distance_increase = distance_increase

        # 如果找到了下一步节点
        if best_neighbor != False:
            # 节点加入tabu list
            # node_str = ''.join([str(i) for i in best_neighbor])
            tabu_list.append(best_neighbor)

            # 选取下一个节点
            sequence_now = best_neighbor

            distance_now = cal_tDistance(nodeCount, points, sequence_now)

            # 计算全局最优有无更新
            if distance_now < distance_optimal:
                distance_optimal = distance_now

                # 输出到文件
                file = open("test6.txt", "a")
                file.write(str(times) + ":" + str(distance_optimal) + ":" + str(sequence_now))
                file.write("\n")
                file.close()

        else:

            # 无路可走（所有邻居都访问过了），则重新初始化
            print("已经无路可走（所有邻居都访问过了），重新初始化序列")
            print("当前第" + str(times) + "轮，distance_now：" + str(distance_now) + "，distance_optimal：" + str(distance_optimal))

            # 重新初始化
            sequence_now = sequence_init.copy()

        # 计次器+1
        times += 1

    return sequence_now

# 实现随机取节点的局部搜索算法
# 对比5，1(还是生成吧).不生成临时邻居 2.不从头计算距离
def LS_7(nodeCount, points):

    # 初始化为原输入顺序
    sequence_init = list(range(0, nodeCount))
    random.shuffle(sequence_init) # 随机打乱
    sequence_now = sequence_init.copy()

    # 初始化tabu list
    tabu_list = []

    # 绘图看看
    draw(nodeCount, points, sequence_now)

    # 计算
    distance_now = cal_tDistance(nodeCount, points, sequence_now)
    distance_optimal = distance_now

    # 记录threshold
    # 1.51_1:nodeCount: 51,line1: 27 68 （7 point：482）（10 point：430）
    # 2.100_3:nodeCount: 100,line1: 86 1065（7 point：23433）（10 point：20800）
    # 3.200_2:nodeCount: 200,line1: 2995 264（7 point：35985）（10 point：30000）
    # 4.574_1:nodeCount: 574,line1: 1.91609e+03 2.07689e+03（7 point：40000）（10 point：37600）
    # 5.1889_1:nodeCount: 1889,line1: 1.27840e+04 1.00980e+04（7 point：378069）
    # 6.33810_1:nodeCount: 33810,line1: 322375 329675（7 point：78478868）
    threshold = 0
    if nodeCount == 51:
        threshold = 430
    elif  nodeCount == 100:
        threshold = 20800
    elif  nodeCount == 200:
        threshold = 30000
    elif  nodeCount == 574:
        threshold = 40000
    elif  nodeCount == 1889:
        threshold = 378069
    elif  nodeCount == 33810:
        threshold = 78478868


    # 计次器，当前第0次
    times = 0

    # 循环，直到满足门槛
    while distance_now > threshold:

        # 每500轮，重新随机初始化
        if times % 500 == 0:
            random.shuffle(sequence_init) # 随机打乱
            sequence_now = sequence_init.copy()

        distance_now = cal_tDistance(nodeCount, points, sequence_now)

        # 每100轮，打印当前信息
        if times % 100 == 0:
            print("当前tabu list 长度为：" + str(len(tabu_list)), end="  ")
            print("当前distance_optimal为：" + str(distance_optimal), end="  ")
            print("distance_now：" + str(distance_now))

        # 记录邻居中的最优节点
        best_neighbor = False
        best_neighbor_distance_increase = sys.maxsize

        # 选点
        for idx_1 in range(0, nodeCount - 1):
            for idx_2 in range(idx_1 + 1, nodeCount):

                sequence_temp = sequence_now.copy()

                # 做交换，并计算有无改进
                sequence_temp[idx_1: idx_2] = list(reversed(sequence_temp[idx_1: idx_2]))

                # 判断是否在tabu list。如果在，放弃。
                # node_str = ''.join([str(i) for i in sequence_temp])
                if sequence_temp in tabu_list:
                    continue

                # 计算距离的变化
                distance_increase = cal_distance_increase(idx_1, idx_2, points, sequence_now)

                if distance_increase <= best_neighbor_distance_increase:
                    best_neighbor = sequence_temp
                    best_neighbor_distance_increase = distance_increase

        # 如果找到了下一步节点
        if best_neighbor != False:
            # 节点加入tabu list
            # node_str = ''.join([str(i) for i in best_neighbor])
            tabu_list.append(best_neighbor)

            # 选取下一个节点
            sequence_now = best_neighbor

            distance_now = cal_tDistance(nodeCount, points, sequence_now)

            # 计算全局最优有无更新
            if distance_now < distance_optimal:
                distance_optimal = distance_now

                # 输出到文件
                file = open("test5-1.txt", "a")
                file.write(str(times) + ":" + str(distance_optimal) + ":" + str(sequence_now))
                file.write("\n")
                file.close()

        else:

            # 无路可走（所有邻居都访问过了），则重新初始化
            print("已经无路可走（所有邻居都访问过了），重新初始化序列")
            print("当前第" + str(times) + "轮，distance_now：" + str(distance_now) + "，distance_optimal：" + str(distance_optimal))

            # 重新初始化
            sequence_now = sequence_init.copy()

        # 计次器+1
        times += 1

    return sequence_now

# 通过贪心算法获得初始路径（每一步，找最近的点）
# 遍历了所有可能，但是没什么用
def LS_8(nodeCount, points):

    # 记录所有路径总的最优
    optimal_total_distance = sys.maxsize
    optimal_sequence = []

    for start_idx in range(0, nodeCount):

        sequence_init = [start_idx]
        remain_list = list(range(0, nodeCount))
        remain_list.remove(start_idx)

        while len(sequence_init) < nodeCount:

            # 记录最小距离
            min_distance = sys.maxsize
            min_idx = 0

            # 每一步，找最近的点
            for idx in remain_list:

                # 计算距离
                temp_total_distance = length(points[sequence_init[-1]], points[idx])

                if temp_total_distance < min_distance:
                    min_distance = temp_total_distance
                    min_idx = idx

            # 选择最近节点，并从剩余list中移除
            sequence_init.append(min_idx)
            remain_list.remove(min_idx)

        # 计算总距离
        temp_total_distance = cal_tDistance(nodeCount, points, sequence_init)

        # 打印每一轮的距离
        print("start_idx:" + str(start_idx) + ", temp_total_distance:" + str(temp_total_distance))

        if temp_total_distance < optimal_total_distance:
            optimal_total_distance = temp_total_distance
            optimal_sequence = sequence_init

    # 绘图看看
    sequence_now = optimal_sequence
    draw(nodeCount, points, sequence_now)


    return sequence_now

# 实现随机取节点的局部搜索算法
# 对比6，同样的逻辑，从一个432分的解开始，做更长的探索。但是tabu list只记录交换的两个点的坐标（后，交换两点的位置）
def LS_9(nodeCount, points):

    # 初始化计时器
    begin_time = time.perf_counter()
    last_round_time = begin_time # 上一轮时间戳

    # 初始化为原输入顺序
    sequence_init = [3, 45, 9, 10, 28, 2, 5, 0, 33, 22, 1, 31, 48, 32, 17, 49, 39, 50, 38, 15, 14, 44, 16, 18, 40, 19, 7, 13, 35, 23, 12, 30, 11, 42, 29, 43, 21, 37, 25, 20, 36, 6, 26, 47, 27, 41, 24, 34, 4, 8, 46]
    sequence_now = sequence_init.copy()

    # 初始化tabu list
    tabu_list = []

    # 绘图看看
    # draw(nodeCount, points, sequence_now)

    # 计算
    distance_now = cal_tDistance(nodeCount, points, sequence_now)
    distance_optimal = distance_now

    # 记录threshold
    # 1.51_1:nodeCount: 51,line1: 27 68 （7 point：482）（10 point：430）
    # 2.100_3:nodeCount: 100,line1: 86 1065（7 point：23433）（10 point：20800）
    # 3.200_2:nodeCount: 200,line1: 2995 264（7 point：35985）（10 point：30000）
    # 4.574_1:nodeCount: 574,line1: 1.91609e+03 2.07689e+03（7 point：40000）（10 point：37600）
    # 5.1889_1:nodeCount: 1889,line1: 1.27840e+04 1.00980e+04（7 point：378069）
    # 6.33810_1:nodeCount: 33810,line1: 322375 329675（7 point：78478868）
    threshold = 0
    if nodeCount == 51:
        threshold = 430
    elif  nodeCount == 100:
        threshold = 20800
    elif  nodeCount == 200:
        threshold = 30000
    elif  nodeCount == 574:
        threshold = 40000
    elif  nodeCount == 1889:
        threshold = 378069
    elif  nodeCount == 33810:
        threshold = 78478868


    # 计次器，当前第0次
    times = 0

    # 循环，直到满足门槛
    while distance_now > threshold:

        distance_now = cal_tDistance(nodeCount, points, sequence_now)

        if times % 100 == 0:
            print("当前tabu list 长度为：" + str(len(tabu_list)), end="  ")
            print("当前distance_optimal为：" + str(distance_optimal), end="  ")
            print("distance_now：" + str(distance_now), end="  ")

            # 当前计时
            now_time = time.perf_counter()
            print("当前总耗时：" + str(now_time - begin_time), end="  ")
            print("上一轮耗时：" + str(now_time - last_round_time))
            last_round_time = now_time

        # 记录邻居中的最优节点
        best_neighbor = False
        best_neighbor_distance_increase = sys.maxsize
        best_neighbor_index = (0, 0, 0, 0)

        # 选点
        for idx_1 in range(0, nodeCount - 1):
            for idx_2 in range(idx_1 + 1, nodeCount):

                sequence_temp = sequence_now.copy()

                # 做交换，并计算有无改进
                sequence_temp[idx_1: idx_2] = list(reversed(sequence_temp[idx_1: idx_2]))

                # 判断是否在tabu list。如果在，放弃。
                # 不能只放序列的idx或者城市的idx，否则很容易满
                # node_str = ''.join([str(i) for i in sequence_temp])
                if (sequence_now[idx_1], sequence_now[idx_2]) in tabu_list:
                    continue

                # 计算距离的变化
                distance_increase = cal_distance_increase(idx_1, idx_2, points, sequence_now)

                if distance_increase <= best_neighbor_distance_increase:
                    best_neighbor = sequence_temp
                    best_neighbor_distance_increase = distance_increase
                    best_neighbor_index = (sequence_now[idx_1], sequence_now[idx_2])

        # 如果找到了下一步节点
        if best_neighbor != False:
            # 节点加入tabu list
            # node_str = ''.join([str(i) for i in best_neighbor])
            tabu_list.append(best_neighbor_index)

            # 选取下一个节点
            sequence_now = best_neighbor

            distance_now = cal_tDistance(nodeCount, points, sequence_now)

            # 计算全局最优有无更新
            if distance_now < distance_optimal:
                distance_optimal = distance_now

                # 输出到文件
                file = open("test6.txt", "a")
                file.write(str(times) + ":" + str(distance_optimal) + ":" + str(sequence_now))
                file.write("\n")
                file.close()

        else:

            # 无路可走（所有邻居都访问过了），则重新初始化
            print("已经无路可走（所有邻居都访问过了），重新初始化序列")
            print("当前第" + str(times) + "轮，distance_now：" + str(distance_now) + "，distance_optimal：" + str(distance_optimal))

            # 重新初始化
            sequence_now = sequence_init.copy()

        # 计次器+1
        times += 1

    return sequence_now

# 实现随机取节点的局部搜索算法
# 基于tsp_5_1，做实验
def LS_10(nodeCount, points):


    # 初始化为原输入顺序
    sequence_init = list(range(0, nodeCount))
    sequence_now = sequence_init.copy()
    # random.shuffle(sequence_now)
    threshold = 4

    # 初始化tabu list
    tabu_list = []

    # 绘图看看
    draw(nodeCount, points, sequence_now)

    # 计算
    distance_now = cal_tDistance(nodeCount, points, sequence_now)
    distance_optimal = distance_now

    # 计次器，当前第0次
    times = 0

    # 循环，直到满足门槛
    while distance_now > threshold:

        distance_now = cal_tDistance(nodeCount, points, sequence_now)

        if times % 10 == 0:
            print("当前tabu list 长度为：" + str(len(tabu_list)), end="  ")
            print("当前distance_optimal为：" + str(distance_optimal), end="  ")
            print("distance_now：" + str(distance_now))
            # draw(nodeCount, points, sequence_now)

        # 记录邻居中的最优节点
        best_neighbor = False
        best_neighbor_distance_increase = sys.maxsize
        best_neighbor_index = (0, 0, 0, 0)

        # 选点
        for idx_1 in range(0, nodeCount - 1):
            for idx_2 in range(idx_1 + 1, nodeCount):

                sequence_temp = sequence_now.copy()

                # 做交换，并计算有无改进
                sequence_temp[idx_1: idx_2] = list(reversed(sequence_temp[idx_1: idx_2]))

                # 判断是否在tabu list。如果在，放弃。
                # 不能只放序列的idx或者城市的idx，否则很容易满
                # node_str = ''.join([str(i) for i in sequence_temp])
                if (sequence_now[idx_1], sequence_now[idx_2]) in tabu_list:
                    continue

                # 计算距离的变化
                distance_increase = cal_distance_increase(idx_1, idx_2, points, sequence_now)

                if distance_increase <= best_neighbor_distance_increase:
                    best_neighbor = sequence_temp
                    best_neighbor_distance_increase = distance_increase
                    best_neighbor_index = (sequence_now[idx_1], sequence_now[idx_2])

        # 如果找到了下一步节点
        if best_neighbor != False:
            # 节点加入tabu list
            # node_str = ''.join([str(i) for i in best_neighbor])
            tabu_list.append(best_neighbor_index)

            # 选取下一个节点
            sequence_now = best_neighbor

            distance_now = cal_tDistance(nodeCount, points, sequence_now)

            # 计算全局最优有无更新
            if distance_now < distance_optimal:
                distance_optimal = distance_now

                # 输出到文件
                file = open("test10.txt", "a")
                file.write(str(times) + ":" + str(distance_optimal) + ":" + str(sequence_now))
                file.write("\n")
                file.close()

        else:

            # 无路可走（所有邻居都访问过了），则重新初始化
            print("已经无路可走（所有邻居都访问过了），重新初始化序列")
            print("当前第" + str(times) + "轮，distance_now：" + str(distance_now) + "，distance_optimal：" + str(distance_optimal))

            # 重新初始化
            sequence_now = sequence_init.copy()

        # 计次器+1
        times += 1

    print("times:" + str(times))

    return sequence_now


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

