#!/usr/bin/python3

# © Copyright 2020, Roisin Mary Keating and Barak A. Pearlmutter, Maynooth University

import random
import argparse
import pygame
import numpy as np
from pygame.locals import *
import agent.simple_agent as sp_a
import matplotlib.pyplot as plt
import particle.simple_particle as sp_p
import maze.office as mz_of
import math
import calculate.databox as cal_db


def main():
    ## Process command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-debug", help="debug level (default: %(default)s)", type=int, default=0)
    parser.add_argument("-eat", help="agent's particle absorption rate (default: %(default)s)", type=float, default=0.25)
    parser.add_argument("-ax", help="agent width (default: %(default)s)", type=float, default=100.0)
    parser.add_argument("-ay", help="agent height (default: %(default)s)", type=float, default=20.0)
    parser.add_argument("-ax0", help="agent initial position down (default: %(default)s)", type=float, default=250.0)
    parser.add_argument("-ay0", help="agent initial position right (default: %(default)s)", type=float, default=250.0)
    parser.add_argument("-avel", help="agent chase velocity (default: %(default)s)", type=float, default=5.0)
    parser.add_argument("-sx", help="source offset left from LR (default: %(default)s)", type=float, default=100.0)
    parser.add_argument("-sy", help="source offset up from LR (default: %(default)s)", type=float, default=100.0)
    parser.add_argument("-winx", help="arena width (default: %(default)s)", type=int, default=1000)
    parser.add_argument("-winy", help="arena height (default: %(default)s)", type=int, default=600)
    parser.add_argument("-emit", help="particle emission rate (default: %(default)s)", type=float, default=5.0)
    parser.add_argument("-brown", help="particle diffusion variance (default: %(default)s)", type=float, default=5.0)
    parser.add_argument("-dt", help="simulation timestep (default: %(default)s)", type=float, default=0.3)
    parser.add_argument("-frame", help="display every i-th frame (default: %(default)s)", type=int, default=1)
    args = parser.parse_args()

    # debug level
    debug = args.debug

    if debug > 0:
        print(args)

    # absorption rate: chance of a particle being eaten when on agent for one unit of time
    eatRate = args.eat

    # size of arena
    win_x = args.winx
    win_y = args.winy

    # size of agent
    agent_x = args.ax
    agent_y = args.ay

    # expected number of particles released per unit time
    releaseRate = args.emit

    # time step of simulation
    dt = args.dt

    # particle diffusion variance per unit time
    diffusionVariance = args.brown

    # initial position of agent (offset from upper left corner)
    u = [args.ax0, args.ay0]

    # chase velocity of agent
    vr = args.avel

    # source of particles (offset from lower right corner)
    source = (args.sx, args.sy)

    frame = args.frame

    ## Update derived quantities
    source = (win_x - source[0], win_y - source[1])

    if debug > 0:
        print("source:", source)

    ## Initialize random number generator
    rng = np.random.default_rng()

    ## Initialize display (game) engine
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((win_x, win_y))
    pygame.display.set_caption("Smelly the Chemotactic Agent")
    font = pygame.font.SysFont('Cambria', 40)

    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    db_box = cal_db.DataBox()
    ## 递增吸收率 变化范围 - x
    for i_eat in np.arange(0, 1, 0.5):
        db_box.add_eat(i_eat)
        ## 循环运行代理次数
        for run_times in range(8):
            ## 吸收率步增
            args.eat = i_eat
            # args.eat = 0.25

            ## 代理回到起始位置
            args.ax0 = 250.0
            args.ay0 = 250.0
            ## 拿出来得args参数
            eatRate = args.eat
            u = [args.ax0, args.ay0]
            # 准备画图 draw some table
            # plt.ion()  # 开启interactive mode 成功的关键函数
            # plt.figure("some graph as you see")

            ## Initialize temportal loop variables
            particles = []
            t = 0.0
            framei = 0

            a_agent = sp_a.SimpleAgent(screen, args, source)
            agent_number = 0
            agent_box = []
            for i in range(0, agent_number):
                agent_box.append(sp_a.SimpleAgent(screen, args, source))

            # ii = 0
            # time_box = [0]

            while True:
                if framei == 0:
                    ## Time to die?
                    for event in pygame.event.get():
                        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                            pygame.quit()

                    ## Run, run, as fast as you can. You can't catch me, I'm the Stinky Cheese Man!
                    ## So comment this out:
                    # pygame.time.delay(100)

                    screen.fill(white)

                    ## Draw the agent
                    # (u_x,u_y) = u
                    # pygame.draw.rect(screen, green, (int(u_x), int(u_y), int(agent_x), int(agent_y)))
                    # # with blue racing stripes
                    # pygame.draw.rect(screen, blue, (int(u_x + agent_x/2)-1, int(u_y), 2, int(agent_y)))
                    # pygame.draw.rect(screen, blue, (int(u_x), int(u_y + agent_y/2)-1, int(agent_x), 2))

                    a_agent.update_agent()

                    for i_agent in agent_box:
                        i_agent.update_agent()

                    ## Draw the odor source
                    pygame.draw.circle(screen, blue, intPair(source), 5)

                ## Maybe particles are born: | 泊松分布，具体每一步的运算结果是什么？
                particles += [source] * rng.poisson(releaseRate * dt)

                # if ii < 10:
                #     print(particles)
                #     ii+=1

                if debug > 1:
                    print("particles =", particles)

                if debug > 0:
                    print("#particles:", len(particles))

                ## Initialize particle loop variables
                for i_agent in agent_box:
                    i_agent.quad = [0, 0, 0, 0]

                quads = [0, 0, 0, 0]
                newParticles = []

                for p in particles:

                    # Update particle position
                    (p_x, p_y) = p = updatePosition(p, wind(p, t), diffusionVariance, dt, rng)

                    if framei == 0:
                        pygame.draw.circle(screen, red, intPair(p), 2)

                    i = whatQuad(p_x - (a_agent.u_x + a_agent.agent_x / 2), p_y - (a_agent.u_y + a_agent.agent_y / 2),
                                 a_agent.agent_x / 2, a_agent.agent_y / 2)
                    p_survive = -1
                    for i_agent in agent_box:
                        p_touch = whatQuad(p_x - (i_agent.u_x + i_agent.agent_x / 2), p_y - (i_agent.u_y + i_agent.agent_y / 2),
                                           i_agent.agent_x / 2, i_agent.agent_y / 2)
                        if p_touch >= 0:
                            p_survive = 0
                            i_agent.quad[p_touch] += 1

                    if debug > 2:
                        print("agent", a_agent.u, "particle", p, "quad", i)
                    if i >= 0:
                        quads[i] += 1

                    if p_y < 0 or p_y > win_y or p_x < 0 or p_x > win_x:
                        if debug > 2:
                            print("Not adding: particle at", p, "off screen")
                    elif a_agent.eatRate == 0 or (i < 0 and p_survive < 0) or rng.exponential(1 / a_agent.eatRate) >= dt:
                        newParticles.append(p)
                    else:
                        if debug > 2:
                            print("Not adding: particle at", p, "quad", i, "eaten")

                particles = newParticles

                if debug > 0:
                    print("quads:", quads)

                # Calculate the new coordinates of the agent
                # (a_agent.u_x, a_agent.u_y) = updatePosition(a_agent.u, calcv(quads, a_agent.vr), 0.0, dt, rng)
                u_tmp = updatePosition(a_agent.u, calcv(quads, a_agent.vr), 0.0, dt, rng)
                a_agent.set_position(u_tmp[0],u_tmp[1])

                for i_agent in agent_box:
                    (i_agent.u_x, i_agent.u_y) = updatePosition(i_agent.u, calcv(i_agent.quad, i_agent.vr), 0.0, dt, rng)

                if debug > 0:
                    if a_agent.u_x < 0 or a_agent.u_y < 0 or a_agent.u_x + a_agent.agent_x > win_x or a_agent.u_y + a_agent.agent_y > win_y:
                        print("Agent out of bounds")

                a_agent.bounds()
                for i_agent in agent_box:
                    i_agent.bounds()

                if framei == 0:
                    # Update screen
                    screen.blit(font.render(' t = ' + str(round(t, 3)) + ', steps = ' + str(a_agent.get_times()), False, (0, 0, 0)), (0, 0))
                    pygame.display.update()

                t += dt
                framei = np.mod(framei + 1, frame)

                # if t > 10.0:
                #     framei = 1

                # # draw some table
                # plt.ion()  # 开启interactive mode 成功的关键函数
                # plt.figure("some graph as you see")
                #
                # # t_now = i*0.1
                # # t.append(t_now)#模拟数据增量流入，保存历史数据
                # # m.append(sin(t_now))#模拟数据增量流入，保存历史数据
                # # n.append(cos(t_now))#模拟数据增量流入，保存历史数据
                # # plt.plot(t,m,'-r')
                # # lateral
                # plt.subplot(2,2,1)
                # plt.title("lateral offset from target")
                # plt.xlabel("time")
                # plt.ylabel("distance")
                # plt.grid(True)
                # plt.plot(a_agent.time_box, a_agent.bias_target,'-g', lw=1)
                #
                # plt.subplot(2,2,2)
                # plt.title("lateral offset from last step")
                # plt.xlabel("time")
                # plt.ylabel("distance")
                # plt.grid(True)
                # plt.plot(a_agent.time_box, a_agent.bias_step,'-b', lw=1)
                #
                # plt.subplot(2,2,3)
                # plt.title("The distance of each step from the source")
                # plt.xlabel("time")
                # plt.ylabel("distance")
                # plt.grid(True)
                # plt.plot(a_agent.time_box, a_agent.distance,'-r', lw=1)
                #
                # plt.subplot(2,2,4)
                # plt.title("How far is each step forward")
                # plt.xlabel("time")
                # plt.ylabel("distance")
                # plt.grid(True)
                # plt.plot(a_agent.time_box, a_agent.forward_step,'--y', lw=1)
                #
                # # print(len(a_agent.time_box))
                #
                # plt.pause(0.001)
                # # if (i == 1999):
                # #     plt.pause(1)

                if a_agent.is_arrive() == True:
                    a_agent.set_runtime(t)
                    db_box.arrive(a_agent, True)
                    ## 回收内存
                    del a_agent
                    # plt.clf()  # 清空画布上的所有内容
                    break
                if t > 1000:
                    a_agent.set_runtime(t)
                    db_box.arrive(a_agent, False)
                    ## 回收内存
                    del a_agent
                    break
                # if not (a_agent.get_times() % 100):
                #     print(a_agent.get_times())

            # db_box.print_databox()

            # draw some table
            db_box.cal_all()
            # db_box.save_as_txt()
            db_box.savenew_as_txt()
            plt.ion()  # 开启interactive mode 成功的关键函数
            plt.figure("some graph as you see")

            # average time of each eat
            plt.subplot(2, 2, 1)
            plt.title("avg arrive time")
            plt.xlabel("eat rate")
            plt.ylabel("avg time")
            plt.grid(True)
            plt.plot(db_box.eats, db_box.avg_steps, '-g', lw=1)

            # probability of arrive no more than 1000time-step of each eat
            plt.subplot(2, 2, 2)
            plt.title("probability of arrive in 1000")
            plt.xlabel("eat rate")
            plt.ylabel("probability")
            plt.grid(True)
            plt.plot(db_box.eats, db_box.success_rate, '-g', lw=1)

            # variance of time of each eat
            plt.subplot(2, 2, 3)
            plt.title("arrive time variance")
            plt.xlabel("eat rate")
            plt.ylabel("variance")
            plt.grid(True)
            plt.plot(db_box.eats, db_box.variance_steps, '-g', lw=1)

            plt.pause(0.001)
            # 回收内存
            plt.clf()  # 清空画布上的所有内容

    pygame.quit()


# a velocity based on differential odors (highly viscous medium)
def calcv(quads, vr):
    xdir = np.sign(- quads[0] + quads[1] - quads[2] + quads[3])
    ydir = np.sign(- quads[0] - quads[1] + quads[2] + quads[3])
    return scaleVect(vr / np.sqrt(2), (xdir, ydir))


def updatePosition(u, v, var, dt, rng):
    # integration position based on velocity, using a single Euler step of: d/dt position = velocity + noise
    return sumVect(u, sumVect(scaleVect(dt, v),
                              scaleVect(np.sqrt(dt * var), (rng.standard_normal(), rng.standard_normal()))))


def whatQuad(x, y, maxx, maxy):
    if abs(x) > maxx or abs(y) > maxy or x == 0 or y == 0:
        return -1
    else:
        return int(x > 0) + 2 * int(y > 0)


def wind(p, t):
    return (-1.2, -0.3)


def scaleVect(s, v):
    return (s * v[0], s * v[1])


def sumVect(u, v):
    return (u[0] + v[0], u[1] + v[1])


def intPair(p):
    return (int(p[0]), int(p[1]))

if __name__ == "__main__":
    main()
