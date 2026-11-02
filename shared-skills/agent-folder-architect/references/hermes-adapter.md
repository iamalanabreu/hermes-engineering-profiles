# Hermes adapter and operational contract

## What changed
The supplied Agent Folder Architect already had valid name/description frontmatter
in its filesystem source. Resource views may omit that metadata. It has not been
replaced with an invented upstream skill. The original renderer and its unit tests
are retained; the compact entrypoint adds native routing and a safe evolution CLI.

`architect.py` is the preferred command. `scaffold.py` remains the original
operational-layout generator for compatibility. It does not add the newer layout
mapping or reviewed-update behavior. Both render from the same blueprint schema.

## Layout mapping
- operational: original Portuguese paths and required playbook files.
- hermes: arquivos -> references/files; validacao -> references/validation;
  referencias -> references/domain; exemplos -> examples; testes -> scripts/tests;
  notas.md -> references/notes.md; PENDENCIAS.md -> references/pending.md.
Local Markdown links are rewritten relative to their new file. The entrypoint lists
each support file so a selective skill installer can include it. Do not assume
installers copy unreferenced repository files or follow Python imports automatically.

## Evolution and recovery
The plan stores only explicit proposed text-file changes and each previous hash.
The operator reviews the diff and approves the SHA-256 of the exact JSON bytes.
A digest is not a login or authorization token. The caller must be permitted to
write the root and keep it unavailable to untrusted concurrent writers.

Apply validates all preimages, takes a lock and backs up replaced files in
`.architect-backups/<run>/files/`. Normal failures restore touched files. A sudden
process exit or power loss may leave an incomplete multi-file change: inspect
journal.json and compare current hashes before restoring manually. Do not delete
an unrelated concurrent edit. No unlisted file is removed; backups are not auto-pruned.

## Native availability versus capability
The distribution requests `skills.auto_load: [agent-folder-architect]`. Missing,
disabled or shadowed skills and session-start options can prevent effective loading.
Check the runtime index and a new session before claiming native operation. This
package does not patch Hermes to make the model obey, bypass scans, or enforce IAM.

## Test scope
Unit tests prove local file behavior with synthetic fixtures. Native installation
and model routing need the optional runtime smoke test and live evaluation suite.
Neither passing the renderer nor the existence of SKILL.md proves those layers.
