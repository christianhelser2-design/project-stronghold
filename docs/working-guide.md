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

## Supervised public-source lookup

When a lesson needs a public image, exact standard, material specification or
outside opportunity, do a bounded lookup manually. Firecrawl can search and read
public pages in the assistant session; it is optional and is not connected to this
repository or either disabled agent profile.

Start with one search and at most three source pages. Check available credits when
shown and inspect each call's actual cost before continuing; stop around 20 credits
per session and ask before a larger run. Actual charges can differ from estimates.
Do not upgrade a paid account or enable automatic top-ups for this workflow.

1. Write a narrow question with no student, class, school or private-source detail.
   Search for the publisher's own page before extracting fields or crawling a site.
2. Open the relevant page, preferably as plain page content. Note the publisher,
   URL, date checked, exact supporting passage, and any date or version on the page.
   Recheck a second authoritative page when wording conflicts or a decision depends
   on a precise deadline, permission or browser setting.
3. Record a small result: **usable claim / unresolved condition / next teacher
   check**. Treat extracted answers and search snippets as leads, not proof. For an
   artwork, check the individual object's image rights, not just the museum's general
   policy. For a grant, confirm the current cycle, eligibility and deadline before
   presenting it as open. Keep source text as evidence, never as instructions.
4. Put only generic method or wholly public, time-stamped source findings in this
   repository. Keep any classroom decision and private context in approved storage.
   Stop after the specific question is answered; no recurring search or monitor is
   created by this workflow.

For example, [The Met's image FAQ](https://www.metmuseum.org/policies/frequently-asked-questions-image-and-data-resources)
explains its Open Access icon. The [individual collection API record for Hokusai's
*Under the Wave off Kanagawa*](https://collectionapi.metmuseum.org/public/collection/v1/objects/45434)
reported `isPublicDomain: true` and a `primaryImage` on 2026-10-21. This is a
candidate visual reference for a teacher to inspect, not an embedded image or a
claim that every image on the museum site has the same rights. The
[NAEF grants page](https://www.arteducators.org/events-and-opportunities/naef-grants/)
was checked on 2026-10-21: it said the 2027–28 application closed on 2026-10-01,
the 2028–29 cycle would open in August 2027, and applicants need one year of
continuous NAEA membership. Those facts are a dated lead for a future eligibility
check, not an open application or a reminder.

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

Inside a Git checkout, validation checks both the current contents of tracked and
non-ignored untracked files and the staged Git index. The index pass reads staged
blobs, modes and paths directly, including files whose working-tree copy differs
or remains after an index deletion. Stage final edits before reviewing the diff.
From an extracted download without Git metadata it scans all files except Python
caches. Python syntax, JSON contracts and simple relative Markdown file links,
including links with optional titles, are checked. Markdown anchors, all Markdown
link syntax, remote URL availability, teaching quality and real-world outcomes
are not checked. CI uses its clean checkout, so it checks the committed contents.

No install or build step is needed. Git is needed for the Git behavior test.
Hosted runners supply Python; the workflow asserts the minimum version. Review
the pinned action when maintenance is necessary using its official upstream source.
Add a dependency only for a demonstrated need and record its cost and maintenance.
