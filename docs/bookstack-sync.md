# Public BookStack sync

## Source and destination

BookStack is canonical: https://wiki.sandiahomeowners.org.
The configured book is `/books/shha-it-help-guide`. This repository remains
GitHub `Sandia-Heights-Homeowners-Association/IT-help-guide`, public, default
branch `main`. Its local checkout is `/Users/heidi/Projects/SHHA-wiki`.

The nightly **Sync public BookStack content** workflow runs at 09:17 UTC and can
also be started using GitHub Actions → Run workflow. GitHub schedules can be
delayed; public-repository schedules may be disabled after 60 days without
repository activity. Check Actions if a quiet wiki stops refreshing. Successful
unchanged runs do not make placeholder commits.

## How it works

The standard-library exporter makes anonymous GET requests. It uses no token,
Microsoft session, login cookies, Azure credentials or repository secrets.
The GitHub token has repository content-write permission to commit the mirror;
it grants no ability to edit BookStack.

1. Download the public book's portable ZIP and read its hierarchy/content.
2. Read the anonymous book contents to resolve canonical page/chapter URLs.
3. Download native whole-book Markdown. Split its native section boundaries
   only when the book/chapter/page headings match the expected sequence exactly.
   If content introduces ambiguous headings, fall back to native per-page
   Markdown exports, respecting BookStack's Retry-After throttling.
4. Wrap the rendered rich HTML from the portable export as standalone per-page
   HTML, preserving tables and resolving portable references. Public images of
   up to 2 MiB each can be embedded; larger images fail the sync without
   replacing the prior mirror. Attachment links remain live BookStack links;
   attachment binaries and portable ZIPs are not committed.
5. Re-download the ZIP and require the same public snapshot. Portable asset
   filenames are random, so comparisons normalize them to content hashes.
6. Stage all files, then replace only `bookstack-current/`. Failed downloads or
   changing content preserve the last completed snapshot.
7. Commit only the mirror when its content or metadata changed. Unchanged runs
   preserve the prior export timestamp and make no commit. A concurrent human
   Git push makes the bot's fast-forward push fail safely; it never force-pushes.
   Run it again on the latest `main` after resolving the cause.

Ordinary runs use three whole-book export requests plus the public contents
page, avoiding the four-per-minute anonymous export limit. Ambiguous Markdown
headings may make a run slower. The workflow timeout is 15 minutes; a failed run
does not publish partial content. Additional books are not yet enumerated.

## Manual and local refresh

On GitHub, open Actions → Sync public BookStack content → Run workflow on main.
For a local refresh, run:

```sh
python3 scripts/sync_public_bookstack.py
git diff --stat -- bookstack-current
```

The workflow connects through the known Azure default hostname while preserving
the production Host header, TLS SNI and CA/hostname validation. This avoids old
DigitalOcean DNS caches during cutover. Use the same local override if needed:

```sh
python3 scripts/sync_public_bookstack.py --connect-host shha-wiki-fsgyhpgtg6gzc5aw.westus3-01.azurewebsites.net
```

Pull GitHub updates deliberately before local editing. This shared checkout has
unfinished guide/draft changes, so do not reset, clean or broadly stage it.
The sync workflow checks out a clean main and only stages `bookstack-current/`.
It cannot overwrite local drafts on this computer. Browser changes appear in
the remote mirror after a successful run, and in this checkout after pulling.

## Privacy and boundaries

Only content available to anonymous visitors is mirrored. New published pages
in the configured book are included automatically; restricted/unpublished pages
are omitted by BookStack. A later visibility change removes a page from the
current mirror on the next successful export, but its previous public content
remains in Git history. If the entire book becomes inaccessible or empty, sync
fails and preserves the previous snapshot; explicitly review removal of the
public mirror in that case.

Private wiki content requires a separate private backup policy. Do not give
this workflow an administrator/export token to bypass visibility. The legacy
`export-bookstack.py` requires API credentials and defaults to an ignored private
snapshot; it rejects output paths inside the repository outside
`.local-preserved/`. Raw API error response bodies are suppressed.

This workflow does not edit BookStack, publish pending drafts, deploy the Azure
container, change permissions, back up its database or retire DigitalOcean.
The existing GitHub Pages site is legacy static material; pushing the mirror
does not make that site the wiki. Decide its retirement/redirect separately.

## Verification and maintenance

Run syntax checks and offline tests before changing the exporter/workflows:

```sh
python3 -m py_compile export-bookstack.py scripts/*.py
python3 -m unittest discover -s tests -v
```

Verify the exact GitHub run after publishing workflow changes. Check that its
page count matches public BookStack, the mirror is current, and no drafts were
staged. A GitHub Actions failure is visible in Actions; investigate rather than
declaring the export current. Actions are pinned to reviewed upstream commits.
Native export markup/version changes can require updating the contents parser.
