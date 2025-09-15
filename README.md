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
