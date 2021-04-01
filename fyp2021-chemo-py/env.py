import gym
import numpy as np
import pygame
import config
from pygame.locals import *

import math
# pygame config
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

## Parameter of 'theta' in the parametric equation of Archimedean spiral
## Degree of angle of change per unit of time, theta = 360 = 2 * math.pi
## It's different from theta, just per time theta
theta_per_time = 20 * (math.pi/180)

## Parameter of 'a' in the parametric equation of Archimedean spiral
## Radius = a , when theta = 0
a_arch_spire = -30

## Parameter of 'b' in the parametric equation of Archimedean spiral
## Growth of radius that from center to (x, y) of theta per unit
b_arch_spire = 5

rng_maker = np.random.default_rng()

# Set pygame
gameDisplay = pygame.display.set_mode( (config.args.winx, config.args.winy) )

# Load img for agent
agent_img = pygame.image.load('agent.png')

# Load Background img
background_img = pygame.image.load('background.png')

# Draw agent
def agentShow(x, y):
    gameDisplay.blit(agent_img,(x,y))

def updatePosition(u, v: np.ndarray, var, dt):
    # integration position based on velocity, using a single Euler step of: d/dt position = velocity + noise

    # velocity = dt * np.array(v)
    # noise = np.sqrt(dt * var) * np.random.randn(2)
    # delta_u = velocity + noise
    #
    # return u + delta_u

    velocity = dt * np.array(v)
    noise = np.sqrt(dt * var) * rng_maker.standard_normal(2)
    # noise = np.sqrt(dt * var) * np.random.randn(2)
    delta_u = velocity + noise

    # print('====================')
    # print('dt = ', dt)
    # print('var = ', var)
    # print('np.random.randn(2) = ', np.random.randn(2))
    # print('velocity = ', velocity)
    # print('noise = ', noise)
    # print('delta_u = ', delta_u)
    # print('====================')

    return u + delta_u


def whatQuad(x,y, maxx,maxy):
    if abs(x) > maxx or abs(y) > maxy or x == 0 or y == 0:
        return -1
    else:
        return int(x > 0) + 2*int(y > 0)

def calcv(quads, vr):
    xdir = np.sign(- quads[0] + quads[1] - quads[2] + quads[3])
    ydir = np.sign(- quads[0] - quads[1] + quads[2] + quads[3])
    return scaleVect(vr / np.sqrt(2), (xdir, ydir))

def scaleVect(s, v):
        return (s*v[0], s*v[1])

def getSpirePoint(idx, per, emit, time, center, a, b):
    # theta = per*(idx%count)/emit +
    rng = np.random.default_rng()
    theta = per * (time - (idx/emit))
    p_spire = archimedeanSpire(center, a, b, theta)

    if center[0]-p_spire[0] == 0:
        return p_spire
    # else:
    #     r = round(random.uniform(-30,30), 2)
    #     # r = rng.poisson(60) - 30
    #     # r = 1
    #     k = (center[1]-p_spire[1]) / (center[0]-p_spire[0])
    #     alpha = math.atan(k)
    #     return (p_spire[0] + r*math.cos(alpha), p_spire[1] + r*math.sin(alpha))
    else:

        r = np.sqrt(p_spire[0]**2 + p_spire[1]**2)
        r_1 = r/10
        r_2 = r_1/2
        # k = (center[1]-p_spire[1]) / (center[0]-p_spire[0])
        # alpha = math.atan(k)
        return (p_spire[0] + rng.poisson(r_1) - r_2, p_spire[1] + rng.poisson(r_1) - r_1)

# def getSpirePoint_New(u, per, emit, center, b):
#     u = [u[0] - center[0], u[1] - center[1]]
#
#     if u[1] == 0:
#         u[1] = 1
#
#     theta = math.atan(u[0]/u[1])
#     a = u[0]/math.cos(theta) - b*theta
#     theta_next = theta + theta_per_time
#
#     # x_next = (a+b_arch_spire*theta_next)*math.cos(theta_next)
#     # y_next = (a+b_arch_spire*theta_next)*math.sin(theta_next)
#
#     u_next = archimedeanSpire(center, a, b, theta_next)
#     print(u_next,center)
#     return u_next

def archimedeanSpire(center, a, b, theta):
    # Constants
    p = center[0]
    q = center[1]

    x_next = (a+b*theta)*math.cos(theta) + p
    y_next = (a+b*theta)*math.sin(theta) + q

    return x_next, y_next

