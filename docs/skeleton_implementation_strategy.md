# Skeleton Implementation Strategy

## Document Purpose

This document defines a strategy for implementing an architectural skeleton before detailed model behavior is developed.

The skeleton is intended to expose system-wide design problems early, especially problems that would otherwise become visible only while implementing individual blocks, layers, functions, or other detailed units. It focuses on responsibility boundaries, dependency direction, interfaces, output ownership, orchestration, extension behavior, and the runtime data boundary.

The skeleton is not intended to prove the numerical correctness of the final model. Detailed formulas, complete feature definitions, production data acquisition, and full calculation behavior are implemented after the skeleton has been accepted.

# 1. Purpose and Problem Definition

## 1.1 Purpose of the Skeleton

The skeleton exists to validate the structure connecting the major parts of the model before detailed behavior is implemented.

Its primary goal is to reduce the likelihood that implementation of one detailed unit later requires structural changes across several unrelated units.

The skeleton should make it possible to review, at an early stage:

- which major responsibilities exist;
- which unit owns each responsibility;
- how dependencies flow;
- what each unit receives and returns;
- how calculated outputs are identified and reused;
- how optional capabilities are represented;
- how new capabilities can be added;
- how complete results are assembled;
- where actual data enters the model;
- whether detailed implementations can later remain local.

## 1.2 Definition of Structural Change

A structural change is a change that crosses established responsibility boundaries and requires coordinated modification of multiple units with different roles.

Examples include:

- implementing a weighted-aggregation block requires changes to feature ownership, stance orchestration, and result assembly;
- implementing a history-dependent block requires the entire execution engine to become stateful;
- adding one output requires editing several hard-coded output registries in unrelated layers;
- adding a new classifier requires stance-name-specific branching in orchestration;
- introducing actual data requires calculation blocks to load files or access external services;
- sharing one feature across multiple stances requires recalculating the feature separately in each stance.

These changes indicate that the skeleton failed to establish a sufficiently stable architectural boundary.

## 1.3 Acceptable Local Implementation Changes

The skeleton is not expected to eliminate every later change.

The following are normally acceptable:

- implementing the internal algorithm of one unit;
- adding focused tests for that unit;
- refining an interface owned by that unit;
- adding configuration fields required by that capability;
- improving local typing or metadata;
- replacing a stub with a real implementation;
- adjusting local error handling;
- adding a new implementation behind an existing interface.

A local interface refinement is acceptable when it does not require unrelated units to change their responsibilities or internal behavior.

## 1.4 Limits of the Skeleton’s Guarantees

The skeleton cannot guarantee that no architectural change will ever be necessary.

It should instead provide reasonable confidence that:

- major dependency directions are correct;
- responsibility ownership is stable;
- detailed implementation can proceed mostly within existing units;
- extension usually adds or replaces local behavior;
- actual data can enter through an established boundary;
- new model declarations do not require redesign of orchestration.

Unexpected domain requirements may still justify later architectural revision. Such revision should be deliberate and identifiable rather than an accidental consequence of implementing one detailed calculation.

# 2. Scope and Design Principles

## 2.1 Structural Completeness Versus Behavioral Completeness

The skeleton should be structurally complete but behaviorally simplified.

Structural completeness means that the major architectural responsibilities and their relationships are represented, including:

- configuration;
- validation;
- specification resolution;
- runtime input;
- execution orchestration;
- feature calculation;
- component calculation;
- classification;
- stabilization;
- stance composition;
- result assembly.

Behavioral simplification means that the internal calculations may use:

- synthetic inputs;
- predetermined outputs;
- trivial placeholder calculations;
- explicit no-op implementations;
- incomplete capability sets that reject unsupported declarations.

The skeleton must represent where behavior belongs without implementing all of that behavior.

## 2.2 Responsibilities Included in the Skeleton

The skeleton should include enough structure to review:

- the model-definition boundary;
- the configuration-to-runtime boundary;
- the source-neutral runtime input boundary;
- the resolved specification;
- execution context and orchestration;
- major semantic execution layers;
- unit interfaces;
- calculation-block interfaces;
- authoritative output ownership;
- dependency resolution;
- calculate-once and reuse behavior;
- optional-block handling;
- unsupported-capability handling;
- complete result construction;
- extension and substitution scenarios.

## 2.3 Detailed Behavior Deferred Until Later

