# SHHA IT Help Guide

This repo is now a local working copy of the current BookStack wiki at
`https://wiki.sandiahomeowners.org`.

The old standalone wiki files are stale. Treat BookStack as the source of truth,
then use this repo to export, review, simplify, and back up the content.

## What To Keep

Bare code and working artifacts worth keeping:

- `export-bookstack.py` - read-only BookStack exporter.
- `bookstack-current/` - current raw export from BookStack.
- `guide/` - reviewed, simplified Markdown guide built from the current export.
- `TODO.txt` - running list of screenshot/image ideas and editorial follow-ups.
- `README.md` - repo notes and refresh instructions.

What should not be kept as canonical content:

- Old top-level `.md` and `.html` standalone wiki pages.
- `shared.css`, because the standalone HTML site is no longer current.
- One-off `upload-to-bookstack.py` / `update-bookstack*.py` scripts with
  embedded HTML and hard-coded BookStack IDs.

## Normal Agent Workflow

Heidi will usually ask a question that needs to be answered in the wiki. The
agent should do the research, draft the answer, update BookStack, then refresh
the local backup.

Use this flow:

1. Export BookStack before editing, if the local export may be stale.
2. Commit the current export before a major change.
3. Create a branch named `codex/<short-description>`.
4. Draft changes locally first when the edit affects flow, tone, or structure.
5. Update BookStack deliberately through the API or WYSIWYG editor.
6. Re-export BookStack after the remote update.
7. Update `guide/` when the scannable agent/human guide should change.
8. Update `TODO.txt` with image ideas, screenshot locations, or unresolved
   questions.
9. Commit the branch.

Do not treat `bookstack-current/` as hand-edited source. It is an export target.
If a local correction needs to become real, apply it to BookStack, then export
again.

## Images And Attachments

BookStack pages may include images added manually through the WYSIWYG editor.
The current exporter preserves the page HTML and image references, but it does
not download image binaries.

Decision:

- Keep images in BookStack.
- Do not commit large image files to git.
- Use `TODO.txt` to mark where a screenshot or image would help.
- Do not maintain a separate image-binary backup unless that decision changes.

This keeps the git repo useful as a text/content backup without turning it into
a heavy media archive. In a BookStack disaster, this repo restores the text,
structure, links, and image references, but not large uploaded image binaries.

## GitHub Backup Workflow

Use this when the goal is to pull the latest BookStack content into local
Markdown/HTML and push the backup to GitHub.

1. Start from the branch you want to update.

   ```sh
   git switch main
   git pull --ff-only origin main
   ```

2. Pull the live BookStack wiki into local files.

   ```sh
   python3 export-bookstack.py
   ```

3. If the scannable local guide should change, update files under `guide/`.
   Do not hand-edit `bookstack-current/`; it is rewritten by the exporter.

4. Review what changed.

   ```sh
   git status
   git diff --stat
   ```

5. Commit the local backup.

   ```sh
   git add .
   git commit -m "Export BookStack updates"
   ```

6. Push to GitHub.

   ```sh
   git push origin HEAD
   ```

For larger revisions, create a branch first:

```sh
git switch -c codex/<short-description>
```

Then export, edit BookStack, export again, commit, and push that branch.

## Refresh From BookStack

The exporter requires these environment variables:

```sh
BOOKSTACK_TOKEN_ID=...
BOOKSTACK_TOKEN_SECRET=...
```

Optional:

```sh
BOOKSTACK_URL=https://wiki.sandiahomeowners.org
BOOKSTACK_BOOK_ID=1
```

Run:

```sh
python3 export-bookstack.py
```

The command rewrites `bookstack-current/` with:

- `manifest.json` - page IDs, names, URLs, update dates, and local paths.
- `book.md` - combined Markdown export.
- `pages-md/` - one Markdown file per BookStack page.
- `pages-html/` - one HTML file per BookStack page.

## Reviewed Guide Structure

The simplified guide intentionally reduces repeated material:

- [Start Here](guide/00-start-here.md)
- [Volunteer Access](guide/01-volunteer-access.md)
- [Email, Files, and Directory](guide/02-email-files-directory.md)
- [Staff and Admin SOPs](guide/03-staff-admin-sops.md)
- [Operations Open Items](guide/04-operations-open-items.md)
- [New Board Member Guide](guide/05-new-board-member.md)

Recommended BookStack flow:

1. Start Here
2. Email, Files, and Directory
3. Volunteer Access
4. New Board Member Guide
5. Staff and Admin SOPs
6. Operations Open Items
7. GRIT Contributor Guide
8. GRIT Internal Production Reference
9. GRIT Layout Monthly Guide
10. FAQ as an appendix, not the primary navigation path
