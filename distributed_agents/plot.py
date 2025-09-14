import matplotlib.pyplot as plt
import csv

def load_rewards(csv_path):
    episodes, rewards = [], []
    with open(csv_path, mode="r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            episodes.append(int(row["Episode"]))
            rewards.append(float(row["TotalReward"]))
    return episodes, rewards

# Load both logs
episodes1, rewards1 = load_rewards("csvs/dqn_episode_rewards.csv")
episodes2, rewards2 = load_rewards("csvs/sjf_episode_rewards.csv")  

# Plot
plt.figure(figsize=(10, 6))
plt.plot(episodes1, rewards1, label="Deep RL", marker='o', linewidth=2, markersize=4)
plt.plot(episodes2, rewards2, label="SJF", marker='s', linewidth=2, markersize=4)

# Formatting
plt.title("Episode Rewards Comparison between DeepRL and SJF", fontsize=14)
plt.xlabel("Episode", fontsize=12)
plt.ylabel("Total Reward", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

