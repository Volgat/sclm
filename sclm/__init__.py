"""
SCLM: Stateful Coherent Language Model
======================================

A library for adding persistent latent memory to transformer language models.

PROPRIETARY SOFTWARE - DUAL LICENSE MODEL
Copyright (c) 2025 AMEFORGE. All Rights Reserved.

Community License (Free):
- Personal & hobbyist projects
- Academic research (non-profit)
- Small businesses (revenue < $100,000 USD/year)

Commercial License Required:
- Organizations with revenue > $100,000 USD/year
- SaaS products (any revenue)
- Redistribution in proprietary products

Contact: info@amewebstudio.com

Features:
---------
- Persistent state across conversation turns
- Entity coherence in long generation
- Edit mode for local changes without global drift
- Lightweight PACER architecture (~2-5% overhead)

Quick Start:
------------
>>> from sclm import SCLMModel, SCLMConfig
>>> 
>>> # Load with a base model
>>> model = SCLMModel.from_pretrained("mistralai/Mistral-7B-v0.1")
>>> 
>>> # Generate with memory
>>> model.reset_state()
>>> output = model.generate("The wizard Elara discovered", max_new_tokens=50)

Author: Mike Amega, AMEFORGE
License: BSL-1.1 (Business Source License)
"""

__version__ = "0.1.3"
__author__ = "AMEFORGE"
__email__ = "info@amewebstudio.com"
__license__ = "BSL-1.1"
__copyright__ = "Copyright (c) 2025 AMEFORGE. All Rights Reserved."

from .config import SCLMConfig
from .model import SCLMModel, SCLMModelV2
from .components import (
    PACERModule,
    StateInjectionLayer,
    Encapsulation,
    CoherenceExperts,
    DriftRevision,
)
from .utils import (
    load_sclm,
    save_sclm,
    count_parameters,
    get_device,
)

__all__ = [
    # Version
    "__version__",
    # Config
    "SCLMConfig",
    # Models
    "SCLMModel",
    "SCLMModelV2",
    # Components
    "PACERModule",
    "StateInjectionLayer",
    "Encapsulation",
    "CoherenceExperts",
    "DriftRevision",
    # Utils
    "load_sclm",
    "save_sclm",
    "count_parameters",
    "get_device",
]
