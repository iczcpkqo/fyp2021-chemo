# FYP Supporting Documentation

## Program Function

### Training Model

* Run `run.py` to get the reinforcement-learning trained model.
* Models are stored in the model folder.
* Training the model takes a lot of time.
* The model is currently trained and can be used directly. If you don't want to spend a lot of time training the model **you can skip this step**.

### Agent for Reinforcement Learning

* Run `main.py` to run the Agent **with** reinforcement 
* When the program finishes running, the runtime data associated with the agent will be saved in the root directory as a **.csv** file with the format `result_<time>.csv`.

### General Agent without reinforcement learning

* Run `main_backup.py` to run the Agent **without** reinforcement learning
* When the program finishes running, the runtime data associated with the agent will be saved in the root directory as a **.txt** file with the format `<time>.txt`.

## Installation required

### Important Installation

> ==**If the installation does not work due to missing packages, please try the `Basic Installation` below to install more packages**==

| No. | Name             | Version | Installation via pip                 |
| --- | ---------------- | ------- | ------------------------------------ |
| 1   | stable_baselines | 2.10.1  | pip install stable_baselines==2.10.1 |
| 1   | tensorflow       | 1.14.0  | pip install tensorflow==1.14.0       |

### Basic Installation

> ==**If the installation does not work due to missing packages, please try the `FULL Installation` below to install more packages**==

| No. | Name                    | Version |
| --- | ----------------------- | ------- |
| 1   | gym                     | 0.18.0  |
| 2   | numpy                   | 1.19.3  |
| 3   | pygame                  | 1.9.6   |
| 4   | matplotlib              | 3.3.3   |
| 5   | pandas                  | 1.1.5   |
| 6   | stable_baselines        | 2.10.1  |
| 7   | tensorflow              | 1.14.0  |
| 8   | argparse                | -       |
| 9   | datetime                | -       |
| 10  | decimal                 | -       |
| 11  | math                    | -       |
| 12  | pprint                  | -       |
| 13  | time                    | -       |

## FULL Installation

| No. | Name                    | Version    |
| --- | ----------------------- | ---------- |
| 1   | absl-py                 | 0.12.0     |
| 2   | astor                   | 0.8.1      |
| 3   | atari-py                | 0.2.6      |
| 4   | cached-property         | 1.5.2      |
| 5   | click                   | 7.1.2      |
| 6   | cloudpickle             | 1.6.0      |
| 7   | Corpora                 | 1.0        |
| 8   | cycler                  | 0.10.0     |
| 9   | Cython                  | 0.29.14    |
| 10  | future                  | 0.18.2     |
| 11  | gast                    | 0.4.0      |
| 12  | gensim                  | 3.8.3      |
| 13  | google-pasta            | 0.2.0      |
| 14  | grpcio                  | 1.36.1     |
| 15  | gym                     | 0.18.0     |
| 16  | h5py                    | 3.2.1      |
| 17  | importlib-metadata      | 3.9.1      |
| 18  | joblib                  | 1.0.0      |
| 19  | Keras-Applications      | 1.0.8      |
| 20  | Keras-Preprocessing     | 1.1.2      |
| 21  | kiwisolver              | 1.3.1      |
| 22  | llvmlite                | 0.35.0     |
| 23  | Markdown                | 3.3.4      |
| 24  | matplotlib              | 3.3.3      |
| 25  | nltk                    | 3.5        |
| 26  | numba                   | 0.52.0     |
| 27  | numpy                   | 1.19.3     |
| 28  | opencv-python           | 4.5.1.48   |
| 29  | pandas                  | 1.1.5      |
| 30  | Pillow                  | 7.2.0      |
| 31  | protobuf                | 3.15.6     |
| 32  | pygame                  | 1.9.6      |
| 33  | pyglet                  | 1.5.0      |
| 34  | pyparsing               | 2.4.7      |
| 35  | python-dateutil         | 2.8.1      |
| 36  | pytz                    | 2020.4     |
| 37  | regex                   | 2020.11.13 |
| 38  | scikit-learn            | 0.23.2     |
| 39  | scipy                   | 1.5.4      |
| 40  | six                     | 1.15.0     |
| 41  | smart-open              | 4.1.0      |
| 42  | stable-baselines        | 2.10.1     |
| 43  | tensorboard             | 1.14.0     |
| 44  | tensorflow              | 1.14.0     |
| 45  | tensorflow-estimator    | 1.14.0     |
| 46  | termcolor               | 1.1.0      |
| 47  | threadpoolctl           | 2.1.0      |
| 48  | tqdm                    | 4.55.1     |
| 49  | typing-extensions       | 3.7.4.3    |
| 50  | Werkzeug                | 1.0.1      |
| 51  | wrapt                   | 1.12.1     |
| 52  | zipp                    | 3.4.1      |


## Description of key parameters


### main.py

> The following are parameters that may be modified to obtain data of different sizes and scales. Parameters that are not often modified are in the `parser` variable in the `config.py` file.

#### i_eat_start = 0.14

* Parameter explanation
    - The minimum value of eat when the program is run

* Optional content
    - float
    - e.g., 0.14, 0.55

#### i_eat_end   = 0.16

* Parameter explanation
    - The maximum value of eat at the end of the program run

* Optional content
    - float
    - e.g., 0.14, 0.55

#### i_eat_step  = 0.01

* Parameter explanation
    - The program is run many times with different eats, and the interval between each different eat

* Optional content
    - float
    - e.g., 0.01, 0.1

#### i_run_times = 1

* Parameter explanation
    - Number of times the program runs with the same eat value

* Optional content
    - int
    - e.g., 1, 10, 53, 100, 3333

### main_backup.py

> The following are parameters that may be modified to obtain data of different sizes and scales. Parameters that are not often modified are in the `parser` variable in the `main_backup.py` file.


#### switch_cartoon

* Parameter explanation
    - Whether to open the pygame window

* Optional content
    - Boolean
    - e.g., True, False

#### pattern_name

* Parameter explanation
    - Selecting particle effects

* Optional content
    - String
    - e.g., 'spire', 'decay'

#### i_eat_start = 0.14

* Parameter explanation
    - The minimum value of eat when the program is run

* Optional content
    - float
    - e.g., 0.14, 0.55

#### i_eat_end   = 0.16

* Parameter explanation
    - The maximum value of eat at the end of the program run

* Optional content
    - float
    - e.g., 0.14, 0.55

#### i_eat_step  = 0.01

* Parameter explanation
    - The program is run many times with different eats, and the interval between each different eat

* Optional content
    - float
    - e.g., 0.01, 0.1

#### i_run_times = 1

* Parameter explanation
    - Number of times the program runs with the same eat value

* Optional content
    - int
    - e.g., 1, 10, 53, 100, 3333


#### a_arch_spire = -30

* Parameter explanation
    - The parameter set according to the parametric equation of the Archimedean spiral, which is the intersection of the center of the spiral and the x-axis (the Cartesian coordinate system in which the spiral is located has the source of the particle as the origin)

* Optional content
    - float(Recommend int)
    - e.g., 0, -10, -30, 10

#### b_arch_spire = 5

* Parameter explanation
    - Spacing of different circles in the spiral

* Optional content
    - float(Recommend int)
    - e.g., 5, 8

#### theta_per_time = 5

* Parameter explanation
    - Rotational speed of the spiral

* Optional content
    - e.g., 5, 8
