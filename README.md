# 🧠 SCLM: Stateful Coherent Language Model

[![PyPI version](https://badge.fury.io/py/saclm.svg)](https://badge.fury.io/py/saclm)
[![SCLM License](assets/sclm_license_badge.png)](LICENSE)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Model-yellow)](https://huggingface.co/amewebstudio/ananke-sclm)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**SCLM** is architecture who adds **persistent latent memory** to transformer  models, enabling better coherence across long conversations and multi-turn generation.

[📖 Documentation](https://sclm.readthedocs.io) | [🇫🇷 Version Française](#-documentation-française) | [📝 Paper](docs/paper.md) | [💼 Commercial Licensing](#-licensing)

---

## ⚖️ Licensing

**SCLM is Proprietary Software** under a dual-licensing model.

### 🆓 Free for:
- ✅ Personal & hobbyist projects
- ✅ Academic research (non-profit)
- ✅ Small businesses (revenue < $100,000 USD/year)

### 💼 Commercial License Required for:
- ❗ Organizations with revenue > $100,000 USD/year
- ❗ SaaS products (any revenue)
- ❗ Redistribution in proprietary products

📧 **Contact:** [amewebstudio35@gmail.com](mailto:amewebstudio35@gmail.com)

---

## ✨ Features

- 🧠 **Persistent Memory**: State that evolves across conversation turns
- 🎯 **Entity Coherence**: Maintains context about characters, places, objects
- ✏️ **Edit Mode**: Make local changes without affecting global memory
- ⚡ **Lightweight**: Only ~2-5% additional parameters (PACER architecture)
- 🔌 **Easy Integration**: Works with any HuggingFace transformer

## 📦 Installation

```bash
# Basic installation
pip install saclm

# With quantization support
pip install saclm[quantization]

# Full installation (all features)
pip install saclm[full]
```

## 🚀 Quick Start

```python
from sclm import SCLMModel

# Load SCLM model from Hugging Face
model = SCLMModel.from_pretrained(
    "amewebstudio/ananke-sclm",     # Pre-trained SCLM model
    load_in_4bit=True  # Optional: 4-bit quantization
)
```

> `ananke-sclm` is a demo checkpoint, not a requirement. `from_pretrained()` accepts
> **any** HuggingFace causal LM — swap in your own model name and it will load with
> a freshly-initialized PACER module. That module starts untrained, so you'll need to
> fine-tune it before the coherence benefit shows up (see [Limitations](docs/paper.md#8-limitations)).
> `ananke-sclm` ships pre-trained specifically so this Quick Start works out of the box.

```python

# Start new conversation
model.reset_state()

# Build context
model.add_context("The wizard Elara lives in Silverwood forest.")
model.add_context("Her familiar is a silver cat named Nimbus.")

# Generate with memory - entities are remembered!
output = model.generate("One day, Elara decided to", max_new_tokens=50)
print(output)
# "One day, Elara decided to take Nimbus on a journey through Silverwood..."
```

## 📊 Architecture: PACER

SCLM uses the **PACER** architecture:

![SCLM Architecture](assets/sclm_architecture_new.png)

```
PACER = Propagation + Alignment + Coherence + Encapsulation + Revision
```

| Component | Function |
|-----------|----------|
| **Encapsulation** | GRU-style state update from hidden states |
| **Alignment** | Cross-attention between state and hidden layers |
| **Revision** | Drift detection and correction |
| **Coherence** | Mixture-of-Experts for consistency |
| **Propagation** | State injection into transformer layers |

```
┌─────────────────┐
│  Hidden States  │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│Encaps.│ │Inject │
└───┬───┘ └───────┘
    │
    ▼
┌───────────┐
│  Latent   │
│   State   │───────► Persists across turns
└───────────┘
```

## 💡 Use Cases

### Interactive Fiction
```python
model.reset_state()

# Build story world
model.add_context("The kingdom of Eldoria was ruled by Queen Lyra.")
model.add_context("The royal advisor Marcus had served for decades.")

# Characters persist in memory
output = model.generate("Marcus approached the throne and said")
# Marcus and Queen Lyra are remembered correctly
```

### Long Conversations
```python
# Memory persists without growing context window
for turn in conversation_turns:
    model.add_context(turn)

# Generate response with all context in memory
response = model.generate("Based on our discussion,")
```

### Creative Writing
```python
# Chapter 1
model.add_context("Chapter 1: Sarah discovered an old map in the attic.")

# Chapter 2 - Sarah is remembered
output = model.generate("Chapter 2: The next morning, Sarah")
```

## ⚙️ Configuration

```python
from sclm import SCLMConfig

# Custom configuration
config = SCLMConfig(
    latent_state_dim=256,        # State vector dimension
    n_experts=2,                  # Number of MoE experts
    state_injection_layers=[8, 16],  # Which layers to inject
    alpha_inject=0.02,            # Injection strength
)

# Use with model
model = SCLMModel.from_pretrained("model-name", config=config)
```

### Presets

```python
from sclm.config import get_preset

# Use optimized presets
config = get_preset("mistral-7b")  # or "llama-7b", "phi-2", "tiny"
```

## 📖 API Reference

### SCLMModel

| Method | Description |
|--------|-------------|
| `from_pretrained(name)` | Load model from HuggingFace |
| `reset_state()` | Reset memory for new conversation |
| `add_context(text)` | Add context to memory |
| `generate(prompt)` | Generate text with memory |
| `freeze_state()` | Freeze memory for editing |
| `save_checkpoint(path)` | Save model checkpoint |

### Properties

| Property | Description |
|----------|-------------|
| `state_norm` | Current state vector norm |
| `state` | Current state tensor |

## 🔬 Benchmarks

| Model | PACER Params | Overhead | Entity Retention |
|-------|--------------|----------|------------------|
| Mistral-7B | 91.7M | 2.4% | 85% |
| LLaMA-7B | 91.7M | 2.4% | 83% |
| Phi-2 | 52.3M | 1.9% | 81% |

## 🛠️ Advanced Usage

### Edit Mode
```python
# Establish context
model.add_context("The sword was blue and ancient.")

# Make edit without changing memory
model.freeze_state()
output = model.generate("The sword was RED")  # State unchanged
model.unfreeze_state()
```

### Memory Tracking
```python
from sclm.utils import MemoryTracker

tracker = MemoryTracker(model)
tracker.add("Context 1")
tracker.add("Context 2")
output = tracker.generate("Prompt")

print(tracker.summary())
tracker.plot_state_evolution()  # Visualize state changes
```

---

# 🇫🇷 Documentation Française

## Qu'est-ce que SCLM ?

**SCLM** (Stateful Coherent Language Model) ajoute une **mémoire latente persistante** aux modèles de langage transformers, permettant une meilleure cohérence dans les longues conversations.

## ⚖️ Licence

**SCLM est un logiciel propriétaire** sous un modèle de double licence.

### 🆓 Gratuit pour :
- ✅ Projets personnels et hobbyistes
- ✅ Recherche académique (non lucratif)
- ✅ Petites entreprises (revenus < 100 000 $ USD/an)

### 💼 Licence commerciale requise pour :
- ❗ Organisations avec revenus > 100 000 $ USD/an
- ❗ Produits SaaS (tout revenu)
- ❗ Redistribution dans des produits propriétaires

📧 **Contact :** [amewebstudio35@gmail.com](mailto:amewebstudio35@gmail.com)

## Installation

```bash
pip install saclm
```

## Démarrage Rapide

```python
from sclm import SCLMModel

# Charger le modèle SCLM depuis Hugging Face
model = SCLMModel.from_pretrained(
    "amewebstudio/ananke-sclm",
    load_in_4bit=True
)

# Nouvelle conversation
model.reset_state()

# Construire le contexte
model.add_context("Le sorcier Élara vit dans la forêt de Boisargent.")
model.add_context("Son familier est un chat argenté nommé Nimbus.")

# Générer avec mémoire
output = model.generate("Un jour, Élara décida de", max_new_tokens=50)
print(output)
```

## Architecture PACER

| Composant | Fonction |
|-----------|----------|
| **Encapsulation** | Mise à jour de l'état style GRU |
| **Alignement** | Cross-attention état ↔ hidden |
| **Révision** | Détection et correction de dérive |
| **Cohérence** | Mixture d'Experts (MoE) |
| **Propagation** | Injection dans les couches |

---

## 📝 Citation

```bibtex
@article{amega2025sclm,
  title={SCLM: Stateful Coherent Language Models with PACER Architecture},
  author={Amega, Mike},
  year={2025},
  note={AMEFORGE - Proprietary}
}
```

## 📄 License

**Business Source License 1.1 (BSL-1.1)** - See [LICENSE](LICENSE) for details.

Copyright (c) 2025 AMEFORGE. All Rights Reserved.

## 👤 Author

**Mike Amega** - AMEFORGE  
📧 [amewebstudio35@gmail.com](mailto:amewebstudio35@gmail.com)  
🔗 [github.com/Volgat](https://github.com/Volgat)

---

## 💼 Commercial Licensing

For commercial licensing inquiries, enterprise support, or custom development:

📧 **Email:** [amewebstudio35@gmail.com](mailto:amewebstudio35@gmail.com)

### Commercial Benefits:
- ✅ Legal compliance for enterprise use
- ✅ Priority technical support
- ✅ Right to redistribute
- ✅ Warranty and indemnification
- ✅ Custom feature development
