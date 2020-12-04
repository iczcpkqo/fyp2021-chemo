import random
import argparse
import numpy as np
import random
import math

class DataBox:
    def __init__(self):
        # 吸收率有哪些
        self.eats = []

        # 每个吸收率对应的平均时间
        self.avg_steps = []

        # 每个吸收率对应的运行组, 记录每一次运行成功所需要的step (每一组都是使用同一个吸收率运行很多次的结果)
        self.total_steps_group = []

        # 成功次数，运行总次数, 每一组存放了两个数据 [到达次数, 运行总次数]
        self.arrive_times = []

        # 每个吸收率对应的运行组的方差
        self.variance_steps = []

        # 每一个吸收率对应的运行组的成功率
        self.success_rate = []

        return

    # 增加一个吸收率
    def add_eat(self, eat):
        self.eats.append(eat)

    # 增加一个运行耗时
    def add_step(self, step):
        while len(self.total_steps_group) < len(self.eats):
            self.total_steps_group.append([])
        self.total_steps_group[len(self.eats)-1].append(step)

    # 增加一次成功的运行
    def add_success(self):
        while len(self.arrive_times) < len(self.eats):
            self.arrive_times.append([0, 0])
        self.arrive_times[len(self.eats)-1][0] +=1
        self.arrive_times[len(self.eats)-1][1] +=1

    # 增加一次失败的运行
    def add_fail(self):
        while len(self.arrive_times) < len(self.eats):
            self.arrive_times.append([0, 0])
        self.arrive_times[len(self.eats)-1][1] +=1

    # 计算当前数据下，每个吸收率对应的平均运行时间
    def cal_avg_steps(self):
        for i in range(len(self.total_steps_group)):
            i_total_steps = 0
            for j in self.total_steps_group[i]:
                i_total_steps += j
            self.avg_steps[i] = i_total_steps / len(self.total_steps_group[i])
        return self.avg_steps

    # 获得每个吸收率对应的平均运行时间
    def get_avg_steps(self):
        return self.avg_steps

    # 计算每一组中，到达时间的方差
    def cal_variance(self):
        self.cal_avg_steps()
        for i in range(len(self.total_steps_group)):
            i_variance = 0
            for j in self.total_steps_group[i]:
                i_variance += (j-self.avg_steps[i])**2
            self.variance_steps[i] = i_variance / len(self.total_steps_group[i])
        return self.variance_steps

    # 获得每个吸收率对应的方差
    def get_variance(self):
        return self.variance_steps

    # 计算每个吸收率对应的成功率（1000个step以内可以到达目标）
    def cal_success_rate(self):
        for i in range(len(self.arrive_times)):
            self.success_rate[i] = self.arrive_times[i][0] / self.arrive_times[i][1]
        return self.success_rate

    # 获得每一个吸收率对应的成功率
    def get_success_rate(self):
        return self.success_rate

    def arrive(self, a_agent, is_success):
        step = a_agent.get_times()
        if is_success:
            self.add_step(step)
            self.add_success()
        else:
            self.add_fail()

    def print_databox(self):
        print('========================================')

        print('eats:', len(self.eats))
        print('--------------------')
        print(self.eats)
        print('----------------------------------------')

        print('')

        print('total_steps_group', len(self.total_steps_group))
        print('--------------------')
        print(self.total_steps_group)
        print('----------------------------------------')

        print('')

        print('========================================')











