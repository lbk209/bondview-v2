# Working Model Contracts, Configuration, and Reuse for Bondview v2

> **Status: Working document.**
>
> This document collects current design ideas about model configuration, validation, runtime specification, result boundaries, authoritative ownership, and reuse. These concepts are derived from the v2 architecture discussion and implementation lessons from the previous Bondview project. They are not yet a detailed v2 schema or API contract.

## 1. Model Definition Framework

The current working framework separates the architectural concept of model definition from its file representation.

```text
Model Configuration
        ↓
represented in
        ↓
YAML
```

### Model Configuration

**Model Configuration** is the declarative definition of model-specific structure and parameters consumed by Bondview calculation.

Possible contents include:

- input/feature definitions;
- component definitions;
- transformation settings;
- classification thresholds and states;
- stabilization settings;
- rule mappings;
- macro-constraint rules;
- scoring parameters;
- labels;
- output definitions;
- relationships among model concepts.

The exact contents may change as the stance model evolves without changing the architecture of Model Configuration itself.

### YAML

**YAML** is the current representation/serialization format for Model Configuration.

The distinction is important:

```text
Model Configuration = architectural concept
YAML                = file representation
```

A future representation change would not necessarily change the model-definition architecture.

---

## 2. Configuration Processing

The working runtime contract is:

```text
Model Configuration (YAML)
        ↓
Configuration Schema
        ↓
Resolved Model Specification
        ↓
Runtime Calculation
```

### Configuration Schema

The **Configuration Schema** validates whether Model Configuration is structurally and semantically acceptable.

Its purpose is to prevent runtime code from silently repairing, guessing, or inventing missing model structure.

Potential responsibilities include:

- required sections;
- valid names/references;
- supported operators;
- allowed state vocabularies;
- rule-table validity;
- output uniqueness;
- numerical constraints;
- relationship consistency.

The exact schema remains module-specific and is not defined here.

### Resolved Model Specification

The **Resolved Model Specification** is the validated, explicit runtime representation produced from Model Configuration before calculation.

Its purpose is to avoid repeated ad hoc interpretation of loosely structured YAML throughout runtime execution.

Conceptually, it should make things such as the following explicit:

- selected operator/capability;
- validated input references;
- declared ordering;
- optional settings normalized into explicit runtime values;
- classification contracts;
- rule mappings;
- output identities.

The exact implementation may use dataclasses, typed mappings, or another explicit structure.

---

## 3. What Can Be Fixed Before the Stance Model Is Final

The model's economic contents may still change:

```text
feature names
component names
number of components
state labels
thresholds
smoothing choices
normalization choices
rule cases
score scales
macro-constraint tables
output fields
```

That does **not** prevent the higher-level configuration framework from being defined now.

The following concepts can therefore be treated as stable working vocabulary:

```text
Model Configuration
Configuration Schema
Resolved Model Specification
```

What remains provisional is the detailed schema and concrete configuration content.

---

## 4. Authoritative Ownership

Each derived concept should have one authoritative owner.

Examples:

```text
one feature definition
one component calculation
one classified state
one stance output
```

If another consumer needs the same meaning, it should use the authoritative capability or output rather than recalculate an equivalent concept independently.

This principle applies across:

- stance calculation;
- historical diagnostics;
- visualization;
- ETF selection;
- future consumers.

### Example

Incorrect:

```text
Stance Calculation
    └── calculates spread percentile

Diagnostics
    └── independently recalculates spread percentile
```

Preferred:

```text
authoritative spread-percentile calculation
              ↓
      ┌───────┴────────┐
      ↓                ↓
Stance Calculation  Diagnostics
```

The same raw series may legitimately be used by more than one calculation when the derived meanings are different. The rule concerns duplicated **derived meaning**, not exclusive ownership of raw data.

---

## 5. Capability Reuse

Reuse should be expressed as a system rule rather than through names such as `SharedX`.

### Principle

> When an existing capability already provides the required semantics, later consumers reuse that capability rather than implement equivalent logic independently.

Examples of capabilities that may become reusable include:

- Feature Calculation;
- Component Calculation;
- State Classification;
- State Stabilization;
- rule-case construction/lookup mechanics;
- generic constraint application;
- Historical Context Preparation.

