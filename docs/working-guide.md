# Use and maintain the starter

## One useful manual trial

Open one prompt and its matching synthetic JSON file. In an approved assistant,
paste the prompt followed by the JSON inside a clearly marked SOURCE DATA block.
Treat the invented values as demonstration inputs only. No script in this starter
invokes an assistant or consumes private school data.

For lesson readiness, look for concrete actions, a matching checkpoint, student
choice, material limits, cleanup and a place to resume. Check that unsupported
standards and current pacing remain unverified. For room reset, require at most
three small steps using existing supplies and a realistic stop point.

The profiles in `agents/` point to those same prompts and examples. `enabled: false`,
empty `tools`, `manual` invocation and `draft-only` mode document intended limits.
The validator enforces those values in this repository. A future runtime must
implement its own controls; JSON labels are not a security sandbox.

## Make one change

```bash
git switch -c improve/one-small-change
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
git add README.md prompts agents config examples docs scripts tests .github .gitignore AGENTS.md
git diff --cached --stat
git diff --cached
git commit -m "docs: clarify one reusable classroom step"
git push -u origin improve/one-small-change
```

Run the checks after edits and before the commit; inspect all staged content.
Use an appropriate commit message for the actual change. Open a pull request and
review its checks and complete diff. The pull-request template records that review.
Branch rules must be configured separately to make checks mandatory; a workflow
file alone does not prevent someone from merging a failing change.

For a harmless code regression already merged, make a new branch, use
`git revert <bad-commit>`, run checks and review the repair. Do not use this as
private-data remediation; see [privacy](privacy.md).

## Validation and limitations

Inside a Git checkout, validation reads tracked files plus non-ignored untracked
files, then inspects their current working-tree contents. Stage final edits before
reviewing the diff; it does not compare staged bytes to working-tree bytes. From an
extracted download without Git metadata it scans all files except Python caches.
Python syntax, JSON contracts and simple relative Markdown file links are checked.
Markdown anchors, remote URL availability, teaching quality and real-world outcomes
are not checked. CI uses its clean checkout, so it checks the committed contents.

No install or build step is needed. Git is needed for the Git behavior test.
Hosted runners supply Python; the workflow asserts the minimum version. Review
the pinned action when maintenance is necessary using its official upstream source.
Add a dependency only for a demonstrated need and record its cost and maintenance.
