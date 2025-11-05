# Project Context

## Context
Current: Odoo 15, modules, custom modules, infra basics
Target: Odoo 18, same business behavior + improvements where agreed

## Goals
- Preserve critical business flows
- Clean up technical debt (old hacks, deprecated models, issues/bugs due to old frameworks) and unspported APIs
- Make custom modules compatible with Odoo 18 conventions
- Migrate existing Odoo 15 modules to Odoo 18.

## Constraints
- Rollback strategy
- Regulatory / audit constraints for finance modules.

## Principles
- No code change without an OpenSpec change ID
- Specs must be green (openspec validate) before merging PRs
- Specs always win over code if they disagree; code must be brought back in line

## Spec-driven rules
- Always read `openspec/project.md` before proposing major changes.
- For any change, check `openspec/changes/<change-id>/proposal.md`, `tasks.md`, and `specs/*`.
- Do NOT modify core Odoo modules unless a corresponding OpenSpec change exists.
- If requirements are unclear, update the spec or propose edits there instead of guessing in code.


## Purpose
[Describe your project's purpose and goals]

## Tech Stack
- [List your primary technologies]
- [e.g., TypeScript, React, Node.js]

## Project Conventions

### Code Style
[Describe your code style preferences, formatting rules, and naming conventions]

### Architecture Patterns
[Document your architectural decisions and patterns]

### Testing Strategy
[Explain your testing approach and requirements]

### Git Workflow
[Describe your branching strategy and commit conventions]

## Domain Context
[Add domain-specific knowledge that AI assistants need to understand]

## Important Constraints
[List any technical, business, or regulatory constraints]

## External Dependencies
[Document key external services, APIs, or systems]
