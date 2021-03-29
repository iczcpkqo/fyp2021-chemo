from stable_baselines import PPO2

from config import args
from env import Env
import time

# =========== [ Parameter Menu ] ========== #
i_eat_start = 0.14  # The minimum value of eat at the beginning of the program
i_eat_end = 1.00  # The maximum value of eat at the end of the program
i_eat_step = 0.01  # eat is the value that is incremented at the end of each fixed-eat cycle
i_run_times = 10  # Number of cycles per fixed eat

if __name__ == "__main__":

    step_recorder = 0

    args.pattern = current_pattern = 'decay'  # 'decay'  'spire'  Pick one of them
    args.useRl = False  # Whether to use the RL model to generate actions
    args.pygame = False  # Whether to visualize

    args.test = True  # When testing, the position of source is fixed at the specified position

    eat = i_eat_start  # eat Start from initial value

    # log Results
    import pandas as  pd

    result = pd.DataFrame(columns=['group', 'pattern', 'eat', 'absorbPartsNum', 'Time-consuming'])

    import pygame

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((args.winx, args.winy))
    pygame.display.set_caption("Smelly the Chemotactic Agent")
    font = pygame.font.SysFont('Cambria', 40)

    from main_backup import MyInterface

    my_ui = MyInterface(screen)
    switch_pattern = True
    while switch_pattern:
        if current_pattern == 'spire':
            args.sx = 500
            args.sy = 350
            model = PPO2.load('model\ppo_spire')
        elif current_pattern == 'decay':
            args.sx = 900
            args.sy = 600
            model = PPO2.load('model\ppo_decay')
        else:
            args.sx = 200
            args.sy = 500
            model = PPO2.load('model\ppo_decay')

        # Update group
        eat_group = 0

        env = Env(args)
        switch_pattern = False
        while eat <= i_eat_end:

            if switch_pattern:
                break
            # eat Update
            eat += i_eat_step
            for step in range(i_run_times):
                # Update group
                eat_group += 1

                if switch_pattern:
                    break
                # When resetting the environment, specify eat and useRl
                obs, done = env.reset(eat=eat, useRl=False), False

                step_recorder = 200
                while not done:

                    step_recorder += 1
                    if step_recorder%100 == 0:
                        # print(datetime.datetime.now() - step_recorder)
                        print('eat = ', eat, ' | step = ', step+1, '/', i_run_times, ' | step_recorder = ', step_recorder)

                    action, _states = model.predict(obs)
                    obs, rewards, done, info = env.step(action)

                    """
                    info There are statistics for each step:
                    'absorbPartsNum':    Number of ions absorbed in this step
                    'Time-consuming':    Total time spent
                    """
                    info.update({'group': eat_group,
                                 'eat': eat,
                                 'pattern': current_pattern})
                    result = result.append([info], ignore_index=False)

                    ui_pattern = env.render(screen=screen, font=font, my_ui=my_ui)

                    if ui_pattern and ui_pattern != current_pattern:
                        args.pattern = current_pattern = ui_pattern
                        switch_pattern = True
                        break

    # Write log results
    result.to_csv('result_'+ time.strftime("%Y-%m-%d %H.%M.%S", time.localtime()) + '.csv', index=False)
    # result.to_csv('result.csv_', index=False)
