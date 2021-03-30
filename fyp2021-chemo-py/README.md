# FYP Supporting Documentation

## Program Function

### Training Model

* Run `run.py` to get the reinforcement-learning trained model
* Models are stored in the model folder
* Training the model takes a lot of time
* The model is currently trained and can be used directly. If you don't want to spend a lot of time training the model you can skip this step

### Agent for Reinforcement Learning

* Run `main.py` to run the Agent **with** reinforcement 
* When the program finishes running, the runtime data associated with the agent will be saved in the root directory as a **.csv** file with the format `result_<time>.csv`.

### General Agent without reinforcement learning

* Run `main_backup.py` to run the Agent **without** reinforcement learning
* When the program finishes running, the runtime data associated with the agent will be saved in the root directory as a **.txt** file with the format `<time>.txt`.

## Installation required


### Important Installation

| No. | Name             | Version | Installation via pip                 |
| --- | ---------------- | ------- | ------------------------------------ |
| 1   | stable_baselines | 2.10.1  | pip install stable_baselines==2.10.1 |
| 1   | tensorflow       | 1.14.0  | pip install tensorflow==1.14.0       |

### Basic Installation
| No. | Name                    | Version | Installation via pip |
| --- | ----------------------- | ------- | -------------------- |
| 1   | argparse                | -       |                      |
| 2   | datetime                | -       |                      |
| 3   | decimal                 | -       |                      |
| 4   | gym                     | 0.18.0  |                      |
| 5   | numpy                   | 1.19.3  |                      |
| 6   | pygame                  | 1.9.6   |                      |
| 7   | math                    | -       |                      |
| 8   | matplotlib              | 3.3.3   |                      |
| 9   | pandas                  | 1.1.5   |                      |
| 10  | pprint                  | -       |                      |
| 11  | stable_baselines        | 2.10.1  |                      |
| 12  | tensorflow              | 1.14.0  |                      |
| 13  | time                    | -       |                      |

## FULL LIST

absl-py==0.12.0
astor==0.8.1
atari-py==0.2.6
cached-property==1.5.2
click==7.1.2
cloudpickle==1.6.0
Corpora==1.0
cycler==0.10.0
Cython==0.29.14
future==0.18.2
gast==0.4.0
gensim==3.8.3
google-pasta==0.2.0
grpcio==1.36.1
gym==0.18.0
h5py==3.2.1
importlib-metadata==3.9.1
joblib==1.0.0
Keras-Applications==1.0.8
Keras-Preprocessing==1.1.2
kiwisolver==1.3.1
llvmlite==0.35.0
Markdown==3.3.4
matplotlib==3.3.3
nltk==3.5
numba==0.52.0
numpy==1.19.3
opencv-python==4.5.1.48
pandas==1.1.5
Pillow==7.2.0
protobuf==3.15.6
pygame==1.9.6
pyglet==1.5.0
pyparsing==2.4.7
python-dateutil==2.8.1
pytz==2020.4
regex==2020.11.13
scikit-learn==0.23.2
scipy==1.5.4
six==1.15.0
smart-open==4.1.0
stable-baselines==2.10.1
tensorboard==1.14.0
tensorflow==1.14.0
tensorflow-estimator==1.14.0
termcolor==1.1.0
threadpoolctl==2.1.0
tqdm==4.55.1
typing-extensions==3.7.4.3
Werkzeug==1.0.1
wrapt==1.12.1
zipp==3.4.1

