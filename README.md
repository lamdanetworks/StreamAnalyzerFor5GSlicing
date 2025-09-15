📡 StreamAnalyzerFor5GSlicing

An open-source extension project under 6G-XR OC2, delivering AI/ML-based centralized and distributed learning solutions for 5G network slicing over the UOULU 5GTN testbed.

🚀 Features

🎛 Centralized UE Admission Controller using Deep Q-Networks (DQN)

🤖 Distributed Multi-Agent Scheduler using Reinforcement Learning

📈 Live bandwidth monitoring via real-time wget-triggered bandwidth logging

🔧 Seamless integration with UERANSIM and Cumucore 5G Core

📁 Project Structure

/
├── centralized_learning/     # Centralized DQN-based learning
├── distributed_agents/       # Multi-agent RL-based scheduling
├── 6gxr-system-code/         # 5GTN & UERANSIM integration (restricted)
├── utils/                    # Shared utilities (jobs, bandwidth, logging)
├── local_scripts/            # Local execution scripts (restricted access)
├── README.md

🏁 Getting Started

📦 Prerequisites

Python >= 3.8

pip install -r requirements.txt

Access to UOULU 5GTN (contact 5gtn-admin@oulu.fi)

🔧 Installation

git clone https://github.com/lamdanetworks/StreamAnalyzerFor5GSlicing.git
cd StreamAnalyzerFor5GSlicing
pip install -r requirements.txt

🧪 Running the Code

➕ Centralized Learning

cd centralized_learning
python train.py

🌐 Distributed Agents

cd distributed_agents
python train.py

📖 Follow each folder's README.md for detailed setup and environment-specific configurations.

🔐 Access & Configuration

For 6gxr-system-code: Contact 5gtn-admin@oulu.fi to receive valid UERANSIM configurations.

Some variables (e.g., auth tokens, IPs) are declared as None in:

utils.py

local_scripts/*.py

distributed_agents/utils.py

Request values from 5gtn-admin@oulu.fi or streamanalyzer-6gxr@lamdanetworks.io.

📊 Sample Output

Episode

Avg Q Value

Loss

Total Reward

16

0.48

0.57

-1.093

17

0.44

0.70

-1.320

📬 Contact

📧 Email: streamanalyzer-6gxr@lamdanetworks.io

💡 Project support and troubleshooting available via direct contact.

📜 License

Released under MIT License © 2025 Lamda Networks

📚 Citation

If you use this work in your research, please cite it as:

@misc{streamanalyzer2025,
  title={StreamAnalyzerFor5GSlicing: AI-based Resource Optimization for 5G Slices},
  author={Lamda Networks},
  year={2025},
  howpublished={\url{https://github.com/lamdanetworks/StreamAnalyzerFor5GSlicing}}
}

download readme.md ready to be used in github
