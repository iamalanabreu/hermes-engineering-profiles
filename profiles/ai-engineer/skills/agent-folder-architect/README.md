# Agent Folder Architect

Portable operational-folder authoring capability. Read [SKILL.md](SKILL.md).

The original blueprint contract and renderer are retained. The native entrypoint
adds two layouts, preview-first creation, digest-approved evolution and explicit
validation. Python 3.10+; no credentials, network, cloud SDK or provider required.

Run original regression tests from this folder:
`python3 -m unittest discover -s tests -v`

The repository-level suite also exercises the Hermes adapter and evolution path.
The standalone package contains tests but a selective GitHub skill installer may
omit them. Keep the source repository for development and qualification.
