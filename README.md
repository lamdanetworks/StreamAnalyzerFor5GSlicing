# 📡 StreamAnalyzerFor5GSlicing

**6G-XR OC2 Extension Project – Open Source Release**

StreamAnalyzerFor5GSlicing is an AI-enhanced reinforcement learning framework for UE admission control and scheduling in real 5G network slicing scenarios. Developed and validated on **UOULU’s 5GTN testbed**, this system integrates centralized and distributed learning agents for network resource optimization.

---

## 📁 Project Structure

| Folder | Description |
|--------|-------------|
| `6gxr-system-code/` | Core integration with real network functions. Requires UERANSIM configuration for 5GTN. |
| `centralized_learning/` | Centralized Deep RL-based UE admission control agent. |
| `distributed_agents/` | Multi-agent distributed scheduling with reinforcement learning. |

> 🔐 Access to certain configuration variables (marked as `None`) in `util.py` and `local_scripts/*.py` requires credentials—see **Access & Support** below.

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/lamdanetworks/StreamAnalyzerFor5GSlicing.git
cd StreamAnalyzerFor5GSlicing

**###2. Set up Python environment **
```bash
conda create -n 6gxr python=3.11
conda activate 6gxr
pip install -r centralized_learning/requirements.txt if training/running the centralized agent for UE admission control.
pip install inside distributed_agents/ if training/running agent for distributed UE scheduling.

---

**## 🚀 Running the Code
**
For Centralized Learning
bash
Copy
Edit
cd centralized_learning
python train.py
For Distributed Agents
bash
Copy
Edit
cd distributed_agents
python train.py
Follow each folder's README.md for detailed instructions.

## 🔐 Access & Support
For UERANSIM configuration and testbed access:
📧 5gtn-admin@oulu.fi

## For access control variables (e.g. username, hostname, password):
📧 5gtn-admin@oulu.fi

## For general technical or deployment support:
📧 streamanalyzer-6gxr@lamdanetworks.io

### 📜 License
Licensed under MIT License (or adapt based on actual license used).

### 📣 Citation / Attribution
If you use this code in your research or project, please cite our 6G-XR OC2 contribution and reference:

“StreamAnalyzerFor5GSlicing: Reinforcement Learning Agents for 5G UE Admission and Scheduling in Sliced Networks – 6G-XR OC2 Extension Project, 2025.”

### 🤝 Acknowledgements
This work has been developed as part of the 6G-XR Open Call 2, under the SNS JU Horizon Europe initiative with the support of our UOULU Mentor and his technical team.
Testbed access and validation were supported by University of Oulu’s 5GTN.

