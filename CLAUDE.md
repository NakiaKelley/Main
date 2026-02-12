# CLAUDE.md

This file provides guidance for AI assistants working with the **Main** repository.

## Repository Overview

- **Owner**: NakiaKelley
- **Status**: New repository — initial setup phase
- **Remote**: Hosted on GitHub (NakiaKelley/Main)

This repository is in its early stages. No source code, build system, or tests have been added yet. Update this file as the project evolves.

## Project Structure

```
Main/
├── CLAUDE.md          # AI assistant guidance (this file)
└── .git/              # Git repository metadata
```

> As files and directories are added, update this section to reflect the current layout.

## Development Setup

No build system or dependencies are configured yet. When they are added, document:

- Language and runtime versions required
- Package manager and install commands
- Environment variables or `.env` file setup
- Database or service dependencies

## Common Commands

<!-- Update this section as the project grows -->

| Task          | Command |
|---------------|---------|
| Install deps  | _TBD_   |
| Run dev server| _TBD_   |
| Run tests     | _TBD_   |
| Lint           | _TBD_   |
| Build          | _TBD_   |

## Code Conventions

When contributing to this repository, follow these guidelines:

- Write clear, descriptive commit messages that explain *why* a change was made
- Keep pull requests focused on a single concern
- Add tests for new functionality
- Follow the linting and formatting rules configured in the project (once added)

## Git Workflow

- The default branch serves as the stable trunk
- Feature work should be done on dedicated branches
- Branches should be kept up-to-date with the base branch before merging

## Architecture Notes

_No architecture decisions have been documented yet. As the project takes shape, record key decisions here (e.g., framework choices, data flow patterns, API design)._

## Testing Strategy

_No test framework has been configured yet. When tests are added, document:_

- _Test runner and assertion library_
- _Directory structure for tests_
- _How to run unit, integration, and e2e tests separately_
- _Coverage requirements_

## AI Assistant Guidelines

When working in this repository:

1. **Read before writing** — Always read existing files before proposing changes
2. **Stay focused** — Only make changes that are directly requested; avoid unnecessary refactoring
3. **Keep it simple** — Prefer the simplest solution that meets the requirements
4. **Update this file** — When adding significant infrastructure (build tools, test frameworks, CI/CD), update the relevant sections of this CLAUDE.md
5. **Don't over-engineer** — Avoid adding abstractions, utilities, or error handling beyond what is needed for the current task
