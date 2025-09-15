# 📡 StreamAnalyzerFor5GSlicing

An open-source extension project under **6G-XR OC2**, delivering AI/ML-based centralized and distributed learning solutions for **5G network slicing** for the UOULU 5GTN testbed.

---

## 🚀 Features

- 🎛 Centralized UE Admission Controller using binary classification
- 🤖 Distributed Multi-Agent UE Scheduler using Deep Reinforcement Learning
- 📈 Live bandwidth monitoring via real-time wget-triggered bandwidth logging
- 🔧 Seamless integration with UERANSIM and Cumucore 5G Core

---

## 📁 Project Structure

```
/
├── centralized_learning/     # Centralized DQN-based learning for UE admission control
├── distributed_agents/       # Multi-agent RL-based for UE scheduling
├── 6gxr-system-code/         # 5GTN & UERANSIM integration 
```

---

## 🏁 Getting Started

### 📦 Prerequisites

- Python >= 3.8

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
python train.py
python 6gxr_admission_controller.py
```

### 🌐 Distributed Agents

```bash
cd distributed_agents
pip install -r requirements.txt
python train.py
```

> 📖 Follow each folder's `README.md` for detailed setup and environment-specific configurations.

---

## 🔐 Access & Support 

For UERANSIM configuration and testbed access:
📧 5gtn-admin@oulu.fi

For access control variables (e.g. username, hostname, password) i.e. the ones declared as `None` in:
  - `utils.py`
  - `local_scripts/*.py`:
📧 5gtn-admin@oulu.fi and replace `None` with the provided values.

For general technical or deployment or operational support:
📧 streamanalyzer-6gxr@lamdanetworks.io

  
---

## 📜 License

Released under [GNU GENERAL PUBLIC LICENSE Version 3]  (https://github.com/lamdanetworks/StreamAnalyzerFor5GSlicing/blob/main/LICENSE) © 2025 [Lamda Networks](https://lamdanetworks.io)

---

## 📚 Citation

If you use this work in your research, please cite it as:

```bibtex
@misc{streamanalyzer2025,
  title={StreamAnalyzerFor5GSlicing: AI-based Resource Optimization for 5G Slices},
  author={Lamda Networks},
  year={2025},
  howpublished={\url{https://github.com/lamdanetworks/StreamAnalyzerFor5GSlicing}}
}
```
