import random
import argparse
import pygame
import numpy as np
from pygame.locals import *
import random

class SimpleAgent:
    color_body = (0,255,0)
    color_grain = (0,0,255)

    def __init__(self, screen, args):
        args.ax0 += random.randint(-40, 40)
        args.ay0 += random.randint(-40, 40)

        self.SCREEN = screen
        self.eatRate = args.eat
        self.agent_x = args.ax
        self.agent_y = args.ay
        self.u = (args.ax0, args.ay0)
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
        self.quad = [0, 0, 0, 0]

    def update_agent(self):
        pygame.draw.rect(self.SCREEN, self.color_grain, (int(self.u_x), int(self.u_y), int(self.agent_x), int(self.agent_y)))
        # with blue racing stripes
        pygame.draw.rect(self.SCREEN, self.color_body, (int(self.u_x + self.agent_x / 2) - 1, int(self.u_y), 2, int(self.agent_y)))
        pygame.draw.rect(self.SCREEN, self.color_body, (int(self.u_x), int(self.u_y + self.agent_y / 2) - 1, int(self.agent_x), 2))

    def bounds(self):
        self.u_x = np.clip(0.0, self.u_x, self.win_x - self.agent_x)
        self.u_y = np.clip(0.0, self.u_y, self.win_y - self.agent_y)

        self.u = (self.u_x, self.u_y)