A capability does not need `shared` in its name merely because more than one consumer uses it.

### Extraction on actual reuse

Do not create speculative generic frameworks simply because two future paths might look similar.

A useful default is:

```text
first real use
    ↓
implement clear capability
    ↓
second semantically equivalent use appears
    ↓
reuse or extract existing behavior
```

The important part is that the second consumer must not create a parallel implementation when the existing behavior is already authoritative.

---

## 6. Historical Context Preparation

Previous implementation experience showed that historical-context logic is particularly vulnerable to accidental duplication.

For v2, the preferred concept is:

### Historical Context Preparation

> A capability that prepares historical context from authoritative model outputs or accepted historical inputs for diagnostic use.

It is not called `Shared Historical Context Layer` because reuse is already a system rule.

```text
Historical Context Preparation
          ↓
    Historical Context
          ↓
       Diagnostics
```

If several diagnostic paths need the same prepared history:

```text
Historical Context Preparation
        ├── Diagnostic A
        ├── Diagnostic B
        └── Visualization
```

They reuse the capability rather than implement parallel history-building logic.

Historical Context must remain explanatory. It must not become an alternative calculation path that reconstructs the stance model differently.

---

## 7. Result Boundaries

The architecture should generalize the idea of a formal result interface without forcing every module into one generic result class.

### Result Boundary

A **Result Boundary** is a formal interface through which one responsibility exposes authoritative outputs to another consumer.

### Result Contract

A **Result Contract** defines the semantics and required contents of a particular Result Boundary.

Example:

```text
Stance Calculation
        ↓
Bond-Exposure Stance Set
        ↓
ETF Selection
```

The Bond-Exposure Stance Set is already a concrete result boundary.

Other concrete result structures should be designed when their consumers and required semantics are clear.

Potential examples:

```text
Stance result structure
ETF selection result structure
diagnostic report/output structure
```

These should not automatically inherit from a speculative `BaseResult` or `GenericResult`.

---

## 8. Downstream Consumption Rule

Downstream modules should consume formal result boundaries rather than reconstruct upstream concepts from internal implementation details.

Preferred:

```text
Stance Calculation
        ↓
formal stance outputs
        ↓
ETF Selection
```

Avoid:

```text
ETF Selection
        ↓
loads raw rates/macro data
        ↓
recreates Duration/Credit/Curve logic
```

Diagnostics may need more explanatory detail than ETF Selection. This creates a legitimate design question about how much authoritative intermediate information should be retained.

A possible future concept is a calculation trace or explanatory result structure containing items such as:

- features;
- component values;
- raw/stabilized states;
- rule cases;
- core stance;
- macro-constraint effect;
- final stance;
- metadata.

The name and exact contract are intentionally not fixed here.

---

## 9. Separation of Model Structure and Runtime Mechanics

The general working principle is:

```text
Model Configuration
defines model-specific choices

Runtime code
implements reusable mechanics
```

Model-specific choices may include:

- which features/components exist;
- which inputs they use;
- thresholds;
- labels;
- rule mappings;
- macro-constraint cases;
- score/output rules.

Runtime mechanics may include:

- transformations;
- smoothing;
- normalization;
- aggregation;
- classification;
- stabilization;
- rule lookup;
- constraint application;
- result construction.

This separation should not become dogmatic. A genuinely new economic relationship may require a new explicit capability, but the capability should have a clear contract and should not be hidden behind stance-name-specific branching.

---

## 10. Current Working Principles

1. **Model Configuration is an architectural concept; YAML is its current representation.**
2. **Configuration Schema validates the model contract before runtime calculation.**
3. **Resolved Model Specification provides an explicit runtime form.**
4. **Each derived meaning has one authoritative owner.**
5. **Equivalent later consumers reuse authoritative capabilities or outputs.**
6. **Reuse is a rule, not a reason to prefix capability names with `shared`.**
7. **Historical Context Preparation is a reusable capability inside the diagnostic domain, not a second model.**
8. **Result Boundary / Result Contract are general interface concepts; concrete results are defined individually.**
9. **Downstream modules consume formal outputs rather than reconstruct upstream logic.**
10. **Detailed schema fields, output objects, and operator sets remain open until the corresponding lower-level contracts are designed.**