The following may be deferred until after skeleton acceptance:

- complete raw-data acquisition;
- production API integration;
- full historical datasets;
- complete feature formulas;
- actual weighted-sum mathematics;
- complete normalization behavior;
- full smoothing behavior;
- detailed clipping rules;
- full bucket definitions;
- complete hysteresis behavior;
- complete persistence behavior;
- production rule tables;
- final labels and strengths;
- full domain-specific validation;
- numerical regression testing.

A deferred behavior should still have an identified owner and an intended interface when it may affect system structure.

## 2.4 Relationship to the Architecture Contract

The architecture contract remains authoritative for required responsibilities, invariants, and prohibited patterns.

The skeleton translates those architectural requirements into an inspectable implementation structure.

The skeleton review should determine whether the implementation:

- preserves the contract’s responsibility boundaries;
- represents the required execution stages;
- avoids hidden name-based dispatch;
- supports authoritative output ownership;
- prevents accidental recalculation;
- separates configuration, resolution, execution, and results;
- permits later detailed implementation without cross-unit redesign.

The skeleton may reveal an alternative design that appears better than the current contract. Such an alternative is not accepted automatically. It should be reviewed separately and either rejected, implemented as a correction, or adopted through a deliberate contract revision.

# 3. Skeleton Acceptance Model

## 3.1 Locality of Later Implementation Changes

The central acceptance principle is locality of change.

After skeleton acceptance, implementation of a detailed unit should normally modify only:

- that unit;
- its focused tests;
- its owned configuration or specification fields;
- closely related local types or metadata.

If implementation routinely changes several unrelated layers, the skeleton has not achieved its purpose.

## 3.2 Stable Dependency Direction

Dependencies should flow in the intended architectural direction.

A conceptual flow is:

```text
configuration
    ↓
validation and resolution
    ↓
runtime input and execution context
    ↓
feature and component execution
    ↓
classification and stabilization
    ↓
stance composition
    ↓
result assembly
```

Later units may consume outputs from earlier units. Earlier units should not depend on downstream consumers.

In particular:

- calculation blocks should not depend on result presentation;
- feature units should not depend on stance-specific consumers unless explicitly designed as stance units;
- schema validation should not depend on live execution data;
- result assembly should not recalculate model outputs;
- data acquisition should not be embedded inside the pure calculation engine.

## 3.3 Replaceable Internal Implementations

A unit’s consumers should depend on its contract rather than its current stub or algorithm.

Replacing a stub with a real implementation should preserve:

- the unit’s responsibility;
- the semantic meaning of its output;
- its relationship to orchestration;
- downstream ownership assumptions;
- result assembly behavior.

Some local type or metadata refinement may be acceptable, but the replacement should not require unrelated consumers to understand the new algorithm.

## 3.4 Extension Without Orchestration Redesign

The skeleton should demonstrate that supported extension patterns do not require new orchestration branches.

Examples include:

- adding a feature declared through an existing capability;
- adding another component that uses existing blocks;
- changing a weighted calculation from one input to several inputs;
- adding another stance using existing composition capabilities;
- enabling an existing optional block;
- making an existing output available to an additional consumer.

Such extensions may add declarations and local implementations, but they should not require stance-name-specific or component-name-specific control flow.

## 3.5 Conditions Requiring Renewed Architectural Review

Renewed architectural review is appropriate when a proposed change:

- introduces a new responsibility not owned by an existing unit;
- reverses an established dependency;
- requires several unrelated units to change;
- changes authoritative output ownership;
- introduces a second calculation path for an existing concept;
- changes the runtime input boundary;
- changes the completed-result boundary;
- requires a new execution-stage category;
- makes a previously pure layer depend on external I/O;
- introduces a special-case path that cannot be expressed through existing capabilities.

# 4. Architectural Structure and Responsibility Boundaries

## 4.1 Overall System Topology

The system structure describes relationships among major responsibilities.

It does not prescribe one file, class, or function for each responsibility.

The conceptual topology should distinguish:

```text
model definition
    ↓
schema validation
    ↓
resolved specification
    ↓
runtime input
    ↓
execution orchestration
    ↓
semantic calculation layers
    ↓
completed result
```

This topology should be inspectable even when individual calculations remain synthetic.

## 4.2 Semantic Execution Layers

The skeleton should represent the following semantic execution layers where applicable:

