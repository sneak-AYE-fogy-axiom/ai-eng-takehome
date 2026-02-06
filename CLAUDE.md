# Hex Takehome Assignment

## Overview

This repository is intended for use as a takehome assignment for candidates applying to the AI engineering role at Hex.

They are allowed to use any resources they like, including AI assistants, to help them complete the assignment.

The repository runs on Python 3.13, using Astral software for devex:

- Use `uv` for any and all package management.
  - You should also use `uv` for running one-off commands or exploratory scripts.
- Use `ty` for type checking.
- Use `ruff` for linting.

## Instructions

- The repository is structured into the following packages:
  - `framework`: Contains the core framework for the agent.
  - `tools`: Contains the tools for the agent. The candidate will likely want to add more tools to the framework.
  - `evaluation`: Contains evaluation code, and evaluation data for the agent. There is a separate, held-out test set that will be used to evaluate the candidate's agent against unseen data.
  - `interactive.py`: Is a script that allows the candidate to interact with their agent in a REPL-like environment.
