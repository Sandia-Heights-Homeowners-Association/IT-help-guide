# SHHA IT wiki

[Open the wiki](https://wiki.sandiahomeowners.org). BookStack on Azure is the
source of truth. Reading is public; Microsoft login allows SHHA organization
members and invited guests to edit under their own identities. Ordinary users
receive Editor access; administration remains separate.

This checkout moved from `IT-help-guide` to `SHHA-wiki` on October 13, 2026,
preserving Git history and existing local drafts. The GitHub repository remains
[Sandia-Heights-Homeowners-Association/IT-help-guide](https://github.com/Sandia-Heights-Homeowners-Association/IT-help-guide).
It is public. The old standalone HTML/Markdown site still exists through GitHub
Pages; the BookStack wiki is the current documentation. That legacy hosting was
not disabled or revised during this move.

## Start here

- [Handoff for content and visibility review](docs/content-review-handoff.md)
- [Sync operation and recovery](docs/bookstack-sync.md)
- [Azure deployment and migration history](docs/azure-deployment.md)
- `AGENTS.md`: instructions for future work

## What is maintained here

| Location | Purpose |
| --- | --- |
| `bookstack-current/` | Generated public content mirror: 24 pages initially, paired Markdown/HTML, combined Markdown, hierarchy and manifest metadata. Never hand-edit. |
| `guide/` | Older curated drafts/reference guides. Existing uncommitted edits remain local and unpublished. |
| `pending-bookstack-updates/` | Editorial drafts, including existing unpublished updates. Sync never reads, deletes or stages them. |
| `scripts/sync_public_bookstack.py` | Anonymous GET-only public mirror exporter. |
| `export-bookstack.py` | Legacy authenticated API exporter for private snapshots; default output is ignored `.local-preserved/api-export`. |
| `scripts/bookstack_migrate.py` | Initial content import/verification tool. Do not replay it against the edited production book. |
| `.github/workflows/` | Offline tool checks and scheduled/on-demand public content sync. These do not deploy Azure or publish draft edits to BookStack. |

## Automatic sync

The **Sync public BookStack content** workflow runs daily at **09:17 UTC**
(2:17 a.m. MDT / 3:17 a.m. MST). It also has a **Run workflow** action on GitHub.
It exports anonymously, verifies a complete stable snapshot, and commits changes
only under `bookstack-current/` to `main`. Unchanged content makes no commit.
GitHub schedules can be delayed; they are not an immediate notification of edits.

No BookStack credentials are needed. Native portable ZIP exports supply rendered
rich HTML and hierarchy; native Markdown exports capture readable conversions of
browser WYSIWYG edits and newly published pages. Only the current SHHA IT Help Guide book
is configured; additional books need explicit configuration/extension. Images
can be embedded in the contained HTML export; binary ZIP/assets are not committed.
This is a readable content mirror, not a database/files/configuration recovery
backup.

To refresh locally:

```sh
git pull --ff-only
python3 scripts/sync_public_bookstack.py
git diff --stat -- bookstack-current
```

If this computer still caches the DigitalOcean address, add:

```sh
python3 scripts/sync_public_bookstack.py --connect-host shha-wiki-fsgyhpgtg6gzc5aw.westus3-01.azurewebsites.net
```

That override retains the production Host header, TLS SNI and normal certificate
verification. Existing local drafts can make a pull conflict; preserve them and
resolve deliberately rather than resetting the checkout. Automatic exports do
not update local files until you pull.

## Editing procedure

1. Refresh the public mirror before substantive changes.
2. Edit BookStack through its WYSIWYG editor or a deliberate HTML API payload.
   Fetch the current page before API editing and check for newer human changes.
3. Verify the actual live page, then run the GitHub sync or refresh locally.
4. Commit only the intended files. Never upload Markdown exports over rich
   WYSIWYG content or use a broad `git add .` while old drafts remain unfinished.

Authenticated exports can include private content; keep them outside this public
mirror. Restricting a page removes it from subsequent successful anonymous
exports, but old Git commits still retain material that was previously public.
Before adding sensitive information, restrict the wiki page and decide how its
private backup will be handled. Git visibility cannot be enforced by BookStack.

## Checks

Python standard library only; no Node build is required for this repository.

```sh
python3 -m py_compile export-bookstack.py scripts/*.py
python3 -m unittest discover -s tests -v
```

Offline tests cover draft preservation, additions/removals, blocked login/foreign
redirects, stable repeated exports and preservation of the last mirror on
download failure or concurrent content changes.

Azure resources, SSO, imported content and production HTTPS are working. Azure
platform deployment CI/CD, complete recovery testing and DigitalOcean retirement
remain separate unfinished work; see the handoff. Do not operate DigitalOcean
or the unrelated live reminders sender as part of content sync.