1. input resolution;
2. derived-feature calculation;
3. component-score calculation;
4. score or state classification;
5. state stabilization;
6. stance composition;
7. result assembly.

These are semantic responsibilities, not mandatory file boundaries.

Several layers may be implemented in one module when responsibility remains clear. One layer may also contain several substantial units when distinct ownership justifies it.

## 4.3 Dependency Direction

Dependency direction should be explicit and mechanically reviewable where practical.

The structure should prevent:

- downstream units from loading upstream raw inputs;
- classifiers from reconstructing component scores;
- stance composition from recalculating shared features;
- result assembly from interpreting raw configuration;
- consumer-specific behavior from entering shared calculation blocks.

An execution context, dependency registry, or similar mechanism may be used when it helps preserve declared order and output reuse. Such a mechanism should not become an abstraction without a concrete architectural role.

## 4.4 Output Ownership

Every authoritative output should have one owner.

Examples include:

- one owner for each derived feature;
- one owner for each component score;
- one owner for each raw state;
- one owner for each stabilized state;
- one owner for each stance output.

The skeleton should distinguish authoritative outputs from aliases, views, labels, and presentation fields.

Output identities should be explicit enough to detect collisions and prevent two units from claiming the same concept.

## 4.5 Calculate-Once and Reuse Rules

Within one scenario, each authoritative output should be calculated at most once.

Later units should consume stored outputs rather than invoke equivalent calculations again.

The skeleton should demonstrate:

- one feature consumed by multiple components or stances;
- one component output consumed by classification and result assembly;
- one raw state consumed by stabilization;
- one stabilized state consumed by stance composition and result assembly.

The mechanism may use a scenario-local execution context, typed result containers, or another explicit structure. The design goal is authoritative reuse, not a particular implementation technique.

# 5. Unit Contracts and Interfaces

## 5.1 Definition of a Unit

A unit is an independently owned architectural responsibility with an identifiable input, output, dependency set, and implementation boundary.

A unit may be represented by:

- a function;
- a class;
- a group of related functions;
- a service-like object;
- a semantic subsystem.

A unit does not automatically require its own file or class.

The defining property is that its responsibility can be reasoned about and implemented without taking ownership of unrelated behavior.

## 5.2 Unit Categories

The skeleton may contain several categories of units:

### Calculation units

Examples:

- feature operators;
- transformations;
- aggregators;
- classifiers;
- stabilizers;
- rule-composition blocks.

### Orchestration units

Examples:

- dependency resolution;
- execution ordering;
- output registration;
- scenario execution.

### Boundary and adapter units

Examples:

- configuration loading;
- schema validation;
- specification resolution;
- source adapters;
- input assembly.

### Result-construction units

Examples:

- output collection;
- metadata assembly;
- completed-result construction.

Calculation blocks are one category of unit. Not every unit is a calculation block.

## 5.3 Input and Output Contracts

Each important unit contract should identify:

- accepted input types;
- returned output types;
- configuration or specification consumed;
- required execution context;
- missing-value expectations where relevant;
- ordering requirements;
- mutation guarantees;
- output identity and ownership;
- whether the unit is row-local or history-dependent;
- unsupported conditions and failure behavior.

The skeleton may use simplified data, but its interfaces should reflect the expected category and multiplicity of final dependencies.

For example, a multi-input-capable unit may receive a mapping containing only one synthetic input during the skeleton stage. The interface should still remain capable of representing multiple declared inputs later.

## 5.4 Simplified Implementation With Realistic Interfaces

The skeleton may simplify the behavior behind an interface without narrowing the interface to the temporary fixture.

For example:

- a feature unit may receive one synthetic input through a general input mapping;
- a weighted aggregator may return a predetermined series;
- a classifier may return a fixed state sequence;
- a result assembler may construct a real result type from synthetic outputs.

The values may be synthetic. The ownership, types, direction, and semantic distinctions should be real.

## 5.5 Internal Implementation Freedom

A unit’s internal algorithm may remain unspecified during skeleton implementation.

Codex may exercise implementation discretion in areas such as:

- internal function organization;
- local data structures;
- use of frozen dataclasses or typed mappings;
- registry versus direct capability mapping;
- private helper boundaries;
- local validation organization.

Such discretion is acceptable when it does not change architectural responsibility, public contracts, output ownership, or dependency direction.

