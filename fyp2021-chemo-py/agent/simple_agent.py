import random
import argparse
import pygame
import numpy as np
from pygame.locals import *
import random
import math
import matplotlib.pyplot as plt

class SimpleAgent:
    color_body = (0,255,0)
    color_grain = (0,0,255)

    def __init__(self, screen, args, source):
        # args.ax0 += random.randint(-40, 40)
        # args.ay0 += random.randint(-40, 40)

        self.SCREEN = screen
        self.eatRate = args.eat
        self.agent_x = args.ax
        self.agent_y = args.ay
        self.u = [args.ax0, args.ay0]
        self.u_x = args.ax0
        self.u_y = args.ay0
        self.vr = args.avel
        self.source = source
        self.win_x = args.winx
        self.win_y = args.winy
        self.releaseRate = args.emit
        self.diffusionVariance = args.brown
        self.dt = args.dt
        self.frame = args.frame
        self.quad = [0, 0, 0, 0]

        self.u_start = (self.u_x, self.u_y)
        self.u_recoder = [self.u_start]
        self.time_box = [0]
        self.sch = True
        self.is_touch_me = False

        # lateral offset from target
        self.bias_target = [0]

        # lateral offset from last step
        self.bias_step = [0]

        # The distance of each step from the source
        self.distance = [math.hypot(self.source[0] - self.u[0], self.source[1] - self.u[1])]

        # How far is each step forward
        self.forward_step = [0]

    def update_agent(self):
        pygame.draw.rect(self.SCREEN, self.color_grain, (int(self.u_x), int(self.u_y), int(self.agent_x), int(self.agent_y)))
        # with blue racing stripes
        pygame.draw.rect(self.SCREEN, self.color_body, (int(self.u_x + self.agent_x / 2) - 1, int(self.u_y), 2, int(self.agent_y)))
        pygame.draw.rect(self.SCREEN, self.color_body, (int(self.u_x), int(self.u_y + self.agent_y / 2) - 1, int(self.agent_x), 2))

    def bounds(self):
        self.u_x = np.clip(0.0, self.u_x, self.win_x - self.agent_x)
        self.u_y = np.clip(0.0, self.u_y, self.win_y - self.agent_y)

        self.u = [self.u_x, self.u_y]

    def set_position(self, u_x, u_y):
        if self.u_x != u_x or self.u_y != u_y:
            self.is_touch_me = True
        if self.is_touch_me:
            self.u_recoder.append((u_y, u_y))
            self.u_x = u_x
            self.u_y = u_y
            self.u = [self.u_x, self.u_y]

            self.distance.append(math.hypot(self.source[0]-self.u[0], self.source[1]-self.u[1]))
            self.bias_step.append(self.point_distance_line(self.u_recoder[len(self.u_recoder)-1],
                                                           self.u_recoder[len(self.u_recoder)-2],
                                                           self.source))
            self.bias_target.append(self.point_distance_line(self.u_recoder[len(self.u_recoder)-1],
                                                             self.u_start,
                                                             self.source))
            self.forward_step.append(self.distance[len(self.distance)-1]-self.distance[len(self.distance)-2])
            self.time_box.append(self.time_box[len(self.time_box)-1]+1)

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

    def point_distance_line(self, point,line_point1,line_point2):
        #计算向量
        vec1 = (line_point1[0] - point[0], line_point1[1] - point[1])
        vec2 = (line_point2[0] - point[0], line_point2[1] - point[1])
        distance = np.abs(np.cross(vec1,vec2)) / np.linalg.norm((line_point1[0]-line_point2[0], line_point1[1]-line_point2[1]))
        return distance

    def is_arrive(self):
        if self.distance[-1] < 60:
            return True
        else:
            return False

    def get_times(self):
        return len(self.time_box)




# # lateral offset from target
# self.bias_target = [0]
#
# # lateral offset from last step
# self.bias_step = [0]
#
# # The distance of each step from the source
# self.distance = [math.hypot(self.source[0] - self.u[0], self.source[1] - self.u[1])]
