# CLAUDE.md

This file provides guidance for AI assistants working with the **Main** repository.

## Repository Overview

- **Owner**: NakiaKelley
- **Remote**: Hosted on GitHub (NakiaKelley/Main)

This repo holds materials for **two separate organizations**. Keep them strictly separated.

## Two organizations — DO NOT COMMINGLE

### 1. We Serve Your City (nonprofit)
Also referred to as **Citizens Coffee and Catering** or **Citizens Catering**. Nonprofit organization with its own EIN/TIN (TIN 92-1363048).

**All nonprofit files live in `we-serve-your-city/`** — never at the repo root, never mixed with Citizens Products files. Current set:
- `*_SOP.md`, `*_SOP.docx` — kitchen standard operating procedures
- `*_RecipeCard.docx`, `recipe_card_*.txt`, `GoldenHour_RecipeCard.docx`, `HarvestBowl_RecipeCard.docx`, `Strawberry_Fields_Salad_Recipe_Card.docx`
- `CC_GrabAndGo_Week11_*` — weekly grab-and-go workbook
- `Citizens Catering_Transaction List.xlsx`
- `05 TIN 92-1363048 (CC).pdf`

### 2. Citizens Products (for-profit CPG startup)
A net-new for-profit CPG food & beverage company. Separate entity, separate EIN, separate IP, separate brand.

**All Citizens Products files live in `citizens-products/`** — never at the repo root, never mixed with nonprofit files.

### Separation rule (enforced)

When working on either organization:

1. **Do not read, quote, summarize, or use the other organization's files as inputs.** Nonprofit recipes, customers, transactions, EIN, and brand do not flow into Citizens Products materials, and vice versa.
2. **Do not cross-reference brands.** "Citizens Catering," "Citizens Coffee and Catering," and "We Serve Your City" must not appear in any Citizens Products artifact. "Citizens Products" must not appear in any nonprofit artifact.
3. **Refuse requests that would commingle assets** (e.g., "use the nonprofit's transaction data to validate Citizens Products demand"). Commingling a nonprofit and a for-profit creates legal, tax, and IP risk and must be handled by counsel.
4. **Route every new file to the right place.** Citizens Products → `citizens-products/`. Nonprofit → `we-serve-your-city/`. Nothing organization-specific belongs at the repo root.
5. **The `cpg-startup-advisor` subagent works on Citizens Products only.** Do not invoke it for nonprofit work.

## Project Structure

```
Main/
├── CLAUDE.md                       # AI assistant guidance (this file)
├── .claude/agents/                 # Claude Code subagents
│   └── cpg-startup-advisor.md      # Citizens Products advisor (for-profit only)
├── citizens-products/              # Citizens Products (for-profit) — all files here
└── we-serve-your-city/             # We Serve Your City / Citizens Coffee and Catering (nonprofit)
```

## Code Conventions

- Write clear, descriptive commit messages that explain *why* a change was made
- Keep pull requests focused on a single concern
- Never put Citizens Products and nonprofit changes in the same commit

## Git Workflow

- The default branch serves as the stable trunk
- Feature work should be done on dedicated branches
- Branches should be kept up-to-date with the base branch before merging

## AI Assistant Guidelines

When working in this repository:

1. **Confirm which organization the request is for** before reading or writing files. If unclear, ask.
2. **Read before writing** — always read existing files before proposing changes (within the correct organization's scope).
3. **Stay focused** — only make changes that are directly requested; avoid unnecessary refactoring.
4. **Keep it simple** — prefer the simplest solution that meets the requirements.
5. **Update this file** when adding significant infrastructure or when the file/folder layout for either organization changes.
6. **Don't over-engineer** — avoid abstractions, utilities, or error handling beyond what is needed.
