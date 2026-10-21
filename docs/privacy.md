# Public methods, private operations

| Public repository | Approved private storage outside this checkout |
| --- | --- |
| Generic prompts, code, documentation | Actual lesson pacing and operational notes |
| Disabled configuration templates | Rosters, grades, attendance and seating records |
| Completely invented examples | Family contacts, incidents and student support records |
| Public development test results | Internal workbooks, documents, screenshots and exports |
| Rights-cleared original generic material | Student art/images or licensed curriculum lacking publication rights |

Credentials belong in the chosen platform's secret store, never in Git. This
starter needs none. A private repository is not automatically district-approved
student-data storage. Keep sensitive material in its authoritative approved system;
do not copy it here to make development easier.

## Before a push or pull request

1. Create examples from scratch. Removing names from real records is insufficient:
   class, date, behavior or other context may still identify someone.
2. Review all staged files and filenames with `git diff --cached` and
   `git diff --cached --name-only`. Inspect images and attachments separately if
   a future reviewed change allows them; this starter rejects them.
3. Run validation and tests locally. Check issue/PR text, commit messages and logs
   too. Do not paste internal source URLs, private IDs or real incidents there.
4. Publish only the generic method and necessary synthetic evidence.

`.gitignore` reduces accidental staging; it does not protect tracked files,
history, forced adds, screenshots or comments. The validator checks current Git
candidates and staged blobs, including forced tracked files. It is a small
heuristic, not a full secret scanner, identity detector, history audit or
legal/compliance certification.
It cannot detect every token format or identifying fact in prose. Its errors avoid
printing matched values, but even filenames can disclose information.

## If something private is published

Stop sharing it. Notify the authorized owner through an approved private channel.
Revoke or rotate any exposed credential with the account owner, then follow the
applicable incident process. Removing the current file does not remove old commits,
forks, clones, caches or logs. History remediation and repository visibility changes
are separate actions requiring the appropriate authorization. Never paste the
exposed material into a public issue to explain the problem.

## CI boundary

The workflow uses a pinned checkout action, a read-only repository token,
`persist-credentials: false`, no secrets and no deployment step. It runs on
GitHub-hosted runners. Do not add private inputs or `pull_request_target` execution
of untrusted code to this starter.

Reference checked 2026-10-18:
[GitHub secure use guidance](https://docs.github.com/en/actions/reference/security/secure-use).
