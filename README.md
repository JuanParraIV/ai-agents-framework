# AI Agents Framework — BDD-First Delivery

A set of Claude Code subagents that turn raw JIRA issues into shipped features following a **BDD-first** workflow. Each agent has a single responsibility and hard boundaries, so QA defines *what* before Dev writes *how*.

## The pipeline

```
            ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
  raw JIRA  │ product-analyst  │      │ qa-bdd-engineer  │      │    developer     │  PR for
  issue ──▶ │                  │ ──▶  │                  │ ──▶  │                  │ ──▶ human
            │ raw issue →      │      │ story → .feature │      │ .feature → code  │     merge
            │ User Story +     │      │ + step skeletons │      │ (make tests pass)│
            │ Gherkin AC +     │      │ (pending)        │      │                  │
            │ [BDD][DEV][QA]   │      │                  │      │                  │
            └──────────────────┘      └──────────────────┘      └──────────────────┘
                                              │                         ▲
                                              └── [BDD] sub-task "Done" ─┘
                                                  gates the developer
```

1. **product-analyst** — reads raw issues, writes testable User Stories with Gherkin Acceptance Criteria, creates `[BDD]`/`[DEV]`/`[QA]` sub-tasks. Stories land in `AI-draft` for human review.
2. **qa-bdd-engineer** — turns the Gherkin AC into executable `.feature` files and step-definition **skeletons** (pending). The `.feature` becomes the immutable contract.
3. **developer** — implements production code + the pending step definitions until all scenarios pass, then opens a PR (never merges).

## The contract

> The `.feature` file IS the specification. If it's not in the feature file, it doesn't get implemented. If it IS, it MUST be implemented.

The **BDD-First Gate** is a hard requirement: the developer agent refuses to start until the `[BDD]` sub-task is `Done` and step definitions exist.

## Agents

| Agent | Responsibility | Writes to | Never touches |
|-------|----------------|-----------|---------------|
| `product-analyst` | Refine issues → stories + Gherkin AC | JIRA (stories, sub-tasks, links) | source, `.feature`, assignees |
| `qa-bdd-engineer` | Stories → `.feature` + step skeletons | `features/`, `steps/` | source code, parent story |
| `developer` | Make tests pass | source code, step impls | `.feature` files, protected branches |

## Setup

The agents reach real systems through two MCP servers, configured in [`.mcp.json`](./.mcp.json):

- **`atlassian`** (JIRA) — [`mcp-atlassian`](https://github.com/sooperset/mcp-atlassian) via `uvx`.
- **`github`** — the remote [GitHub MCP server](https://github.com/github/github-mcp-server) (branches/PRs for the issue→story→`.feature`→PR flow).

Credentials are injected via environment (`${VAR}`) — **never commit secrets** (`CLAUDE.md` §5). Copy `.env.example` to `.env`, fill in the four values, load them, and relaunch:

```bash
cp .env.example .env          # then edit .env with real tokens
set -a; source .env; set +a   # export JIRA_* and GITHUB_TOKEN
claude                        # MCP reads the env at startup
```

> 📖 **Full step-by-step** (where to get each token, required scopes, direnv setup, verification with `/mcp`, troubleshooting): [`docs/MCP-SETUP.md`](./docs/MCP-SETUP.md).

Requires [`uv`](https://docs.astral.sh/uv/) (`uvx` runs `mcp-atlassian`). Approve both servers on first launch with `/mcp` in Claude Code.

## Usage

Invoke an agent by intent (Claude Code routes by the `description` / trigger phrases) or explicitly:

```
> refinar backlog del proyecto PROJ
> generate BDD tests for PROJ-123
> implement story PROJ-123
```

## Conventions

- Stories created in `AI-draft`, labeled `ai-generated` + `needs-review`.
- Each agent transitions only its own sub-task, never the parent story.
- Branches: `feature/PROJ-XXX-short-description`. Commits: Conventional Commits + `Jira: PROJ-XXX`.
- PRs are created for human merge; agents never merge their own PRs.

## Skills (`.claude/skills/`)

Organized by domain. Built so far (F1–F3 core):

- `product/` — `story-refinement`
- `dev/` — `code-review-security`, `implement-from-bdd`
- `qa/` — `bdd-test-generation`, `test-generation`, `coverage-gap-analysis`, `mutation-testing`

The full SDLC catalog (DevSecOps, DevOps, Platform, SRE, Compliance) and the phased
build plan live in [`docs/ARCHITECTURE.md`](./docs/ARCHITECTURE.md) and
[`docs/ARCHITECTURE-DETAILED.md`](./docs/ARCHITECTURE-DETAILED.md).
