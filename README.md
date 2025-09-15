# 📡 StreamAnalyzerFor5GSlicing

An open-source extension project under **6G-XR OC2**, delivering AI/ML-based centralized and distributed learning solutions for **5G network slicing** for the UOULU 5GTN testbed.

---

## 🚀 Features

- 🎛 Centralized UE Admission Controller using binary classification
- 🤖 Distributed Multi-Agent UE Scheduler using Deep Reinforcement Learning
- 🔧 Seamless integration with UERANSIM and 5GTN Cumucore 5G Core

---

## 📁 Project Structure

```
/
├── centralized_learning/     # Centralized learning for UE admission control
├── distributed_agents/       # Multi-agent RL-based for UE scheduling
├── 6gxr-system-code/         # 5GTN & UERANSIM integration 
```

---

## 🏁 Getting Started

### 📦 Prerequisites

- Python >= 3.11
- conda

---

## 🔧 Installation & Environment setup

```bash
git clone https://github.com/lamdanetworks/StreamAnalyzerFor5GSlicing.git
cd StreamAnalyzerFor5GSlicing
conda env create -f 6gxr.yml
conda activate 6gxr

```

---

## 🧪 Running the Code

### ➕ Centralized Learning

```bash
cd centralized_learning/src
pip install -r requirements.txt
python 6gxr_admission_controller_trainer.py # (optional follow if you need to train the agent with your own data traces)
python 6gxr_admission_controller.py # To run the agent using the trained model
```

### 🌐 Distributed Agents

```bash
cd distributed_agents
pip install -r requirements.txt
bash run_variations.sh # to collect necessary data for training for different configurations (see the .sh file)
python train.py # to train agents based on the training data 
python sjf.py # to obtain results for the Shortest Job First (SFJ) baseline
python plot.py # to create plots comparing your agents with the SJF basedline and the adjust RL settings in ./env/env.py
```

> 📖 Follow each folder's `README.md` for detailed setup and environment-specific configurations.

---

## 🔐 Access & Support 

For UERANSIM configuration, testbed access and access control variables (e.g. username, hostname, password) needed to access resources i.e. the ones declared as `None` in:
  - `utils.py`
  - `local_scripts/*.py`:
📧 5gtn-admin@oulu.fi and replace `None` with the provided values.

For general technical questions, deployment or operational support:
📧 streamanalyzer-6gxr@lamdanetworks.io

  
---

## 📜 License

Released under [GNU GENERAL PUBLIC LICENSE Version 3](https://github.com/lamdanetworks/StreamAnalyzerFor5GSlicing/blob/main/LICENSE)
 © 2025 [Lamda Networks](https://lamdanetworks.io)

---

## 📚 Citation

If you use this work in your research, please cite it as:

```bibtex
@misc{streamanalyzer2025,
  title={StreamAnalyzerFor5GSlicing: AI-based Resource Optimization for a Cumucore 5GC},
  author={Lamda Networks},
  year={2025},
  howpublished={\url{https://github.com/lamdanetworks/StreamAnalyzerFor5GSlicing}}
}
```
