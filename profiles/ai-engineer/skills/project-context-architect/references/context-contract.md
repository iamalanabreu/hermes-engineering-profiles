# Project context input

Schema version: 1. Required fields: slug (kebab-case), title, purpose, kind,
trust_domain, data_classification, scope, non_goals, constraints and acceptance.
The last four fields are nonempty arrays of concrete statements.

Kinds: web, saas, local, cli, service, library, platform, ai, knowledge.
Optional stack is a mapping of confirmed decisions; no entry means undecided.
Optional sources is an array of label/location/status. Status distinguishes
supplied, inspected, synthetic and not-verified; a URL is not proof of inspection.

Do not store keys, internal identities from other organizations, transcripts or
personal data here. Credentials are out-of-band. A context id names scope; it is
not a tenant authorization check or permission to read files.

The output deliberately has no src/, database/, migrations/ or empty ADR directory.
Choose those only after inspecting or designing the actual application. A codebase
map records evidence (entrypoints, dependency edges and known commands); it must
not infer microservices from a folder called services.

For another trust domain, instantiate a new specialist from the same distribution.
Do not clone a live profile's auth, memory or messaging tokens to get a new template.
