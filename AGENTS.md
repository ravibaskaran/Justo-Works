<!-- OPENSPEC:START -->
# OpenSpec Instructions

These instructions are for AI assistants working in this project.

Always open `@/openspec/AGENTS.md` when the request:
- Mentions planning or proposals (words like proposal, spec, change, plan)
- Introduces new capabilities, breaking changes, architecture shifts, or big performance/security work
- Sounds ambiguous and you need the authoritative spec before coding

Use `@/openspec/AGENTS.md` to learn:
- How to create and apply change proposals
- Spec format and conventions
- Project structure and guidelines

Keep this managed block so 'openspec update' can refresh the instructions.

<!-- OPENSPEC:END -->

---

## Migration Overview

This project is an **Odoo 15 → Odoo 18 grayfield migration** involving:
- **67 core modules** to validate on Odoo 18
- **79 custom modules** to migrate and modernize
- **~660 models** across all modules
- Full database migration using **OpenUpgrade**

The migration follows a structured **six-phase approach**:

1. **Preparation** - Environment setup, module inventory, backups
2. **Core Module Validation** - Verify all Odoo base modules work on v18
3. **Custom Module Migration** - Update custom modules for Odoo 18 compatibility
4. **Database Migration** - Execute OpenUpgrade to migrate data and schema
5. **Automation, Security & Performance** - Validate cron jobs, access rights, integrations, performance
6. **Post-Migration Validation & UAT** - Comprehensive testing and user acceptance

Each phase has specific validation requirements detailed in the specs under `openspec/specs/odoo/*.md`.

---

## How to Use OpenSpec on This Project

### Reading Order for Context
When working on migration tasks, always follow this reading order:

1. **Start with `openspec/project.md`**
   - Understand the migration context, goals, and constraints
   - Review the six migration phases and their purposes
   - Note the tech stack and principles

2. **Read relevant domain specs**
   - Navigate to `openspec/specs/odoo/*.md` for the phase you're working on:
     - `migration-preparation.md` - Phase 1 requirements
     - `core-module-validation.md` - Phase 2 requirements
     - `custom-module-migration.md` - Phase 3 requirements
     - `database-migration.md` - Phase 4 requirements
     - `automation-security-performance.md` - Phase 5 requirements
     - `post-migration-validation.md` - Phase 6 requirements

3. **Check active OpenSpec changes**
   - Review `openspec/changes/<change-id>/proposal.md` to understand what's being changed
   - Read `openspec/changes/<change-id>/tasks.md` for implementation checklist
   - Read spec deltas in `openspec/changes/<change-id>/specs/` to see specific requirement changes

### Critical Rules for Odoo Code Changes

**⚠️ Do NOT change Odoo code without checking specs first**

Before modifying any Odoo code (core or custom):
- Identify which migration phase this change relates to
- Read the corresponding spec file under `openspec/specs/odoo/`
- Check if an OpenSpec change exists for this work in `openspec/changes/`
- Verify your proposed changes align with the requirements in the specs

**⚠️ Update specs first, then code**

If you need to change behavior:
1. Update the relevant spec file OR create an OpenSpec change proposal
2. Get approval on the spec change
3. Then implement the code changes consistent with the updated specs

**Never guess or deviate from specs.** If requirements are unclear, ask for clarification or propose a spec update.

---

## Pre-Modification Checklist

Before proposing or making any code changes, complete this checklist:

- [ ] **Identify the migration phase and domain**
  - Which of the 6 phases does this relate to?
  - Which domain spec file is relevant (`openspec/specs/odoo/*.md`)?

- [ ] **Read the context**
  - Have you read `openspec/project.md`?
  - Have you read the relevant domain spec file(s)?

- [ ] **Check for active changes**
  - Does an OpenSpec change already exist for this work?
  - If yes, have you read the `proposal.md`, `tasks.md`, and `specs/*`?

- [ ] **Verify alignment**
  - Are your proposed changes consistent with the specs?
  - If behavior needs to change, have you updated the spec first?

- [ ] **Understand constraints**
  - Do you understand the rollback requirements?
  - Are you aware of any regulatory/audit constraints?
  - Are you maintaining data integrity and user permissions?

**Only proceed with code changes after all checklist items are complete.**

---

## Migration-Specific Guidelines

### Module Updates
- Always update `__manifest__.py` version to "18.0.x.x" format
- Replace deprecated decorators (`@api.one`, `@api.multi`)
- Update import paths to match Odoo 18 structure
- Fix XML xpaths and view inheritance patterns
- Update JS to OWL 2 and ES6 syntax

### Data Integrity
- Validate sequences continue from last number
- Check Many2One and One2Many relationships
- Verify computed fields work correctly
- Ensure attachment filestore is intact

### Security
- Test access rights per user role/group
- Validate record rules function correctly
- Check that users see only permitted data

### Testing
- Test with sample records (create, edit, save)
- Run key workflows end-to-end
- Generate reports (PDF/Excel)
- Validate cron jobs execute successfully
- Check integration endpoints (APIs, webhooks)

---

## Questions or Issues?

If you encounter ambiguity, unclear requirements, or conflicts:
1. **Do not guess** - Ask for clarification
2. **Do not bypass specs** - Propose a spec update instead
3. **Do not skip validation** - Run `openspec validate --strict` before committing

Remember: **Specs win over code.** Always keep them in sync.