## 5.6 Replaceability and Locality of Change

A well-designed unit should be replaceable without modifying unrelated consumers.

The skeleton should make it possible to replace:

- a stub feature producer with a real feature implementation;
- a placeholder aggregator with a real weighted calculation;
- a fixed classifier with a configurable classifier;
- a no-op stabilizer with a history-dependent stabilizer;
- a synthetic source adapter with a frozen-data adapter.

The replacement should preserve the unit’s declared role and output meaning.

## 5.7 Optional and Unsupported Capabilities

The skeleton should distinguish three states:

### Implemented capability

The capability has executable behavior, even if minimal.

### Explicit no-op capability

The capability is intentionally absent or disabled and has defined pass-through or omission semantics.

### Unsupported capability

The capability is not yet implemented and must be rejected clearly.

Unsupported declarations should not be silently accepted and routed through placeholder behavior. This avoids overstating the skeleton’s implemented capabilities.

# 6. Calculation Blocks and Stub Policy

## 6.1 Calculation Blocks as Execution Units

A calculation block is a unit that performs a bounded operation within the execution pipeline.

Examples include:

- preparation;
- transformation;
- aggregation;
- score post-processing;
- classification;
- stabilization;
- rule lookup;
- stance composition.

Blocks should be selected by declared capability rather than hidden names such as a particular stance or component.

## 6.2 What Must Be Structurally Real

Even when behavior is stubbed, the following should be real:

- the block’s responsibility;
- its location in the pipeline;
- its input and output contract;
- its specification type;
- its output identity;
- dependency relationships;
- ordering relative to other stages;
- row-local or history-dependent classification;
- unsupported-case behavior;
- integration with orchestration and result assembly.

## 6.3 What May Remain Stubbed

The following may remain simplified:

- mathematical formulas;
- actual weights;
- normalization calculations;
- rolling-window calculations;
- bucket thresholds;
- hysteresis transition logic;
- persistence counters;
- rule-table contents;
- domain-specific labels;
- numerical missing-value policy.

These may be represented by deterministic placeholder behavior as long as the placeholder is not confused with the final implementation.

## 6.4 Synthetic Outputs and Trivial Placeholder Behavior

Permissible placeholder approaches include:

- returning a predetermined synthetic series;
- returning the first supplied input;
- returning a fixture associated with an output identifier;
- mapping every row to a fixed state;
- emitting synthetic outputs required by all downstream units.

A placeholder should preserve output type, shape, identity, and semantic category.

For example, continuous scores, raw states, stabilized states, and labels should remain distinguishable even when their values are artificial.

## 6.5 Explicit No-Op Behavior

Optional stages may have explicit no-op behavior.

Examples include:

- no input smoothing;
- no score smoothing;
- no clipping;
- no stabilization.

The representation may use absence, `null`, or an explicit `none` capability, but its meaning must be unambiguous and validated.

A no-op is different from an unimplemented capability.

## 6.6 Unsupported Behavior and Rejection

When a capability is not implemented, the schema or resolver should reject its declaration.

Examples may include:

- an unsupported transformation method;
- an unsupported classifier family;
- an unsupported stabilization combination;
- an invalid block order;
- an unsupported adjustment stage.

The runtime should not silently ignore unsupported configuration.

## 6.7 Replacement by Detailed Implementations

After skeleton acceptance, real block implementations should replace stubs incrementally.

Each replacement should verify:

- preserved interface meaning;
- preserved output ownership;
- preserved execution order;
- preserved consumer behavior;
- no new unrelated dependency;
- no duplicate authoritative calculation;
- focused numerical and behavioral tests.

# 7. Runtime Data Boundary and Data Introduction Strategy

## 7.1 Purpose of Data in the Skeleton

Data exists during skeleton implementation to exercise architectural boundaries, not to validate the final economic model.

The skeleton should use enough data structure to test:

- time-series flow;
- input identity;
- multi-input capability;
- output reuse;
- ordering;
- metadata propagation;
- input assembly;
- result coherence.

It does not initially require economically realistic values or complete production datasets.

## 7.2 Source-Neutral Runtime Input Contract

The pure execution engine should receive a source-neutral runtime input object, conceptually:

```text
external source
    ↓
source adapter
    ↓
input assembly
    ↓
InputSnapshot
    ↓
execution engine
```

The execution engine should not need to know whether the snapshot came from:

