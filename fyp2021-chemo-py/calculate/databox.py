import random
import argparse
from decimal import Decimal

import numpy as np
import random
import math


class SingleData:
    # Data, just for one agent
    ## Eat of this agent
    __eat = None

    ## How many times the agent has moved
    __step = None

    ## Run time
    __time = None

    ## Did the agent successfully reach the goal?
    __arrive_successfully = None

    # Set data, setter
    ## Set eat
    def set_eat(self, eat):
        self.__eat = eat

    ## Set step
    def set_step(self, step):
        self.__step = step

    ## Set time
    def set_time(self, time):
        self.__time = time

    ## Set arrive or not
    def set_arrive(self, is_arrive):
        self.__arrive_successfully = is_arrive

    # Get the data
    ## Get eat
    def get_eat(self):
        return self.__eat

    ## Get step
    def get_step(self):
        return self.__step

    ## Get run time
    def get_time(self):
        return self.__time

    ## Get arrive or not
    def get_arrive(self):
        return self.__arrive_successfully

    # Some function
    ## Take all the data by one time when this agent finish her work.
    def now_finish(self, is_arrive, i_eat, i_time, i_step):
        self.set_arrive(is_arrive)
        self.set_eat(i_eat)
        self.set_time(i_time)
        self.set_step(i_step)


class DataBox:
    # Data box for putting all singledata in.

    # Init
    ## Init function
    def __init__(self):
        self.init_general()
        self.init_steps()
        self.init_caldata()

    # Init data
    ## Init general data
    def init_general(self):
        # General
        ## Eat.old
        self.eats = []
        ## Record every data .old
        self.data_box = []
        # New data
        ## Eat box,
        self.__eats = []
        ## save all the singledata
        self.__databox = []

    ## Init step data
    def init_steps(self):
        # Step data
        ## How many steps should evey singleData cost
        self.total_steps_group = []
        ## Save avg steps of every singleData
        self.avg_steps = []
        ## Save variance of every group of singleData which have same eat.
        self.variance_steps = []
        # new data
        # step data
        self.__avg_steps = []
        self.__variance_steps = []

    ## Init time
    def init_time(self):
        # time data
        self.total_seconds_group = []
        self.avg_seconds = []
        self.variance_time = []

        # new data
        self.__avg_time = []
        self.__variance_time = []

    ## Init some data about calculate
    def init_caldata(self):
        # Calculate data
        ## Make a name as a ID for Databox
        self.id_box = self.create_data_id()
        self.arrive_times = []
        self.success_rate = []

        # new data
        # Calculate data
        ## Make a name as a ID for Databox
        self.__id_box = self.create_data_id()
        self.__success_times = []
        self.__success_rate = []
        self.__total_times = []

    # Add
    ## Add a eat .old
    def add_eat(self, eat):
        self.eats.append(eat)

    ## Add a result
    def add_data(self, single_data):
        if single_data.get_eat() not in self.__eats:
            self.__eats.append(single_data.get_eat())
            self.__databox.append([])
        self.__databox[self.__eats.index(single_data.get_eat())].append(single_data)

    # Add steps
    ## Add step.old
    def add_step(self, step):
        while len(self.total_steps_group) < len(self.eats):
            self.total_steps_group.append([])
        self.total_steps_group[len(self.eats) - 1].append(step)

    ## .old
    def add_success(self):
        while len(self.arrive_times) < len(self.eats):
            self.arrive_times.append([0, 0])
        self.arrive_times[len(self.eats) - 1][0] += 1
        self.arrive_times[len(self.eats) - 1][1] += 1

    ## .old
    def add_fail(self):
        while len(self.arrive_times) < len(self.eats):
            self.arrive_times.append([0, 0])
        self.arrive_times[len(self.eats) - 1][1] += 1

    ## Get the average running time corresponding to each absorption rate
    def get_avg_steps(self):
        # return self.avg_steps
        return self.__avg_steps

    ## Get the variance corresponding to each absorption rate
    def get_variance(self):
        # return self.variance_steps
        return self.__variance_steps

    ## Get the success rate corresponding to each absorption rate
    def get_success_rate(self):
        # return self.success_rate
        return self.__success_rate

    # calculate data
    ## Calculate the average running time of each absorption rate under the current data
    def cal_avg_time(self):
        while len(self.__avg_time) < len(self.__databox):
            self.__avg_time.append(0)
        for i in range(len(self.__databox)):
            i_sum_time = 0
            for j in range(len(self.__databox[i])):
                i_sum_time += j.get_time()
            self.__avg_time[i] = i_sum_time / len(self.__databox[i])

    ## Calculate the average number of runs corresponding to each absorption rate under the current data
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

    ## Calculate the variance of the arrival time in each group.old
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

    ## Calculate the variance of the arrival time in each group
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

    ## Calculate the variance of the number of arrivals in each group
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

    ## Calculate the success rate corresponding to each absorption rate (the goal can be reached within 1000 steps)
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

    ## Calculate all statistics
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

    ## Determine whether the incoming agent has reached the source [Which agent, did it succeed?]. old
    def arrive(self, a_agent, is_success):
        step = a_agent.get_runtime()
        if is_success:
            self.add_step(step)
            self.add_success()
        else:
            self.add_step(0)
            self.add_fail()

    ## Make a .txt name also ID
    def create_data_id(self):
        name_a = ['two', 'three', 'four', 'many', 'some']
        name_big = ['tiny', 'puny', 'wee', 'weeny', 'small', 'light', 'mild', 'gentle', 'ethereal', 'heavy', 'fat',
                    'black', 'white', 'green', 'blue', 'expensive']
        name_thing = ['cats', 'dogs', 'cars', 'apples', 'oranges', 'pears', 'classmates']
        return str(name_a[random.randint(0, len(name_a) - 1)]) + " " + str(
            name_big[random.randint(0, len(name_big) - 1)]) + " " + str(
            name_thing[random.randint(0, len(name_thing) - 1)])

    ## Print some data I want to see
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

    # Data stored in file
    ## Save all data.old
    def save_as_txt(self):
        file = open(self.id_box + ".txt", "w")
        # file.write("eat  |  time\n")
        for i in range(len(self.eats)):
            for j in range(len(self.total_steps_group)):
                for k in range(len(self.total_steps_group[j])):
                    file.write(str(self.eats[i]) + "\t" + str(self.total_steps_group[j][k]) + "\n")
        file.close()

    ## Save the latest piece of data.old
    def savenew_as_txt(self):
        file = open(self.id_box + ".txt", "a")
        file.write(str(self.eats[-1]) + "\t" + str(self.total_steps_group[-1][-1]) + "\n")
        file.close()

    ## Save the time spent in each run
    def save_databox_time(self):
        file = open(self.id_box + ".txt", "w")
        # file.write("eat  |  time\n")
        for i in self.__databox:
            for j in i:
                file.write(str(j.get_eat()) + "\t" + str(j.get_time()) + "\n")
        file.close()

    ## Save the time spent in a run
    def save_singledata_time(self, single_data):
        file = open(self.id_box + ".txt", "a")
        # file.write("eat  |  time\n")
        file.write(str(Decimal(single_data.get_eat()).quantize(Decimal("0.00"))) + "\t" + str(Decimal(single_data.get_time()).quantize(Decimal("0.00"))) + "\n")
        file.close()
