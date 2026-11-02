# Repository maintenance contract

This repository AUTHORS three portable Hermes distributions. It is not a live Hermes
home and does not contain the user's company environments. Read README.md, catalog.json
and docs/ARCHITECTURE.md before changing packaging or native behavior.

- Preserve the three profile boundaries and the two canonical shared skills.
- Edit shared-skills/*, never their generated copies under profiles/*/skills/.
- Run `python3 scripts/build_distributions.py --write` only after reviewing source changes;
  default invocation is check-only. Generated local drift is a conflict, not permission to erase it.
- Use only supported native manifest/config fields. Put custom data in clearly documented
  schemas/inputs, not invented Hermes settings.
- Keep secrets, live config, client facts, runtime state, logs and credentials out of source.
- Add tests for file safety, loading contracts and any new helper behavior. Do not count
  a dataset or a mocked test as a live agent evaluation.
- Run the commands in docs/TESTING.md. Report executed, verified, not tested and blocked.
- Preserve all unrelated edits. Do not commit, push, publish, install plugins or contact
  external systems without explicit authorization.
- Source procedures are original synthesis. Keep the supplied Folder Architect provenance
  and any applicable notices; do not import community licenses or code silently.
- Do not weaken checks, alter evidence, or label unexecuted native/live tests PASS.
