# Changelog

All notable changes to SCLM will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-09-26

### Changed
- **Renamed EARCP → PACER** (Propagation, Alignment, Coherence, Encapsulation,
  Revision). The old name collided with an unrelated architecture
  (Expert Aggregation with Regret Control and Performance tracking, published
  separately with an arXiv paper) — same acronym, two unrelated inventions.
  `PACERModule` replaces `EARCPModule`; `sclm.pacer` replaces `sclm.earcp`.
- Removed the "(patent pending)" claim from the README — no filing is in
  progress. The dual license (free under $100K revenue, commercial license
  required above) remains the operative protection.

### Fixed
- `SCLMModel.from_pretrained()` now falls back to a legacy
  `earcp_weights.pt` checkpoint file if `pacer_weights.pt` is not found, so
  checkpoints saved before this rename (e.g. pre-v0.1.2 releases) still load
  without re-training or manual renaming.

## [2.0.0] - 2025-12-16

### Added
- **PACER Architecture**: Complete implementation of Propagation, Alignment, Coherence, Encapsulation, Revision
- **SCLMModel**: High-level API for easy usage
- **SCLMModelV2**: Low-level implementation with full control
- **Option B Architecture**: Deep integration variant with attention/FFN injection
- **Edit Mode**: Freeze state for local editing without memory drift
- **Configuration Presets**: Ready-to-use configs for Mistral-7B, LLaMA-7B/13B, Phi-2
- **CLI Interface**: `sclm chat`, `sclm benchmark`, `sclm info` commands
- **Memory Tracker**: Utility for tracking state evolution across turns
- **Comprehensive Tests**: Unit tests for all components
- **Bilingual Documentation**: English and French documentation

### Changed
- Removed LayerNorm from Encapsulation (allows natural state evolution)
- Reduced default alpha_inject from 0.1 to 0.02 (less perturbation)
- Reduced default injection layers from 4 to 2 (better quality)
- Zero-initialized output projections (start with identity)

### Fixed
- State norm stuck at 16.0 due to LayerNorm normalization
- Gibberish generation from over-injection
- Multi-GPU device mismatch errors
- dtype mismatch (float16 vs float32)

## [1.0.0] - 2025-12-01

### Added
- Initial release
- Basic SCLM wrapper
- Simple state injection

---

## Roadmap

### [2.1.0] - Planned
- NEUROGENESIS: Dynamic state dimension growth
- Training scripts for PACER fine-tuning
- Gradio demo application

### [3.0.0] - Future
- Multi-modal state (vision-language)
- Hierarchical state levels
- Unsupervised training objectives
