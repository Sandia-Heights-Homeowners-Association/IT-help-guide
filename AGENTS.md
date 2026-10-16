# Repository Guidelines

## Project Structure

This repository backs up and curates the SHHA IT Help Guide from BookStack.
`export-bookstack.py` is the read-only Python exporter. Its output is in
`bookstack-current/`, including paired Markdown and HTML page exports. Do not
hand-edit it; update BookStack and export again. The reviewed guide is in
`guide/`; offline drafts go in `pending-bookstack-updates/`.

## Reader Journey and Tone

Keep the wiki self-contained: a reader should be able to start on a page,
follow its links, finish a task, and know what to do next. Build clear paths
for office staff, future IT administrators (who may be helping office staff),
internal volunteers with SHHA accounts, and external volunteers using personal
email. Start broad pages with "who this is for" and a first action; link to the
next relevant guide or a named help contact. Never send readers to a page that
assumes knowledge they have not been given, or to a dead end—this is a help
guide, not an escape room.

Assume some readers have very little computer experience. Explain unfamiliar
terms before using them, use numbered steps for tasks, and say what they should
expect to see or happen. Keep the voice friendly and reassuring. A small,
appropriate joke is welcome when it eases anxiety; no one has ever enjoyed a
password reset, but the instructions can still be kind.

## Refresh, Validation, and Development

This repository lives at `/Users/heidi/Projects/SHHA-wiki`; its remote is
GitHub `Sandia-Heights-Homeowners-Association/SHHA-wiki`, default branch main.
The GitHub repository was renamed from IT-help-guide on October 16, 2026;
GitHub Pages hosting is disabled. Do not recreate the retired repository or
re-enable the static site. BookStack's existing book slug remains unchanged.
Read README.md and docs/content-review-handoff.md first. Preserve uncommitted
guide/ edits, the TODO.txt deletion and unpublished pending-bookstack-updates/
drafts. They were carried intact through the move and are not approved live
content. Never publish them just because an automatic sync is requested.

Use Python 3 to refresh the public backup after a BookStack change:

```sh
python3 scripts/sync_public_bookstack.py
```

The anonymous exporter stages a complete snapshot before replacing
`bookstack-current/`; review it with `git status` and `git diff --stat`.
Before committing Python changes, run
`python3 -m py_compile export-bookstack.py scripts/*.py` and
`python3 -m unittest discover -s tests -v`. After publishing formatted content,
check its HTML export for raw Markdown or broken tables and links.

## Writing and Naming Conventions

Write concise, plain-language Markdown with sentence-case headings and
descriptive relative links (for example, `[Volunteer Access](01-volunteer-access.md)`).
Keep guide filenames zero-padded and kebab-cased: `02-email-files-directory.md`.
For Python, use four-space indentation, type hints where useful, standard-library
modules only, and `snake_case` names.

## Change and Review Workflow

Treat BookStack as the source of truth. For substantive edits, export first,
create `codex/<short-description>`, update BookStack through its editor or a
verified HTML API payload, then export again. If access is unavailable, draft
in `pending-bookstack-updates/`.

Use short, imperative commits, such as `Add Microsoft Forms guidance`.
Pull requests should name affected readers and pages, link related requests,
and include screenshots for visual changes. Never commit tokens or secrets.

## Hosting, visibility and automation

Azure BookStack is live at https://wiki.sandiahomeowners.org. Public reading is
intentional; Microsoft login supplies Editor rights for organization members and
invited guests. Do not change public visibility, user grants, OIDC settings,
APP_KEY or deployment resources as a side effect of editing documentation.
Review visibility with the user before restricting or adding sensitive content.
This repository is public. Previously public material persists in Git history;
restricting a wiki page does not erase its old Git versions. No resident records,
private reports, credentials or recovery information belong here.

The nightly/on-demand GitHub workflow reads anonymous native BookStack exports
and stages only bookstack-current/. It never publishes to BookStack or touches
guide/, pending-bookstack-updates/ or Azure settings. Keep it credential-free.
The legacy authenticated exporter writes private snapshots under ignored
.local-preserved/api-export by default; never direct privileged API exports to
the public mirror. API content edits require the current live HTML, a deliberate
change and readback verification; converted Markdown is not safe for replacing
rich WYSIWYG pages. The initial migration tool is not an update/sync tool.

Do not SSH into or operate DigitalOcean. Hosting retirement and the separate
DigitalOcean reminders sender remain pending. Complete DB/files/configuration
recovery and Azure platform deployment CI/CD are separate work, not provided by
the public content sync workflow. Verify the actual GitHub workflow run after
changing automation; do not claim it works from local tests alone.