- synthetic fixtures;
- frozen actual data;
- local files;
- APIs;
- a cache;
- another provider.

The runtime input contract should identify the data needed for one coherent scenario.

## 7.3 Simplified Synthetic Inputs

Early skeleton execution may use one or a few artificial time series.

A single synthetic input may be sufficient for one unit’s execution while that unit emits several downstream-required outputs.

The fixture may be minimal, but the interface should not be artificially restricted to one input when multiple inputs are part of the intended contract.

Synthetic inputs should be deterministic and easy to inspect.

## 7.4 Structurally Realistic Data Properties

Before skeleton acceptance, fixtures should represent data properties that may affect architecture, including where relevant:

- ordered time indexes;
- multiple frequencies;
- different observation ranges;
- missing observations;
- source and unit metadata;
- raw-input reuse;
- multi-input feature dependencies;
- scenario-consistent alignment.

These properties may initially be represented with synthetic values.

The goal is to avoid assuming that all inputs have identical dates, frequency, completeness, or ownership.

## 7.5 Frozen Actual-Data Sample

Near the end of the skeleton stage, a small deterministic sample derived from actual data should be introduced.

Its purpose is to verify that actual data can be converted into the accepted runtime input contract without changing unrelated calculation units.

The frozen sample should be:

- reproducible;
- independent of credentials;
- independent of network availability;
- limited in size;
- sufficient to expose important data-boundary properties.

The skeleton stage does not use the sample to prove model accuracy.

## 7.6 Live Production Data After Skeleton Acceptance

Live and complete data integration should normally occur after skeleton acceptance.

This includes:

- API clients;
- credentials and environment variables;
- retry behavior;
- caching;
- complete series inventories;
- full historical ranges;
- source-specific validation;
- production refresh behavior.

These responsibilities should produce the already accepted runtime input boundary rather than modify calculation-block interfaces.

## 7.7 Acceptable Data-Related Refinements

Introducing realistic or frozen actual data may justify local refinements such as:

- adding metadata fields;
- clarifying time-index requirements;
- defining frequency metadata;
- refining missing-observation representation;
- adding a local alignment-result type;
- improving the input assembler.

These are acceptable when changes remain within the data boundary and do not alter unrelated calculation responsibilities.

## 7.8 Data-Related Structural Failure Indicators

The following indicate a structural problem:

- each feature loads its own source data;
- the execution engine depends on credentials or network access;
- alignment logic is duplicated across components;
- stance interfaces change because one source has missing dates;
- result assembly handles source-specific irregularities;
- classifiers need to know source frequencies;
- adding one data source changes unrelated calculation blocks;
- synthetic and actual data require separate execution paths after input assembly.

# 8. Phased Skeleton Implementation

## 8.1 Structural Topology

Establish:

- major responsibilities;
- semantic layers;
- dependency direction;
- configuration and runtime boundaries;
- authoritative output ownership;
- completed-result boundary.

No meaningful numerical calculation is required.

## 8.2 Unit-Contract Establishment

Define the main unit categories and contracts.

Identify:

- accepted inputs;
- produced outputs;
- specification consumed;
- dependencies;
- mutation guarantees;
- row-local or history-dependent behavior;
- unsupported conditions.

The goal is to ensure that detailed algorithms can later be inserted behind stable responsibilities.

## 8.3 Connected Synthetic Skeleton

Connect the main units using deterministic synthetic behavior.

The connected path should demonstrate:

```text
synthetic runtime input
    ↓
stub feature outputs
    ↓
stub component outputs
    ↓
stub classification or stabilization
    ↓
stub stance composition
    ↓
complete result
```

The path should be executable even though its numerical meaning is artificial.

## 8.4 Structural Variation and Substitution Checks

Exercise cases likely to reveal architectural weaknesses:

- one unit producing multiple outputs;
- one output feeding multiple consumers;
- one-input and multi-input specifications;
- row-local and history-dependent interfaces;
- optional block enabled and disabled;
- a stub replaced with another implementation;
- a new declaration added without an orchestration branch;
- duplicate output ownership rejected.

## 8.5 Frozen Actual-Data Boundary Check

Introduce a small frozen actual-data sample through the accepted input boundary.

Verify that:

- source-specific details remain outside calculation blocks;
- input assembly is the main integration point;
- unrelated unit contracts remain unchanged;
- execution and result assembly remain the same;
- synthetic and frozen actual inputs use the same runtime path.

