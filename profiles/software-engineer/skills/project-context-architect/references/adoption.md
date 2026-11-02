# Safe adoption

1. Resolve the authorized repository/workspace. A shell cd alone may not switch the
   Hermes session workspace. Verify the active context instead of guessing.
2. Inspect instruction files and their documented precedence for the supported release.
   Existing .hermes.md/HERMES.md can take precedence over AGENTS.md. The helper emits
   a warning but does not modify those files automatically.
3. Preview the adoption plan. Its AGENTS.md change appends one link only. Existing
   application files, README and unrelated context packages are not touched.
4. Approve the exact plan digest. Changed preimages require a new review. Do not
   run with root permissions as a substitute for missing project authorization.
5. After application, inspect the diff and start a new session to test discovery.
6. Project-local skills under .hermes/skills or .agents/skills require project trust.
   Invoke native trust configuration only after explicit approval; presence is not trust.
7. Keep a successful declared context separate from application test results. A
   generated context does not prove a service runs, a test passes or a secret exists.

Recovery: the helper keeps .architect-backups with journals. A multi-file apply is
not power-failure atomic. Restore only after comparing current content and protecting
concurrent edits. Never delete an unexplained stale lock.
