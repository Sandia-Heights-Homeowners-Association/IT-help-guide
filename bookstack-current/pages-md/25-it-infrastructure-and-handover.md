# IT Infrastructure and Handover

**Who this is for:** the incoming IT professional and staff arranging continuity. Start by obtaining approved individual access through the office, then read the maintained repository guides. This public page explains the systems and responsibilities; credentials, recovery codes, private records and detailed security configuration belong in approved private documentation.

*Deployment and address checks: October 13, 2026. Read the current repository status and actual cloud settings before acting; names and migration status can change.*

## Start with ownership and access

1. Ask office staff to arrange approved access to the SHHA GitHub organization, Azure subscription, Microsoft 365/Entra administration and the relevant DNS/service-provider accounts. Use your own named accounts.
2. The repositories are in the [Sandia Heights Homeowners Association GitHub organization](https://github.com/Sandia-Heights-Homeowners-Association). The office-accessible `sandiahomeowners@gmail.com` account is an organization owner; coordinate access and account recovery through the office.
3. Confirm a primary and backup administrator, billing/renewal owners and recovery contacts for each service. GitHub access does not grant Azure, Microsoft or DNS access.
4. Keep passwords, API tokens, database connection strings, MFA recovery codes and resident/editorial records out of this wiki and public Git history.

## Systems and sources of truth

<table id="bkmrk-systemresponsibility"><thead><tr><th>System</th><th>Responsibility and infrastructure</th><th>Maintained source</th></tr></thead><tbody><tr><td>Association website and resident database</td><td>The website's MariaDB database owns homeowner, property and resident-link records. Authorized website administrators make corrections there. The toolbox and public dashboard use dedicated SELECT-only access; neither is a replacement membership database.</td><td>Obtain the website maintainer's operating and recovery documentation through the office.</td></tr><tr><td>Microsoft 365</td><td>Owns mailboxes, calendars, committee groups and SharePoint files. Entra supplies Microsoft identity. The toolbox uses Microsoft Graph for calendar/group reads and approved mail delivery; it does not create a second calendar or change group membership.</td><td>Microsoft administration and the private toolbox connection/operations guide.</td></tr><tr><td>SHHA Toolbox</td><td>Node.js 24 LTS application on Azure App Service. Platform Microsoft authentication verifies identity; the app enforces separate tool grants. Operational configuration, successful-send history, queued work and authorized private review state persist outside deployed application files.</td><td>[SHHA-toolbox](https://github.com/Sandia-Heights-Homeowners-Association/SHHA-toolbox), private, deployment branch `main`.</td></tr><tr><td>Public statistics dashboard</td><td>Separate Node.js 24 LTS Azure App Service application at [dashboard.sandiahomeowners.org](https://dashboard.sandiahomeowners.org/). It reads aggregates through SELECT-only queries and generates reports in memory. It has no private staff tools, Graph mail or reminder worker.</td><td>[SHHA-dashboard](https://github.com/Sandia-Heights-Homeowners-Association/SHHA-dashboard), private, deployment branch `main`.</td></tr><tr><td>IT wiki</td><td>Upstream BookStack in an Azure App Service container, with Azure Database for MySQL and persistent Azure Files for configuration/uploads. Public reading and native BookStack Microsoft OIDC editing are separate. Preserve APP\_KEY, the database and uploaded files during upgrades or recovery.</td><td>[SHHA-wiki](https://github.com/Sandia-Heights-Homeowners-Association/SHHA-wiki), public. Local project folder: `SHHA-wiki`. Branch `main` checks tools and mirrors public content; it does not deploy the BookStack container.</td></tr><tr><td>GRIT submissions</td><td>The public site is [sandiaheightsgrit.app](https://sandiaheightsgrit.app/). Its domain still served the Vercel-hosted version at this check. The Azure migration version uses Next.js/React on Node.js 22 LTS, Neon PostgreSQL, private Azure Blob photo storage, Cloudflare Turnstile and Resend. Public-domain cutover to Azure remains separate from deploying that version.</td><td>[grit-newsletter](https://github.com/Sandia-Heights-Homeowners-Association/grit-newsletter), private. Use `azure` for the Azure deployment; `main` retains earlier source. Read its deployment guide before choosing a branch.</td></tr><tr><td>Neighborhood map</td><td>Master mapping work is done in QGIS and exported with qgis2web/OpenLayers. GitHub Pages serves the public web export. Its layers and attribute tables are public; the site does not query the homeowner database. Street tiles use OpenStreetMap; aerial imagery uses USGS. Browser filters do not make any published data private.</td><td>[SHHA-map](https://github.com/Sandia-Heights-Homeowners-Association/SHHA-map), public, publication branch `main`. Back up the master QGIS project and source GIS data separately.</td></tr></tbody></table>

The toolbox, dashboard and Azure newsletter version currently share existing Azure compute, with separate applications, settings and deployments. The wiki uses its own plan, database and file storage. Confirm subscriptions, resources, network configuration and current costs in the protected repository/cloud inventory; a public URL or repository name is not a complete deployment specification.

## Current addresses and DNS

- [wiki.sandiahomeowners.org](https://wiki.sandiahomeowners.org/): Azure BookStack; anyone can read, approved Microsoft users can edit.
- [dashboard.sandiahomeowners.org](https://dashboard.sandiahomeowners.org/): public aggregate dashboard on Azure.
- [toolbox.sandiahomeowners.org](https://toolbox.sandiahomeowners.org/.auth/login/aad?post_login_redirect_uri=%2F): protected staff toolbox with Microsoft login and per-tool grants.
- [sandiaheightsgrit.app](https://sandiaheightsgrit.app/): public contribution site; confirm the migration status before changing its host.
- [Neighborhood map on GitHub Pages](https://sandia-heights-homeowners-association.github.io/SHHA-map/): current map address; a map subdomain is deferred.

The standalone reminders web address is retired; its function is in **Toolbox → Email Reminders**. Older toolbox statistics/Board Report links redirect to the separate public dashboard.

InMotion provides the authoritative DNS zone for `sandiahomeowners.org` at this check; the GRIT domain uses Vercel nameservers. Registrar, DNS provider and application host are different responsibilities. Moving hosting does not require moving nameservers. Preserve mail and unrelated verification records when changing a web destination. Verify the final HTTPS binding/certificate and Microsoft callback, not just the DNS record.

## Microsoft login and permission boundaries

The toolbox uses Azure App Service Authentication and its independent group/user grants. A Microsoft sign-in or committee membership does not automatically grant resident-data access. Invited guests can use their own personal email identity in the SHHA tenant without an SHHA email suffix.

BookStack uses its own native OIDC registration and page/role permissions. Do not apply toolbox authentication rules to the wiki: public reading must remain available while edits stay attributed to signed-in people. The GRIT editor uses its own protected editorial access rather than toolbox Microsoft grants.

Retain the existing shared Entra application used by the toolbox and Microsoft Graph when retiring legacy reminder code; an older application name is not evidence it can be deleted. Keep the master calendar/sender `admin@sandiahomeowners.org`. SHHA display and reminder timezone is `America/Denver`.

## Development, deployment and documentation

1. Read the project's README, AGENTS.md, deployment and operations guides. Verify the actual deployment branch. Inspect Git status and recent commits; other IT work may share a checkout. Preserve unfinished drafts and do not publish them accidentally.
2. For Node applications, use the project's declared Node LTS version and committed lockfile. Test with synthetic data. Toolbox/dashboard changes go through their checks and exact Azure deployment; newsletter changes use the Azure branch workflow. A healthy endpoint alone does not verify database, photo, CAPTCHA or email integrations.
3. For the map, edit the master QGIS source, export outside the repository, use the approved importer, review public fields, then verify GitHub Pages deployment. The website export is not the master GIS backup.
4. For wiki content, edit the live WYSIWYG page or deliberately send current HTML through BookStack's API. Pull before changing a page, preserve newer human edits and verify live readback. Do not round-trip converted Markdown over rich tables.
5. The wiki's nightly/on-demand GitHub job exports anonymous public pages as Markdown, rendered HTML and metadata. It makes no BookStack writes and needs no administrator token. Restricted content is omitted from new exports, but previously public content remains in Git history. Maintain private content backups separately.
6. BookStack software upgrades are separate from content sync. Review the pinned upstream container release, take compatible database/file/configuration backups and plan rollback before applying schema-changing upgrades. Azure deployment CI/CD for the wiki remains work to finish.

## Operations and recovery

Azure's current toolbox settings enable email sending, reminder scheduling, group monitoring and group notifications. An authorized administrator should verify Operational status and recent delivery history before relying on a rule or changing automation. This settings check is not a test email or proof that every delivery path works.

The retired reminders address does not establish whether every old hosting workload or scheduler has been shut down. Confirm final state import, successful-send history, the prior scheduler's shutdown and rollback arrangements in the private migration runbook before calling that operational cutover complete. Do not restore an old sending service alongside the current worker.

- Toolbox deployments must preserve persistent state, send deduplication history, reminder rules, group baselines, queued notices and access policy. Read its private backup rules: some authorized review/campaign files need separate handling rather than entering routine operational backups.
- Wiki recovery needs MySQL data, configuration/APP\_KEY and uploaded-file storage. Markdown/HTML or a portable content ZIP is not a complete installation backup. Full recovery testing remains to be completed.
- GRIT recovery must cover both Neon records and photo bytes. The current public site and Azure preview share live data; use a separate development database for routine testing. Read the repository's approved migration/integration procedures.
- Keep an independent recovery copy, document responsible people and test restoration. Confirm master GIS backups, DNS/domain renewals and cloud certificate renewal.

## First tasks for the incoming IT professional

1. Confirm office-assisted access, ownership, backup administrators and service billing/renewal contacts.
2. Recheck live URLs, private repository guides, deployment branches and cloud settings. Resolve discrepancies between older migration notes and current operation.
3. Review page visibility and repository visibility together before adding sensitive material. The wiki and its public mirror are not a place for private infrastructure inventories or security-remediation details.
4. Verify recovery coverage and remaining cutovers, including the GRIT public domain, wiki platform deployment workflow and legacy hosting retirement.
5. Update this overview with verified completion dates; keep passwords, tenant/resource identifiers, permissions inventories and recovery instructions in the approved private runbooks.

See [Public Utilities and SHHA Toolbox](https://wiki.sandiahomeowners.org/books/shha-it-help-guide/page/public-utilities-and-shha-toolbox) for the reader-facing guide and [Systems Inventory](https://wiki.sandiahomeowners.org/books/shha-it-help-guide/page/systems-inventory) for the wider software/service list.
