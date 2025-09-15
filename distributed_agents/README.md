This folder contains the necessary files to train and test agents UPF500 and UPF250, as they are declared in the environment file ./env/env.py

To train the agents, run the following command:

```python train.py

This trains the two agents and stores their best model (the two agents are equal in our environment thus there is not need for a separate best model per agent) inside folder 'best_model'.

You may then use the file ./best_model/best_model.pth to run your agents at realtime and/or for testing the agents, compare them with baselines, etc.

To test agent  UPF500, simply run python test_upf500.py. This will provide you step by step logs of all the important steps performed by the agent. To capture the logs you may use 'python test_upf500.py > log.test.upf500.log'.


To test agent  UPF500, simply run python test_upf500.py. This will provide you step by step logs of all the important steps performed by the agent. To capture the logs you may use 'python test_upf500.py > log.test.upf500.log'.

Note that we assume that 100 episodes (i.e. epoques) have been used to derive the best trained model when running 'python train.py'. If you would like to run the training for more episodes please edit the file train.py, replace the relevant variable 'num_episodes' in line 109 of the file and save the file. Then, run 'python train.py' to train your environment for your requested number of episodes.

To run the Shortest Job First baseline, run the command 'python sjf.py'. This will run SJF for 1 episode and will store the results in file "csvs/sjf_episode_rewards.csv". For more episodes, please replace the variable num_episodes in line 121 of the file.

Note that to compare how well your agents behave against SJF, run the commands 'python train.py' and 'python sjf.py' for the same number of episodes. Then you can see the obtained rewards per episode by plotting using the command 'python plot.py'.



