# SHHA IT wiki

[Open the wiki](https://wiki.sandiahomeowners.org). BookStack on Azure is the
source of truth. Reading is public; Microsoft login allows SHHA organization
members and invited guests to edit under their own identities. Ordinary users
receive Editor access; administration remains separate.

The public repository is
[Sandia-Heights-Homeowners-Association/SHHA-wiki](https://github.com/Sandia-Heights-Homeowners-Association/SHHA-wiki),
and its local checkout is `/Users/heidi/Projects/SHHA-wiki`. The local folder moved
on October 13, 2026; the GitHub repository was renamed from `IT-help-guide` on
October 16, preserving history, issues and Actions. There is one maintained wiki
repository. The old GitHub repository URL redirects to this one; no separate old
repository remains to delete. Do not recreate that name.

Legacy GitHub Pages hosting is disabled. Read and edit the live BookStack wiki;
old static source files remain historical reference only. The BookStack book URL
still contains `shha-it-help-guide`; that is a content address, not a dependency
on the retired repository name.

## Start here

- [Handoff for content and visibility review](docs/content-review-handoff.md)
- [Sync operation and recovery](docs/bookstack-sync.md)
- [Azure deployment and migration history](docs/azure-deployment.md)
- `AGENTS.md`: instructions for future work

## What is maintained here

| Location | Purpose |
| --- | --- |
| `bookstack-current/` | Generated public content mirror: paired Markdown/HTML for every public page in the configured book, combined Markdown, hierarchy and manifest metadata. Never hand-edit. |
| `guide/` | Older curated drafts/reference guides. Existing uncommitted edits remain local and unpublished. |
| `pending-bookstack-updates/` | Editorial drafts, including existing unpublished updates. Sync never reads, deletes or stages them. |
| `scripts/sync_public_bookstack.py` | Anonymous GET-only public mirror exporter. |
| `export-bookstack.py` | Legacy authenticated API exporter for private snapshots; default output is ignored `.local-preserved/api-export`. |
| `scripts/bookstack_migrate.py` | Initial content import/verification tool. Do not replay it against the edited production book. |
| `.github/workflows/` | Offline tool checks and scheduled/on-demand public content sync. These do not deploy Azure or publish draft edits to BookStack. |

## Automatic sync

The [Sync public BookStack content workflow](https://github.com/Sandia-Heights-Homeowners-Association/SHHA-wiki/actions/workflows/bookstack-sync.yml)
runs in **GitHub Actions in this repository**, daily at **09:17 UTC**
(**3:17 a.m. MDT / 2:17 a.m. MST**, America/Denver). Its definition is
[.github/workflows/bookstack-sync.yml](.github/workflows/bookstack-sync.yml).
It does not run on a person's computer or inside the Azure BookStack container.

1. Editors save pages in BookStack, using either the browser WYSIWYG editor or
   an authorized API edit. BookStack remains the source of truth.
2. The scheduled workflow reads the live public book anonymously, including
   newly published pages and edits made with the WYSIWYG editor.
3. It validates a complete stable export and updates only `bookstack-current/`
   on GitHub's `main` branch. Individual Markdown files are in
   `bookstack-current/pages-md/`; matching rich HTML is in `pages-html/`.
4. Changed content gets a bot commit. Unchanged content makes no commit. Failed
   exports preserve the previous completed mirror. Nothing is uploaded back to
   BookStack, and local drafts are never published by this job.

For an immediate refresh, open the linked workflow, choose **Run workflow**, and
select **main**, or run:

```sh
gh workflow run bookstack-sync.yml --repo Sandia-Heights-Homeowners-Association/SHHA-wiki --ref main
```

Check the run's result in Actions; a missing bot commit can simply mean the
content was unchanged. GitHub schedules can be delayed. GitHub may disable a
public repository's scheduled workflows after 60 days without repository
activity; check that the workflow remains active and re-enable it in Actions if
needed. A computer does not need to stay on. Pull deliberately to bring GitHub's
mirror into a local checkout; the schedule does not update local files.

Verified after the repository rename on October 16, 2026: the [manual sync run](https://github.com/Sandia-Heights-Homeowners-Association/SHHA-wiki/actions/runs/38964215308)
succeeded, exported 27 public pages, and committed the changed mirror. The daily
schedule remains active.

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
