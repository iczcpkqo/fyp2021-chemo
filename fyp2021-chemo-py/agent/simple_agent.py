import random
import argparse
import pygame
import numpy as np
from pygame.locals import *
import random
import math
import matplotlib.pyplot as plt


class SimpleAgent:
    # Base data
    color_body = (0, 255, 0)
    color_grain = (0, 0, 255)

    # Screen data
    SCREEN = None

    # Args data
    is_init_args = False
    __eatRate = None
    agent_x = None
    agent_y = None
    u = None
    u_x = None
    u_y = None
    vr = None
    source = None
    win_x = None
    win_y = None
    releaseRate = None
    diffusionVariance = None
    dt = None
    frame = None
    u_start = None
    u_recoder = None

    # General data
    quad = None
    time_box = None
    steps = None
    sch = None
    is_touch_me = None
    ## How much time pass
    runtime = None

    # Calculative data
    ## Lateral offset from target
    bias_target = None
    ## Lateral offset from last step
    bias_step = None
    ## The distance of each step from the source
    distance = None
    ## How far is each step forward
    forward_step = None

    def __init__(self, switch_cartoon, screen, args):
        # args.ax0 += random.randint(-40, 40)
        # args.ay0 += random.randint(-40, 40)
        if switch_cartoon:
            self.init_yeacartoon(screen, args)
        elif not switch_cartoon:
            self.init_nocartoon(args)

    # No cartoon
    def init_nocartoon(self, args):
        self.init_args(args)
        self.init_general()
        self.init_cal()

    # yea cartoon
    def init_yeacartoon(self, screen, args):
        self.init_screen(screen)
        self.init_args(args)
        self.init_general()
        self.init_cal()

    # Init screen
    def init_screen(self, screen):
        self.SCREEN = screen

    # Init args
    def init_args(self, args):
        self.__eatRate = args.eat
        self.agent_x = args.ax
        self.agent_y = args.ay
        self.u = [args.ax0, args.ay0]
        self.u_x = args.ax0
        self.u_y = args.ay0
        self.vr = args.avel
        self.source = (args.sx, args.sy)
        self.win_x = args.winx
        self.win_y = args.winy
        self.releaseRate = args.emit
        self.diffusionVariance = args.brown
        self.dt = args.dt
        self.frame = args.frame
        self.u_start = (self.u_x, self.u_y)
        self.u_recoder = [self.u_start]
        self.is_init_args = True
        self.source = (args.winx - self.source[0], args.winy - self.source[1])

    # Init source
    def init_source(self, source):
        return None

    # Init general data
    def init_general(self):
        self.quad = [0, 0, 0, 0]
        self.time_box = [0]
        self.steps = 0
        self.sch = True
        self.is_touch_me = False
        # How much time pass
        self.runtime = 0

    # Init calculative data
    def init_cal(self):
        # Lateral offset from target
        self.bias_target = [0]
        # Lateral offset from last step
        self.bias_step = [0]
        # How far is each step forward
        self.forward_step = [0]
        if self.is_init_args:
            # The distance of each step from the source
            self.distance = [math.hypot(self.source[0] - self.u[0], self.source[1] - self.u[1])]

    # Setter
    ## Set eat rate
    def set_eat(self, i_eat):
        self.__eatRate = i_eat

    # Getter
    def get_eat(self):
        return self.__eatRate

    # Updater
    ## Update draw
    def update_agent(self):
        pygame.draw.rect(self.SCREEN, self.color_grain,
                         (int(self.u_x), int(self.u_y), int(self.agent_x), int(self.agent_y)))
        # With blue racing stripes
        pygame.draw.rect(self.SCREEN, self.color_body,
                         (int(self.u_x + self.agent_x / 2) - 1, int(self.u_y), 2, int(self.agent_y)))
        pygame.draw.rect(self.SCREEN, self.color_body,
                         (int(self.u_x), int(self.u_y + self.agent_y / 2) - 1, int(self.agent_x), 2))

    ## Update bounds
    def bounds(self):
        self.u_x = np.clip(0.0, self.u_x, self.win_x - self.agent_x)
        self.u_y = np.clip(0.0, self.u_y, self.win_y - self.agent_y)

        self.u = [self.u_x, self.u_y]

    # Calculative data

    ## Update position
    def set_position(self, u_x, u_y):
        # 每一次位置变更时触发
        if self.u_x != u_x or self.u_y != u_y:
            self.is_touch_me = True
        # 在第一次触发后，每一帧都触发
        if self.is_touch_me:
            self.u_recoder.append((u_y, u_y))
            self.u_x = u_x
            self.u_y = u_y
            self.u = [self.u_x, self.u_y]

            ### Temp delete ###
            # self.distance.append(math.hypot(self.source[0] - self.u[0], self.source[1] - self.u[1]))
            # self.bias_step.append(self.point_distance_line(self.u_recoder[len(self.u_recoder) - 1],
            #                                                self.u_recoder[len(self.u_recoder) - 2],
            #                                                self.source))
            # self.bias_target.append(self.point_distance_line(self.u_recoder[len(self.u_recoder) - 1],
            #                                                  self.u_start,
            #                                                  self.source))
            # self.forward_step.append(self.distance[len(self.distance) - 1] - self.distance[len(self.distance) - 2])
            # self.time_box.append(self.time_box[len(self.time_box) - 1] + 1)
            ###  ###
            self.add_steps(1)

        # if (len(self.time_box)==501 and ):
        # print(len(self.time_box))
        # print(self.sch)

        # if (len(self.time_box)==201 and self.sch):
        #     print("dfsfsdf")
        #     del self.u_recoder[0:200]
        #     del self.distance[0:200]
        #     del self.bias_step[0:200]
        #     del self.bias_target[0:200]
        #     del self.forward_step[0:200]
        #     del self.time_box[0:200]
        #     self.time_box[0] = 0
        #     # for i in range(len(self.time_box)):
        #     #     self.time_box[i] = i
        #     self.sch = False
        #     plt.clf() #清空画布上的所有内容
        #     print(self.time_box)
        #     print(self.bias_target)

    def point_distance_line(self, point, line_point1, line_point2):
        # 计算向量
        vec1 = (line_point1[0] - point[0], line_point1[1] - point[1])
        vec2 = (line_point2[0] - point[0], line_point2[1] - point[1])
        distance = np.abs(np.cross(vec1, vec2)) / np.linalg.norm(
            (line_point1[0] - line_point2[0], line_point1[1] - line_point2[1]))
        return distance

    def is_arrive(self):
        if self.is_init_args:
            # The distance of each step from the source
            now_distance = math.hypot(self.source[0] - self.u[0], self.source[1] - self.u[1])
            if now_distance < 60:
                return True
        return False

    def set_runtime(self, runtime):
        self.runtime = runtime

    def add_steps(self, i_step):
        self.steps += i_step

    def get_times(self):
        return len(self.time_box)

    def get_runtime(self):
        return self.runtime

    def get_steps(self):
        return self.steps

# # lateral offset from target
# self.bias_target = [0]
#
# # lateral offset from last step
# self.bias_step = [0]
#
# # The distance of each step from the source
# self.distance = [math.hypot(self.source[0] - self.u[0], self.source[1] - self.u[1])]
