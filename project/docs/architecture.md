# Manufacturing Orchestrator — Architecture

## Overview

This project implements a multi-agent system for manufacturing data analysis.

The system executes tasks through a structured pipeline:

Planner → Executor → Critic → Loop

It supports:
- local data processing (Scenario 1)
- API-based processing (Scenario 2)
- failure injection and recovery
- dynamic programming optimization
- concurrent execution
- GUI visualization



## Core Components

### 1. Planner

The planner generates a valid sequence of actions using a backtracking algorithm.

Features:
- dependency-aware planning
- pruning of invalid branches
- support for multiple scenarios



### 2. Executor

The executor runs each tool action with strict validation.

Responsibilities:
- input validation
- execution of tools
- error handling
- storing results in context



### 3. Critic

The critic validates outputs and enforces safety rules.

Checks include:
- schema validation
- logical consistency
- safety constraints

The critic can:
- approve execution
- reject invalid results
- stop execution safely



### 4. Agent Loop

The loop manages execution flow.

Features:
- bounded steps
- retry mechanism
- failure handling
- logging of each step



## Tools Layer

The system uses modular tools:

- `csv_tools` → load local CSV data
- `kpi_tools` → compute KPIs
- `report_tools` → generate reports
- `http_tools` → simulate API calls
- `indicator_tools` → validate and transform API data
- `safety` → enforce security rules



## Scenarios

### Scenario 1 

Pipeline:
CSV → KPIs → Critic → Report

### Scenario 2 

Pipeline:
API → Validation → Transformation → Report



## Failure Injection

The system supports multiple failure modes:

- wrong file path
- timeout
- HTTP 429 (rate limit)
- invalid JSON
- transformation error

The system:
- detects errors
- retries when possible
- stops safely when needed



## Recovery Mechanism

Fallback strategy:
- if primary API fails
- switch to backup endpoint



## Dynamic Programming (DP)

The planner uses memoization to avoid recomputation.

Features:
- cache of previous plans
- cache hit ratio tracking
- performance improvement



## Concurrency

The system supports parallel execution.

Validated with:
- multiple concurrent runs
- isolated contexts
- no state leakage



## Observability

The system logs all events:

- run_id for each execution
- step-level logs
- structured JSON logs
- redaction of sensitive data



## GUI

The graphical interface provides:

- scenario selection
- failure injection control
- execution results
- plan visualization
- timeline (Plan → Act → Observe → Critique)
- tool-call inspector
- safety panel
- metrics (success rate, recovery rate, DP stats)



## Conclusion

The system is modular, robust, and extensible.

It demonstrates:
- multi-agent orchestration
- safe execution
- fault tolerance
- performance optimization