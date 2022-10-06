# kindo

Kindo is a reinforcement learning high-level API enabling developers and analysts to use [Stable Baselines 3](https://github.com/DLR-RM/stable-baselines3) and [TF-Agents](https://github.com/tensorflow/agents) algorithms.

[Stable Baselines 3](https://github.com/DLR-RM/stable-baselines3) is powered by [PyTorch](https://github.com/pytorch/pytorch).
[TF-Agents](https://github.com/tensorflow/agents) is powered by [Tensorflow 2.X](https://github.com/tensorflow/tensorflow) \
Kindo enables to train models using both Tensorflow 2.X and PyTorch deep learning frameworks.


## Main features
 - [x] Training algorithms from both tf_agents and stable_baselines3 packages
 - [x] Monitoring and plotting training history, saving it in a consistent format
 - [x] stable_baselines3 similar callbacks for both stable_baselines3 and tf_agents
 - [x] Open AI gym environments compatibility
 - [ ] Open AI gym environment from `.csv` file creation
 - [ ] Bandit problems support

## Installation
### Prerequisites

Kindo requires python 3.8+

### Install using pip
`pip install git+https://github.com/NEU-AI-Skunkworks/kindo.git@master`

## Important Information

If you use conda environment, and your kernel was killed with an error \
`OMP: Error #15: Initializing libiomp5.dylib, but found libomp.dylib already initialized.` \
Check out this [stackoverflow question](https://stackoverflow.com/a/54533223)

## Examples
Kindo code example notebook is provided [here](examples/kindo_example.ipynb)
