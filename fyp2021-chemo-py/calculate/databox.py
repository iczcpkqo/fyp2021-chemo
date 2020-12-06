import random
import argparse
from decimal import Decimal

import numpy as np
import random
import math


class SingleData:
    # 数据
    ## 当前数据的吸收率
    __eat = None

    ## 移动的次数
    __step = None

    ## 移动的时间
    __time = None

    ## 运行是否成功
    __arrive_successfully = None

    # 设置数据
    ## 设置吸收率
    def set_eat(self, eat):
        self.__eat = eat

    ## 设置次数
    def set_step(self, step):
        self.__step = step

    ## 设置时间
    def set_time(self, time):
        self.__time = time

    ## 设置抵达状态
    def set_arrive(self, is_arrive):
        self.__arrive_successfully = is_arrive

    # 获取数据
    ## 获取吸收率
    def get_eat(self):
        return self.__eat

    ## 获取次数
    def get_step(self):
        return self.__step

    ## 获取时间
    def get_time(self):
        return self.__time

    ## 获取是否成功
    def get_arrive(self):
        return self.__arrive_successfully

    # 场景方法
    ## 当运行一次后，根据结果一次性组装所有数据
    def now_finish(self, is_arrive, i_eat, i_time, i_step):
        self.set_arrive(is_arrive)
        self.set_eat(i_eat)
        self.set_time(i_time)
        self.set_step(i_step)


