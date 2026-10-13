# SHHA IT guide

Public IT documentation for the **Sandia Heights Homeowners Association**, intended
to help staff, volunteers and incoming IT maintainers understand how SHHA systems
fit together and continue their work.

**Current wiki:** [wiki.sandiahomeowners.org](https://wiki.sandiahomeowners.org/).

## What this repository contains

This public repository contains the earlier standalone Markdown/HTML guides.
Its `index.html` and related files are also published through GitHub Pages at
[the legacy guide address](https://sandia-heights-homeowners-association.github.io/IT-help-guide/).
These files are useful reference material; the current BookStack wiki is the
authoritative published guide. This GitHub checkout is not a complete export of
current wiki content.

BookStack provides browser editing, books/chapters/pages and attachments. It is
upstream software, rather than a custom SHHA application. Wiki content and
hosting configuration have separate publication/recovery workflows.

## Hosting and Azure boundary

The live wiki remains on its existing host while a separate Azure BookStack
migration is being prepared. Azure hosting uses a Linux App Service container,
a MySQL database and persistent file storage. Those resources and a preview app
exist, but creation alone does not establish completed content migration,
authentication, DNS cutover or restore verification.

This repository currently contains **no Azure application deployment workflow**.
Pushing these static guide files publishes the Pages version; it does not update
BookStack's database/content or deploy the Azure wiki. The maintained Azure
deployment source/runbook still needs to be established in the GitHub organization
as part of that separate migration. Confirm its location and current status with
the IT maintainers before operating the hosting platform.

## Documentation and access

Describe stable responsibilities and sources of truth: Microsoft 365 owns mail,
calendars and groups; the association website owns resident records; the public
membership dashboard exposes aggregates; restricted reconciliation tools compare
records for staff review. Link authorized maintainers to private repository
READMEs/runbooks for deployment branches, Azure resources and detailed operations.

Repositories are managed in the
[Sandia Heights Homeowners Association GitHub organization](https://github.com/Sandia-Heights-Homeowners-Association).
Application source repositories are private; this guide and the public map are
public. The office-accessible **sandiahomeowners@gmail.com** account is an owner.
Arrange approved individual access through the office.

Treat wiki pages and this repository as public even when unshared/unlisted.
Do not include credentials, recovery codes, private permissions, resident records,
editorial submissions, private reports or sensitive operational state. Obtain
access/recovery information through approved private channels.

For a documentation update, first identify whether the change belongs in current
BookStack content or these legacy static files. Review links and public suitability,
publish through the appropriate workflow and verify the actual destination.
Git history preserves static source; it does not back up the wiki database,
attachments or infrastructure. The wiki's recovery procedure must cover all three.
