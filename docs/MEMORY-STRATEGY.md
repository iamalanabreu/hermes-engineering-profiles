# Memory strategy

How a profile in these distributions should split durable knowledge between the
local capped memory files and the Hindsight bank. Written after the 2026-11-02
migration of `ai-devsecops-engineer`, where nine operational entries were moved
out of the local store because they could not fit.

## Two stores, two budgets

| Layer | Surface | Budget | Holds |
|---|---|---|---|
| Local | `MEMORY.md` / `USER.md` in the profile directory | hard cap (`memory_char_limit`, commonly 2.200 / 1.375 chars) | Identity, behavioral preferences, scope gates, standing conventions — facts that must be present in **every** prompt |
| Hindsight | `hindsight_retain` / `hindsight_recall` against a bank | none of the local cap | Infrastructure topology, tool configuration, API quirks, procedures — anything that changes when the environment changes |

The distinction is not importance. It is **frequency of relevance**: a fact belongs
in local memory only if it should shape every single turn regardless of task.

## Routing rules

1. **A rejected local write is a routing signal, not a compression problem.** When
   the `memory` tool refuses a write because it would exceed the cap, the fact
   belongs in Hindsight. Do not answer by shortening it, and do not evict an
   unrelated entry to make room.
2. **Never compress an operational fact to fit the cap.** Abbreviating a hostname,
   dropping a path, or flattening a version to save 200 characters produces
   confident-but-wrong recall later.
3. **`memory.provider: hindsight` does not mean the `memory` tool writes to
   Hindsight.** The tool always edits the capped local files. Hindsight is reached
   through its own retain and recall surfaces.
4. **Migrate when the cap is hit, not when it is nearly hit.** A near-full local
   store with a working Hindsight bank is a known state; treat it as stable.

## Bank naming

The convention organizes data. It is not an authorization boundary — see the
isolation note below.

| Pattern | Example | Use when |
|---|---|---|
| `agent-<profile>` | `agent-ai-devsecops-engineer` | Private memory for one profile |
| `team-<topic>` | `team-devops` | Knowledge shared across profiles for a domain |
| `project-<name>` | `project-hindsight-deploy` | Memory scoped to one deployment or incident |
| `user-<name>` | `user-iam-alan-abreu` | Memory about a person, across profiles |

Start a new profile at `agent-<profile>`. Promote to `team-<topic>` only when
multiple profiles explicitly need the same facts.

## Resolving the effective bank

Precedence is not obvious and has caused a real incident: an old top-level
`bank_id: hermes` silently superseded a correctly configured `agent-<profile>`
in the environment. Read the effective value, not the intended one:

1. Non-empty top-level `bank_id` in the profile's `hindsight/config.json`
2. Else `banks.hermes.bankId` in the same file
3. Else `HINDSIGHT_BANK_ID` from the environment

Print all three during an audit. A mismatch between them is a defect, not a
harmless duplicate.

## Isolation reality

Validated 2026-09-01 against a self-hosted deployment: the tenant API key is
**server-wide**. Any caller holding it can recall, list, and retain against any
bank on that server, including banks it never created.

Consequences to state plainly before promising isolation:

- The `bank_id` is a namespace for organization, **not** a security boundary.
- Every profile sharing one server key shares one trust domain.
- Real isolation requires a second server or a separate tenant keypair.

## Minimum facts a distribution profile should carry in local memory

Keep this small. Anything beyond it belongs in Hindsight.

- The profile's purpose and its domain boundaries.
- The user's language, timezone, and response-shape preferences.
- Standing gates that must never be skipped (approval boundaries, secret handling).
- Environment facts with no task home: canonical repo owner, vault variable names.

## Migration checklist

1. **Inventory.** Dump the local store and classify each entry as identity,
   preference, or operational.
2. **Back up.** Copy `MEMORY.md` and `USER.md` to a timestamped location.
3. **Retain.** Send each operational entry to the bank with a short context tag.
4. **Verify by recall.** Query the bank for each retained fact. Retain succeeding
   is not recall succeeding; require the fact to come back.
5. **Rewrite local.** Reduce the local files to identity and preferences only.
6. **Re-read.** Confirm the next prompt still carries the identity facts and that
   nothing operational was lost in the rewrite.

A migration that retains successfully but never recalls has verified nothing.

## Second-brain integration

When a COG or Obsidian vault is in use, the vault is a **third** store with a
different job: long-form narrative, decisions, and runbooks meant for human
reading and git history. It is not a substitute for either of the above.

- Vault path comes from `COG_VAULT_PATH`. Do not search the disk for vaults.
- The shared safe vault (`COG_GLOBAL_SAFE_PATH`) is read-only.
- Vault notes may be linked from a bank entry, but the bank entry must not depend
  on the vault being mounted.