class DataBox:
    # 数据

    # 实例初始化
    ## 步数容器
    def __init__(self):
        self.init_general()
        self.init_steps()
        self.init_caldata()

    # 初始化数据
    ## 初始化总数据
    def init_general(self):
        # 总数据
        ## 吸收率列表.old
        self.eats = []
        ## 记录每一次运行.old
        self.data_box = []
        # new data
        ## 吸收率列表
        self.__eats = []
        ## 每一次运行结果容器
        self.__databox = []

    ## 初始化步数数据
    def init_steps(self):
        # 步数数据
        ## 每个吸收率对应的运行组, 记录每一次运行成功所需要的step (每一组都是使用同一个吸收率运行很多次的结果)
        self.total_steps_group = []
        ## 每个吸收率对应的平均步数
        self.avg_steps = []
        ## 每个吸收率对应的运行组的步数方差
        self.variance_steps = []
        # new data
        # 步数数据
        ## 每个吸收率对应的平均步数 [平均步数]
        self.__avg_steps = []
        ## 每个吸收率对应的运行组的步数方差 [吸收率, 步数方差]
        self.__variance_steps = []

    ## 初始化时间数据
    def init_time(self):
        # 时间数据
        ## 每个吸收率对应的运行组, 记录每一次运行成功所需要的step (每一组都是使用同一个吸收率运行很多次的结果)
        self.total_seconds_group = []
        ## 每个吸收率对应的平均时间
        self.avg_seconds = []
        ## 每个吸收率对应的运行组的时间方差
        self.variance_time = []

        # new data
        # 时间数据
        ## 每个吸收率对应的平均时间 [[吸收率, 平均时间]]
        self.__avg_time = []
        ## 每个吸收率对应的运行组的时间方差 [[吸收率, 时间方差]]
        self.__variance_time = []

    ## 初始化计算数据
    def init_caldata(self):
        # 计算数据
        ## 生成数据容器的ID
        self.id_box = self.create_data_id()
        ## 成功次数，运行总次数, 每一组存放了两个数据 [到达次数, 运行总次数]
        self.arrive_times = []
        ## 每一个吸收率对应的运行组的成功率
        self.success_rate = []

        # new data
        # 计算数据
        ## 生成数据容器的ID
        self.__id_box = self.create_data_id()
        ## 成功次数，每一个吸收率对应的成功次数 [成功次数]
        self.__success_times = []
        ## 每一个吸收率对应的运行组的成功率 [成功率]
        self.__success_rate = []
        ## 每一个吸收率对应的，运行总次数
        self.__total_times = []

    # 增加总数
    ## 增加一个吸收率.old
    def add_eat(self, eat):
        self.eats.append(eat)

    ## 增加一次运行结果
    def add_data(self, single_data):
        if single_data.get_eat() not in self.__eats:
            self.__eats.append(single_data.get_eat())
            self.__databox.append([])
        self.__databox[self.__eats.index(single_data.get_eat())].append(single_data)

    # 增加步数数据
    ## 增加一个运行步数.old
    def add_step(self, step):
        while len(self.total_steps_group) < len(self.eats):
            self.total_steps_group.append([])
        self.total_steps_group[len(self.eats) - 1].append(step)

    # 增加计算数据
    ## 增加一次成功的运行.old
    def add_success(self):
        while len(self.arrive_times) < len(self.eats):
            self.arrive_times.append([0, 0])
        self.arrive_times[len(self.eats) - 1][0] += 1
        self.arrive_times[len(self.eats) - 1][1] += 1

    ## 增加一次失败的运行.old
    def add_fail(self):
        while len(self.arrive_times) < len(self.eats):
            self.arrive_times.append([0, 0])
        self.arrive_times[len(self.eats) - 1][1] += 1

    # 获得计算数据
    ## 获得每个吸收率对应的平均运行时间
    def get_avg_steps(self):
        # return self.avg_steps
        return self.__avg_steps

    ## 获得每个吸收率对应的方差
    def get_variance(self):
        # return self.variance_steps
        return self.__variance_steps

    ## 获得每一个吸收率对应的成功率
    def get_success_rate(self):
        # return self.success_rate
        return self.__success_rate

    # 计算数据
    ## 计算当前数据下，每个吸收率的平均运行时间
    def cal_avg_time(self):
        while len(self.__avg_time) < len(self.__databox):
            self.__avg_time.append(0)
        for i in range(len(self.__databox)):
            i_sum_time = 0
            for j in range(len(self.__databox[i])):
                i_sum_time += j.get_time()
            self.__avg_time[i] = i_sum_time / len(self.__databox[i])

    ## 计算当前数据下，每个吸收率对应的平均运行次数
    def cal_avg_steps(self):
        ### old
        # while len(self.avg_steps) < len(self.eats):
        #     self.avg_steps.append(0)
        # for i in range(len(self.total_steps_group)):
        #     i_total_steps = 0
        #     for j in self.total_steps_group[i]:
        #         i_total_steps += j
        #     self.avg_steps[i] = i_total_steps / len(self.total_steps_group[i])
        # return self.avg_steps
        ### new
        while len(self.__avg_steps) < len(self.__databox):
            self.__avg_steps.append(0)
        for i in range(len(self.__databox)):
            i_sum_steps = 0
            for j in range(len(self.__databox[i])):
                i_sum_steps += j.get_step()
            self.__avg_steps[i] = i_sum_steps / len(self.__databox[i])

    ## 计算每一组中，到达时间的方差.old
    def cal_variance(self):
        self.cal_avg_steps()
        while len(self.variance_steps) < len(self.eats):
            self.variance_steps.append(0)
        for i in range(len(self.total_steps_group)):
            i_variance = 0
            for j in self.total_steps_group[i]:
                i_variance += (j - self.avg_steps[i]) ** 2
            self.variance_steps[i] = i_variance / len(self.total_steps_group[i])
        return self.variance_steps

    ## 计算每一组中，到达时间的方差
    def cal_variance_time(self):
        self.cal_avg_time()
        while len(self.__variance_time) < len(self.__databox):
            self.__variance_time.append(0)
        for i in range(len(self.__databox)):
            i_variance = 0
            for j in self.__databox[i]:
                i_variance += (j.get_time() - self.__avg_time[i]) ** 2
            self.__variance_time[i] = i_variance / len(self.__databox[i])
        return self.__variance_time

    ## 计算每一组中，到达次数的方差
    def cal_variance_steps(self):
        self.cal_avg_steps()
        while len(self.__variance_steps) < len(self.__databox):
            self.__variance_steps.append(0)
        for i in range(len(self.__databox)):
            i_variance = 0
            for j in self.__databox[i]:
                i_variance += (j.get_step() - self.__avg_steps[i]) ** 2
            self.__variance_steps[i] = i_variance / len(self.__databox[i])
        return self.__variance_steps

    ## 计算每个吸收率对应的成功率（1000个step以内可以到达目标）
    def cal_success_rate(self):
        # while len(self.success_rate) < len(self.eats):
        #     self.success_rate.append(0)
        # for i in range(len(self.arrive_times)):
        #     self.success_rate[i] = self.arrive_times[i][0] / self.arrive_times[i][1]
        # return self.success_rate
        while len(self.__success_rate) < len(self.__databox):
            self.__success_rate.append(0)
        for i in range(len(self.arrive_times)):
            i_success = 0
            i_total = 0
            for j in self.__databox[i]:
                i_total += 1
                if j.get_arrive() == True:
                    i_success += 1
            self.__success_rate[i] = i_success / i_total
        return self.__success_rate

    ## 计算所有统计数据
    def cal_all(self):
        # old
        self.cal_variance()
        self.cal_success_rate()
        self.cal_avg_steps()

        # new
        self.cal_avg_steps()
        self.cal_avg_time()
        self.cal_variance_steps()
        self.cal_variance_time()
        self.cal_success_rate()

    # 外部辅助
    ## 判断传入代理是否抵达源头 [哪一个代理， 成功了吗]. old
    def arrive(self, a_agent, is_success):
        step = a_agent.get_runtime()
        if is_success:
            self.add_step(step)
            self.add_success()
        else:
            self.add_step(0)
            self.add_fail()

    # 内部辅助
    ## 创建当前数据容器的ID
    def create_data_id(self):
        name_a = ['two', 'three', 'four', 'many', 'some']
        name_big = ['tiny', 'puny', 'wee', 'weeny', 'small', 'light', 'mild', 'gentle', 'ethereal', 'heavy', 'fat',
                    'black', 'white', 'green', 'blue', 'expensive']
        name_thing = ['cats', 'dogs', 'cars', 'apples', 'oranges', 'pears', 'classmates']
        return str(name_a[random.randint(0, len(name_a) - 1)]) + " " + str(
            name_big[random.randint(0, len(name_big) - 1)]) + " " + str(
            name_thing[random.randint(0, len(name_thing) - 1)])

    ## 打印一些我想看的数据
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

    # 数据存入文件中
    ## 保存全部数据.old
    def save_as_txt(self):
        file = open(self.id_box + ".txt", "w")
        # file.write("eat  |  time\n")
        for i in range(len(self.eats)):
            for j in range(len(self.total_steps_group)):
                for k in range(len(self.total_steps_group[j])):
                    file.write(str(self.eats[i]) + "\t" + str(self.total_steps_group[j][k]) + "\n")
        file.close()

    ## 保存最新一条数据.old
    def savenew_as_txt(self):
        file = open(self.id_box + ".txt", "a")
        file.write(str(self.eats[-1]) + "\t" + str(self.total_steps_group[-1][-1]) + "\n")
        file.close()

    ## 保存每一次运行耗费的时间
    def save_databox_time(self):
        file = open(self.id_box + ".txt", "w")
        # file.write("eat  |  time\n")
        for i in self.__databox:
            for j in i:
                file.write(str(j.get_eat()) + "\t" + str(j.get_time()) + "\n")
        file.close()

    ## 保存一次运行耗费的时间
    def save_singledata_time(self, single_data):
        file = open(self.id_box + ".txt", "a")
        # file.write("eat  |  time\n")
        file.write(str(Decimal(single_data.get_eat()).quantize(Decimal("0.00"))) + "\t" + str(Decimal(single_data.get_time()).quantize(Decimal("0.00"))) + "\n")
        file.close()