## 8.6 Skeleton Acceptance Review

Before detailed implementation begins, review:

- architecture-contract compliance;
- responsibility clarity;
- dependency direction;
- interface sufficiency;
- output ownership;
- calculate-once behavior;
- extension behavior;
- stub policy;
- unsupported-capability behavior;
- data-boundary behavior;
- indicators of speculative abstraction;
- indicators of hidden special cases.

# 9. Structural Validation Scenarios

## 9.1 One Unit Producing Multiple Outputs

A feature-producing unit may use a simplified input while emitting all outputs required by downstream units.

The scenario should verify that:

- each output has a unique identity;
- downstream units consume only declared outputs;
- result assembly preserves semantic distinctions;
- later real calculation can replace the producer locally.

## 9.2 One Output Consumed by Multiple Units

A shared feature should be consumable by several components or stances without recalculation.

The scenario should verify:

- one authoritative producer;
- stable reuse;
- no consumer-owned copy of the calculation;
- no mutation by consumers.

## 9.3 Single-Input and Multi-Input Declarations

The skeleton should show that a general input contract can represent:

- a direct one-input calculation;
- a one-input explicitly weighted calculation;
- a multi-input weighted calculation.

The actual weighted mathematics may remain stubbed, but the architectural capability and specification distinction should be present.

## 9.4 Row-Local and History-Dependent Blocks

The skeleton should distinguish blocks that operate independently by row from blocks that require ordered historical context.

The history-dependent interface should have access to sufficient ordered data without forcing unrelated row-local blocks to become stateful.

## 9.5 Optional Blocks

At least one optional stage should be tested as:

- enabled;
- explicitly disabled or no-op;
- unsupported where applicable.

The orchestration path should remain clear and deterministic.

## 9.6 Adding Features, Components, and Stances

Extension drills should demonstrate that an additional declaration can use existing capabilities without:

- name-specific dispatch;
- new hard-coded output lists across multiple files;
- recalculation of existing outputs;
- changes to unrelated units.

## 9.7 Replacing Stubs Without Changing Consumers

At least one stub should be replaced with a different deterministic implementation during skeleton validation.

Consumers should continue to use the same semantic contract.

This demonstrates that the unit boundary is real rather than merely descriptive.

## 9.8 Preventing Duplicate Calculation

The skeleton should detect or prevent:

- duplicate output registration;
- repeated calculation of the same authoritative feature;
- separate stance-owned calculations of a shared feature;
- result assembly invoking model logic again.

# 10. Codex Implementation and Review Approach

## 10.1 Codex’s Implementation Role

Codex acts as the implementation agent.

The user and ChatGPT define and evaluate the architectural direction. Codex implements the skeleton within the stated contract and constraints.

Codex is not required to produce a separate architecture proposal before implementation.

## 10.2 Directional Instructions and Permitted Discretion

The implementation prompt should define:

- the skeleton’s purpose;
- architectural invariants;
- required responsibility boundaries;
- required acceptance scenarios;
- prohibited patterns;
- the intended level of behavioral simplification.

It need not prescribe every class, function, helper, or file.

Codex may exercise coding discretion where the contract does not require one particular implementation form.

## 10.3 Required Architectural Invariants

The implementation should preserve at least:

- configuration, resolution, execution, and result separation;
- source-neutral runtime input;
- explicit unit responsibilities;
- capability-driven execution;
- authoritative output ownership;
- calculate-once behavior;
- stable downstream reuse;
- no hidden source access in calculation blocks;
- explicit unsupported-capability handling;
- complete coherent result assembly.

## 10.4 Independent Contract-Conformance Review

Review should not rely only on Codex’s summary.

The implementation should be compared independently against:

- the architecture contract;
- this skeleton strategy;
- stated acceptance scenarios;
- actual dependency direction;
- actual output ownership;
- actual extension behavior.

The review should map important contract clauses to implementation mechanisms.

## 10.5 Violations, Permissible Choices, and Design Improvements

Differences from the expected implementation should be classified as:

### Violation

The implementation conflicts with the contract or skeleton purpose and should be corrected.

### Permissible implementation choice

The implementation differs from an imagined structure but preserves the required responsibility and behavior.

### Potential design improvement

The implementation does not follow the current contract, but the alternative may be architecturally preferable.