class Env(gym.Env):
    # Set this in SOME subclasses
    reward_range = (-float('inf'), float('inf'))
    spec = None

    def __init__(self, args):
        super(Env, self).__init__()

        self.partices = []
        self.useRl = args.useRl
        self.pattern = args.pattern

        # Ambient maximum number of steps
        self.timeStep = args.timeStep

        # Window size
        self.win_x = args.winx
        self.win_y = args.winy

        # Agent length and width
        self.agent_x = args.ax
        self.agent_y = args.ay

        # When test = True, sorce position is fixed
        self.test = args.test
        self.source_test_init = [args.sx, args.sy]

        # expected number of particles released per unit time
        self.releaseRate = args.emit

        # time step of simulation
        self.dt = args.dt

        # particle diffusion variance per unit time
        self.diffusionVariance = args.brown

        # initial position of agent (offset from upper left corner)
        self.u_init = np.array([args.ax0, args.ay0])
        self.u = self.u_init

        # chase velocity of agent
        self.vr = args.avel

        # rl agent action space (don't care)
        self.action_space = gym.spaces.box.Box(low= np.array([-1, -1], dtype=np.float32),
                                               high=np.array([ 1,  1], dtype=np.float32))

        # rl agent observation space (leave it alone)
        self.observation_space = gym.spaces.box.Box(low= np.array([-self.agent_x / 2, -self.agent_y / 2], dtype=np.float32),
                                                    high=np.array([self.agent_x / 2,   self.agent_y / 2], dtype=np.float32))

        # display every i-th frame (default: %(default)s)
        self.frame = args.frame

        ## Initialize random number generator
        self.rng = np.random.default_rng()


    def step(self, action: np.ndarray):

        # The agent selects an action, the environment migrates one step,
        # and returns to the agent information such as new observations and rewards.

        # Update All particles positions
        self._updateParticles()

        dis_before = self._distance()

        # Calculate action by RL selection or by original method
        action_exec =  action * self.vr if self.useRl else calcv(self.quads, self.vr)

        # agent Execute action
        self.u = np.clip(
            updatePosition(self.u, action_exec, 0.0, self.dt),
            a_min=0.0,
            a_max=[self.win_x - self.agent_x, self.win_y - self.agent_y]
        )

        dis_after = self._distance()

        # Get the next status observation
        next_obs, absorbPartsNum = self._get_obs()

        # Calculate reward (distance variation of agent from source)
        reward =  dis_before - dis_after

        # Determine if termination conditions are met
        done = self._terminal()

        # log Information
        info = {'absorbPartsNum': absorbPartsNum,
                'Time-consuming': self.t}

        # total time update
        self.t += self.dt

        return next_obs, reward, done, info

    def reset(self, eat=0, useRl=True):
        # Reset environment
        self.useRl = useRl
        self.particles = [] # Clear ion
        self.t = 0.0 # Reset time

        # Reset the eat eat modifications on the outside
        self.eatRate = 1 - eat

        # source of particles (offset from lower right corner)
        if self.test:
            self.source = self.source_test_init
        else:
            self.source = [ np.random.rand() * self.win_x,
                            np.random.rand() * self.win_y]
        self.u = self.u_init

        # print(self.source)
        self.wind = self.u - self.source # Blow to agent
        self.wind = self.wind * 1.2 / np.linalg.norm(self.wind) #  Zoom Wind Speed Size
        return np.array([0, 0], dtype=np.float32)

    def render(self, screen, font, my_ui):
        # draw pygame
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()

        screen.fill(white)
        screen.blit(background_img, (0, 0))

        ## Draw the agent
        u_x, u_y = self.u.tolist()
        # pygame.draw.rect(screen, green, (int(u_x), int(u_y), int(self.agent_x), int(self.agent_y)))
        agentShow(int(u_x), int(u_y))

        # with blue racing stripes
        # pygame.draw.rect(screen, blue, (int(u_x + self.agent_x / 2) - 1, int(u_y), 2, int(self.agent_y)))
        # pygame.draw.rect(screen, blue, (int(u_x), int(u_y + self.agent_y / 2) - 1, int(self.agent_x), 2))

        ## Draw the odor source
        pygame.draw.circle(screen, blue, self.intPair(self.source), 5)
        ## Draw the particles

        for p in self.particles:
            pygame.draw.circle(screen, red, self.intPair(p), 2)
        screen.blit(font.render(' t = ' + str(round(self.t, 3)), False, (0, 0, 0)), (0, 0))

        ui_clicked = my_ui.show()

        pygame.display.update()

        # Return the pattern obtained by the ui
        return ui_clicked

    def close(self):
        pygame.quit()

    def seed(self, seed=None):
        pass

    def _agent_center(self):
        # Calculate agent center coordinates
        return self.u + [self.agent_x/2, self.agent_y/2]

    def _distance(self):
        # Payoff function
        distance = np.sqrt(
                        np.sum(
                            np.square(self._agent_center() - self.source)
                        )
                    )

        return distance

    def _updateParticles(self):

        # Update ion
        # 1, new particle generated from source;
        # 2, particle extinction determined by eatRate

        ## New ions are generated from the source
        # self.particles += [self.source] * self.rng.poisson(self.releaseRate * self.dt)

        self.partices.append(Particle(0, a_arch_spire, b_arch_spire, self.source))
        newParticles = []

        ## Initialize particle loop variables
        # old method of calculating the amount needed for an action: self.quads
        self.quads = [0, 0, 0, 0]

        for p in self.particles:
            print(p)
            # Update particle position
            if self.pattern == 'spire':
                # p_x, p_y = p = np.array(
                #     getSpirePoint(idx, theta_per_time, self.releaseRate, self.t,
                #                   (self.source[0], self.source[1]), a_arch_spire, b_arch_spire)
                # )


                p_x, p_y = np.array(
                    p.nextPosistion(theta_per_time)
                )
                # p_x, p_y = p = np.array(getSpirePoint_New(p, theta_per_time, self.releaseRate, (self.source[0], self.source[1]), b_arch_spire))
            else:
                p_x, p_y = updatePosition(p.u, self.wind, self.diffusionVariance, self.dt)
                p.setPosition((p_x, p_y))

            u_x, u_y = self.u

            i = whatQuad(
                p_x - (u_x + self.agent_x / 2),
                p_y - (u_y + self.agent_y / 2),
                self.agent_x / 2, self.agent_y / 2
            )

            if i >= 0:
                self.quads[i] += 1

            newParticles.append(p)

        self.particles = newParticles

    def _terminal(self):
        # episode Termination judgment.
        # 1, agent reaches source, end of task;
        # 2, agent out of bounds, end of task

        cent = self._agent_center()

        # Out of bounds out_of_range -> bool
        out_of_range  = self.u + [self.agent_x, self.agent_y] > [self.win_x, self.win_y]
        out_of_range  = np.any( self.u < 0 ) or np.any(out_of_range)

        if out_of_range or np.linalg.norm( cent-self.source ) < 20 :
            # todo: 到达source的判断阈值需要调整 当前为 20
            return True
        elif self.t > self.dt * self.timeStep :
            # The longest time step to reach the environment
            return True
        else:
            return False

    def _get_obs(self):
        # Obtaining status observations
        # return: Contact agent ions,
        #         average position relative to agent center [x, y],
        #         number of absorbed ions

        cent = self._agent_center()

        def _help(coor):
            # Does the particle hit the agent
            return np.all( np.abs( coor - cent ) < [self.agent_x / 2, self.agent_y / 2] )
        observed_particels = list(filter(_help, self.particles)) # observed_particels 是 所有碰到agent 的离子.

        # The particles are absorbed when they hit the agent
        beforeAbsorbed = len(self.particles)

        absorbFilter = lambda coor: ~_help(coor)
        filted_particles = list(filter(absorbFilter, self.particles)) # filted_particles : 所有没有碰到 agent 的离子

        # Absorb particles with the probability of self.eatRate
        filted_particles += [p for p in observed_particels if np.random.rand() < self.eatRate]
        self.particles = filted_particles

        afterAbsorbed = len(self.particles)

        absorbNum = beforeAbsorbed - afterAbsorbed # absorbNum : Number of absorbed particles

        if len(observed_particels) == 0:
            # No particles hit the agent
            return np.array([0, 0], dtype=np.float32), absorbNum
        else:
            observed_particels = np.array(observed_particels, dtype=np.float32)
            observed_particels = np.mean( observed_particels, axis=0 ) - self.u # 平均位置

            return observed_particels, absorbNum

    @classmethod
    def intPair(cls, p):
        return int(p[0]), int(p[1])

class Particle(gym.Env):

    def __init__(self, theta, a, b, center=(0,0)):
        self.u = (center[0], center[1])
        self.x = center[0]
        self.y = center[1]
        self.theta = theta
        self.a = a
        self.b = b
        self.center = center

    def nextPosition(self, per):
        self.theta = self.theta + per
        x = (self.a + self.b * self.theta) * math.cos(self.theta) + self.center[0]
        y = (self.a + self.b * self.theta) * math.sin(self.theta) + self.center[1]

        self.u = (x, y)
        self.x = x
        self.y = y

        return self.u

    def setPosition(self, u):
        self.u = u
        self.x = u[0]
        self.y = u[1]

        return u
