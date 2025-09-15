# 📡 StreamAnalyzerFor5GSlicing

An open-source extension project under **6G-XR OC2**, delivering AI/ML-based centralized and distributed learning solutions for **5G network slicing** as an extension for the UOULU 5GTN testbed.

---

## 🚀 Features

- 🎛 Centralized UE Admission Controller using Deep Q-Networks (DQN)
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
- `pip install -r requirements.txt`
- Access to UOULU 5GTN (contact `5gtn-admin@oulu.fi`)

---

## 🔧 Installation

```bash
git clone https://github.com/lamdanetworks/StreamAnalyzerFor5GSlicing.git
cd StreamAnalyzerFor5GSlicing
pip install -r requirements.txt
```

---

## 🧪 Running the Code

### ➕ Centralized Learning

```bash
cd centralized_learning
python train.py
```

### 🌐 Distributed Agents

```bash
cd distributed_agents
python train.py
```

> 📖 Follow each folder's `README.md` for detailed setup and environment-specific configurations.

---

## 🔐 Access Configuration

- For 6gxr-system-code: Contact `5gtn-admin@oulu.fi` to receive valid UERANSIM configurations.
- Some variables (e.g., auth tokens, IPs) are declared as `None` in:
  - `utils.py`
  - `local_scripts/*.py`
  
Request values from `5gtn-admin@oulu.fi` and replace `None` with the provided values.

---


## 📬 Contact

- 📧 Email: [streamanalyzer-6gxr@lamdanetworks.io](mailto:streamanalyzer-6gxr@lamdanetworks.io)
- 💡 Project support and troubleshooting available via direct contact.

---

## 📜 License

Released under   GNU GENERAL PUBLIC LICENSE Version 3  © 2025 [Lamda Networks](https://lamdanetworks.io)

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