A potential improvement should be evaluated separately. It may be rejected, corrected, or adopted through a deliberate contract revision.

# 11. Success and Failure Criteria

## 11.1 Indicators of Successful Structure

The skeleton is working as intended when:

- detailed implementation changes remain local;
- consumers do not depend on stub internals;
- new declarations use existing orchestration;
- shared outputs are reused;
- output ownership is unambiguous;
- result construction remains stable;
- source changes remain outside pure calculation units;
- unsupported behavior fails clearly;
- synthetic and frozen actual data use the same execution path;
- block replacement does not affect unrelated units.

## 11.2 Indicators of Missed Structural Problems

The skeleton has likely missed a structural problem when:

- implementing one block changes several unrelated layers;
- multi-input support changes every caller;
- history-dependent behavior makes the whole engine stateful;
- adding outputs requires editing several hard-coded registries;
- new classifiers require name-based branches;
- shared features are recalculated by consumers;
- actual data leaks source-specific concerns into model units;
- result assembly reconstructs calculations;
- optional blocks require separate orchestration paths.

## 11.3 Acceptable Post-Skeleton Changes

After acceptance, acceptable changes include:

- implementing real formulas;
- replacing placeholders;
- adding focused validation;
- adding block-specific configuration fields;
- refining unit-local types;
- adding tests for numerical and state behavior;
- improving errors within an existing contract;
- extending an existing capability without changing its architectural role.

## 11.4 Changes Requiring Architectural Reconsideration

Architectural reconsideration is required when a change:

- introduces a new semantic layer;
- changes dependency direction;
- changes completed-result ownership;
- changes the runtime input model;
- creates a second authoritative calculation path;
- requires several unrelated units to change;
- introduces a new cross-cutting execution context;
- cannot be expressed through existing extension mechanisms;
- invalidates the locality-of-change acceptance principle.

# 12. Completion Criteria and Transition

## 12.1 Skeleton Completion Checklist

The skeleton is complete when:

- the major system topology is implemented;
- responsibility boundaries are explicit;
- unit contracts are represented;
- major units are connected;
- synthetic execution produces a coherent complete result;
- output ownership is unique;
- authoritative outputs are reused rather than recalculated;
- optional and unsupported behavior are distinguishable;
- structural validation scenarios pass;
- a frozen actual-data sample enters through the accepted runtime boundary;
- actual-data introduction does not change unrelated calculation units;
- known limitations and unsupported capabilities are documented.

## 12.2 Readiness for Detailed Block Implementation

Detailed block implementation may begin when there is reasonable confidence that:

- the block has a stable owner;
- its required context is available through its interface;
- its output has a stable consumer contract;
- replacing its stub should remain local;
- its algorithm does not require a new system-wide responsibility;
- focused tests can be written without reconstructing the whole system.

## 12.3 Transition to Actual Algorithms and Full Capabilities

After skeleton acceptance, capabilities should be implemented incrementally.

A reasonable progression may include:

1. derived-feature operators;
2. direct single-input scoring;
3. generalized weighted aggregation;
4. normalization and transformation;
5. smoothing and clipping;
6. classification;
7. hysteresis and persistence;
8. rule composition;
9. labels and strengths;
10. complete model definitions.

Each implementation should preserve the accepted architecture and include focused validation.

## 12.4 Transition to Production Data Integration

Production data integration should build on the accepted source-neutral input boundary.

The transition may then add:

- production source adapters;
- API and file integration;
- credentials and environment handling;
- caching;
- complete series definitions;
- full historical ranges;
- production alignment and refresh rules.

These additions should populate the existing runtime input contract rather than redefine calculation-unit responsibilities.

# Summary

The skeleton is a structurally complete, behaviorally simplified implementation intended to expose system-wide design problems before detailed calculations are built.

Its success is measured primarily by locality of later change:

```text
implement one detailed unit
    ↓
change that unit and its focused contract
    ↓
leave unrelated units unchanged
```

Synthetic inputs and stub calculations are appropriate during early skeleton work. Interfaces, responsibility boundaries, output identities, dependency direction, and result structure should nevertheless reflect the intended architecture.

Before the skeleton is accepted, structurally realistic fixtures and a small frozen actual-data sample should confirm that the runtime data boundary is not based on unrealistic assumptions. Live production acquisition and full numerical behavior remain later implementation work.
