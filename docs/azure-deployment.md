# SHHA wiki deployment and API maintenance

> Historical plan and implementation notes through October 13, 2026. The repo
> has now moved into SHHA-wiki and public automatic syncing is implemented.
> On October 16, 2026 the GitHub repository was also renamed to SHHA-wiki and
> legacy GitHub Pages hosting was disabled. Existing BookStack URLs are unchanged.
> README.md, docs/bookstack-sync.md and docs/content-review-handoff.md supersede
> older pending-status statements below. Azure platform deployment CI/CD and
> full recovery/hosting retirement are still pending.

Keep BookStack as the visual editing system and move the current documentation
to a fresh Azure installation. Use this folder as the checkout for one maintained
GitHub repository containing deployment configuration, API tooling, content
drafts and approved exports. BookStack application code remains an upstream
dependency rather than a fork maintained by SHHA.

## Decisions on October 13 2026

- Retain BookStack and its books, chapters and pages; WYSIWYG editing is essential.
- Use the BookStack HTTP API to extract current DigitalOcean content and populate
  Azure. Do not SSH into DigitalOcean or use a server/database copy.
- Old edit history and the complete source database are outside migration scope.
  The user accepts a content-only migration. Images are believed to be minimal;
  inventory actual referenced assets before deciding none need transfer.
- Keep Microsoft sign-in for SHHA tenant members and invited guests, with future
  edits attributed to individual accounts. Keep the existing Codex API workflow.
- Defer chatbot and NotebookLM work.

## One repository with two independent workflows

Use one repository, with separate platform deployment and content publication.
Do not maintain a second copy of BookStack source code. A second repository is
useful only if infrastructure and documentation later need different owners or
access policies.

| Workflow | What changes | Where it takes effect |
| --- | --- | --- |
| Platform deployment | Azure definitions, image version, nonsecret configuration and deployment tools | Running BookStack software and Azure resources |
| Content publication | Selected documentation pages, hierarchy, descriptions and tags | BookStack's database through its API |
| Content export | Fresh snapshots of authorized live pages | Local/repository mirrors and private migration archives |
| Human editing | Staff or volunteer saves in BookStack | Live database immediately; later captured by export |

The local checkout and GitHub repository are now both `SHHA-wiki`. Git history
and local drafts were preserved when moving the folder and renaming the remote.
The daily public-content sync runs in this repository's GitHub Actions; it does
not deploy Azure. The platform deployment workflow described below remains a
plan, not implemented CI/CD. Use README.md for current operation.

Proposed layout, to implement when moving the checkout:

```text
SHHA-wiki/
  README.md
  AGENTS.md
  infra/                      Azure definitions and nonsecret parameters
  deployment/                 Pinned BookStack image and upgrade configuration
  scripts/                    Export, inventory, migration and publishing tools
  docs/                       Operation, migration and recovery instructions
  content/                    Approved page mirrors and reviewed drafts
  .github/workflows/          Checks, platform deploy and selected API operations
  .env.example                Variable names only
  .gitignore                  Exclude credentials and private migration archives
```

Retain or deliberately map the existing `guide/`, `bookstack-current/` and
`pending-bookstack-updates/` directories during the move. Do not silently discard
local drafts, pretend the July snapshot is current, or publish pending drafts
as part of migration. Secret settings, user/permission inventories and binary
migration archives stay in protected storage outside Git. Review which content
is suitable for the repository before adding fresh exports.

## Deploying base BookStack

Use a separate Azure Linux App Service running a maintained BookStack container,
Azure Database for MySQL Flexible Server, and persistent file storage. This
managed deployment fits the no-SSH workflow: GitHub Actions and Azure APIs manage
the platform, while the BookStack API manages documents.

1. Put the Azure resource definitions and a tested image reference in this repo.
   Pin a release and image digest; do not use a moving `latest` tag. Initially
   deploy a published upstream image directly. A private registry or custom image
   is needed only if compatibility testing or SHHA customization requires it.
2. Quote the app plan, MySQL tier, persistent files and backups before creating
   paid resources. Treat this as a separate wiki deployment. Do not assume the
   toolbox's existing plan has capacity or alter its access/email configuration.
   The earlier VM estimate does not price this managed design.
3. Create an empty dedicated database, enable verified database TLS, and configure
   a persistent upload/configuration mount. If using LinuxServer.io's image,
   prove the Azure Files mount at `/config`, startup, file permissions and TLS
   behavior on the target. If needed, maintain a thin container adapter rather
   than forking BookStack. Never put MySQL data files on the application file mount.
   On this dedicated Azure MySQL server, retain
   `sql_generate_invisible_primary_key=OFF` in the infrastructure definitions.
   Azure's ON default blocked BookStack's standard primary-key replacement
   migration; the OFF setting allowed initialization to complete.
4. Initialize the new installation using the image's supported startup process.
   Keep preview access restricted while securing the bootstrap administrator.
   Generate a new Azure APP_KEY because this is a fresh installation, store it
   securely, and preserve it for all future redeployments/recovery.
5. Configure native BookStack OIDC against the SHHA Microsoft tenant, with its own
   registration and exact preview/production callbacks. Test a tenant member,
   invited guest and administrator. Assign ordinary editor rights separately
   from administration. Reading is public, as explicitly clarified by the user
   on October 13, 2026; Microsoft authentication is required for editing.
6. Create a dedicated BookStack API account/token with the required content
   permissions. Test noninteractive token requests through the Azure endpoint.
   Keep BookStack's API reachable using its own token authentication rather than
   requiring every automation request to pass an interactive browser login.
7. Verify that changing/restarting the container preserves database contents,
   uploads and APP_KEY. Configure database recovery and separate file backups
   through managed Azure services/APIs, and perform a restore test.

Base BookStack is installed once initially, but it is not a one-time software
deployment. Maintain security releases and tested upgrades by changing the pinned
image reference. Take database/files backups before upgrades. Database schema
changes may require restoring matching data and image versions for rollback;
switching back to an older image alone is not a complete rollback procedure.

## CI/CD behavior

- **Checks:** validate deployment definitions and API tools on relevant commits.
  Tests use synthetic content and do not publish pages or print private API data.
- **Platform deployment:** commits touching `infra/` or `deployment/` trigger the
  deployment workflow after checks. Use GitHub-to-Azure OIDC with narrowly scoped
  access. Apply the pinned image/configuration and verify that exact deployment
  with startup, health, sign-in and persistence checks. Do not import or overwrite
  wiki content during container startup or ordinary deployment.
- **Content publication:** initially run deliberately for selected reviewed
  pages. Use a separate BookStack token, independent of Azure deployment access.
  Ordinary mirror/draft commits do not redeploy the platform or automatically
  overwrite live pages. Serialize automation and compare live content against
  the drafting baseline before publishing; resolve intervening human edits.
- **Content export:** pull after publication and periodically when requested.
  Export-only changes do not publish back to BookStack. Keep passwords/tokens in
  secure local configuration or GitHub secrets, never the committed files or logs.

## API migration sequence

### Capture current DigitalOcean content

Use the existing source API credentials through secure configuration. Enumerate
all authorized shelves, books, chapters and pages with pagination; record which
scope the token can actually see. Obtain page HTML and original Markdown where
present, hierarchy/order, descriptions, tags and current URLs. Capture summaries,
timestamps and content hashes so the final sync can detect later changes.

If the source supports the Portable ZIP API, export books with their referenced
files and keep those archives privately. ZIP import/export API endpoints were
introduced in BookStack v25.07. If unavailable, use ordinary content endpoints
and supported asset downloads/uploads; do not upgrade or access the source server
to obtain ZIP support. Probe the live API documentation/capabilities before
writing source-version-specific code.

Keep raw HTML as the fidelity reference for WYSIWYG pages, and Markdown as a
secondary readable export. Inventory images, linked attachments and embedded
resources even though few are expected. Record any inaccessible content/assets
instead of treating a partial export as complete. Preserve the current Quick
Links SharePoint targets directly from live content.

### Import and verify Azure

Import one representative book first, then the remainder. Prefer supported ZIP
import where its behavior is verified; otherwise recreate books/chapters/pages
through documented API calls. Recreate shelves/book associations and order
separately where ZIP does not cover them. Record source-to-target object IDs and
URLs; imports allocate new target identities, so do not reuse hard-coded source
IDs for later publishing.

Import WYSIWYG pages as HTML rather than converting old HTML tables through
Markdown. Once every page exists, repair internal wiki links through the verified
mapping and test cross-book links and paragraph anchors. Preserve external
SharePoint destinations. Check whether the installed API can retain old slugs;
where URLs change, plan and test supported redirects or update affected links.
Do not promise unchanged historical URLs before this check.

Compare titles, hierarchy, order, page content, tables, tags, links and any assets.
Historical authorship/revisions, old accounts/passwords, operational settings and
exact old role grants are not part of this migration. Create new SSO users,
editor policy and API credentials on Azure. Record any remaining content
exceptions for review. Test a human WYSIWYG edit and an API edit before cutover.

### Synchronize and switch the hostname

Arrange an editing pause through the source BookStack administration/UI rather
than SSH. If source writes cannot be blocked through supported settings, have
editors stop saving and repeat content inventories until the final snapshot is
stable. Re-export changes/deletions since the rehearsal, apply them to Azure and
verify counts/hashes. Re-running the migration must update mapped objects rather
than create duplicate books or pages.

Keep Azure editing paused until final sync completes. Prepare the production
hostname binding, TLS and OIDC callback, then switch wiki DNS to Azure and confirm
the actual endpoint, sign-in, links and token API access. Reopen editing on Azure
as the sole active wiki. Retain the final private content export, target mapping
and an immediate Azure backup; run a fresh content export from Azure.

Before the user deletes DigitalOcean hosting, verify content and SSO/API checks,
Azure backup recovery and any other workloads on that hosting plan. The reminders
cutover remains separate if it shares the VPS. Do not delete or operate the
DigitalOcean plan from this workflow. Any rollback after Azure edits start must
preserve those new edits; routing back to an older source loses them.

## Day to day API control

Live Azure BookStack is authoritative. Before drafting an update, pull the latest
affected pages. Prepare a reviewed HTML change for formatted pages, publish only
the intended pages through the API, verify their rendering, then refresh the
approved repository mirror. API edits are attributed to the account owning that
token; individual human attribution requires individual credentials. Human edits
in the browser use the signed-in person's SSO-linked account.

The repo therefore maintains BookStack's deployment and our control tools. It
does not replace the live database with a set of files on every push.

## Implementation order

### Azure setup walkthrough status

On October 13, the connected Azure subscription was `Azure subscription 1`.
Its Web App listing contained no BookStack wiki app, and its MySQL Flexible
Server listing was empty. No Azure resources were created during this check.

Resource group `shha-wiki-rg` in West US 3 was created by the user and verified
with provisioning state Succeeded. The user then created MySQL Flexible Server
`shha-wiki-rg`; it was verified Ready, MySQL 8.4, Burstable Standard_B1ms, 20 GiB,
public access enabled and 7-day backup retention. Its hostname is
`shha-wiki-rg.mysql.database.azure.com`. The dedicated BookStack database and
application login are now configured and verified below. Review backup
retention and the production tier before cutover.

Storage account `shhawikistorage` and classic share `bookstack` now exist. The
share was verified SMB. The account is FileStorage, StandardV2_LRS, using
provisioned v2 billing rather than the proposed StorageV2 pay-as-you-go model.
The initial 1,024 GiB allocation was reduced by the user. Verification now shows
32 GiB, 1,007 IOPS and 61 MiB/s, using Azure's recommended performance settings.
Billing follows these provisioned quantities. The documented HDD minimums are
32 GiB, 500 IOPS and 60 MiB/s; further performance reduction is optional after
checking the resulting cost/performance tradeoff.

The user created Linux container Web App `shha-wiki` on dedicated plan
`shha-wiki-plan`. Azure reports Running, Always On enabled, and sidecar-mode
configuration (`sitecontainers`). Its main container `bookstack` uses
`lscr.io/linuxserver/bookstack:version-v26.09.1`, with target port 80.
Its default hostname is
`shha-wiki-fsgyhpgtg6gzc5aw.westus3-01.azurewebsites.net`.
Running alone is the Azure resource state; application initialization was
separately verified after the database compatibility fix below.
The user saved the Azure Files mount named `bookstack`;
verification shows account `shhawikistorage`, share `bookstack`, path `/config`,
and mount configuration state Ok. Azure Files contains the application's
configuration directories, `www/.env`, and upload/attachment directories,
confirming startup wrote to the persistent share. The login page also loads
after restart. A human content edit and upload/restart test remain pending.
A CLI query error exposed the mount's storage key in diagnostic output during
verification. The mount was switched to the alternate key and the exposed key
was rotated and verified invalidated; credential values are not recorded here.
MySQL administrator login is `wikiadmin`. The user created database `bookstack`;
verification confirms `utf8mb4` and `utf8mb4_unicode_ci`. The current firewall
originally allowed the user's client IP only. Seven exact-IP firewall rules
(`bookstack-app-01` through `bookstack-app-07`) were added for the Web App's
current outbound addresses; refresh these if a plan/network change alters them.
The local Azure CLI `rdbms-connect` extension
was installed to support an interactive, TLS-verified database connection with
password prompting. The user reports creating `bookstack_app`, requiring SSL
and granting it privileges only on `bookstack.*`. Its database login was verified
with certificate/hostname validation and TLS 1.3 cipher TLS_AES_256_GCM_SHA384.

Base Web App settings were applied: the exact HTTPS preview URL, database host
above, port 3306, username `bookstack_app`, database `bookstack`, production mode,
debug disabled, secure session cookies, timezone America/Denver and PUID/PGID
1000. Database TLS uses `MYSQL_ATTR_SSL_CA=/etc/ssl/certs/ca-certificates.crt`;
startup successfully connected and ran the standard schema migrations.
The pinned BookStack version hardcodes utf8mb4/utf8mb4_unicode_ci for its MySQL
connection, matching the created database. A new 32-byte APP_KEY was generated
and stored in Azure app settings, with a private local copy outside Git at
`/Users/heidi/.config/shha-wiki/azure-app-key`. Preserve this key on upgrades and
include it in protected recovery storage; the local copy is not an off-site backup.
The user entered DB_PASSWORD directly in Azure's Environment variables panel;
the secret was used internally for verification without printing or saving it.

Startup verification on October 13 initially found a working login page but
only 44 of the release's 103 schema migrations recorded. Full container logging
identified MySQL error 1235 at
`2020_08_04_111754_drop_joint_permissions_id`: Azure's
`sql_generate_invisible_primary_key=ON` disallowed the primary-key replacement.
The parameter was changed to OFF on this dedicated wiki server, and BookStack
was restarted to resume its standard migrations. All 103 migrations then
completed, ending at `2026_07_27_201402_update_users_external_auth_id_collation`.
The HTTPS `/login` endpoint returned 200 with the BookStack login form after
restart. No upstream application fork or manual migration edits were needed.
`sql_require_primary_key` was verified OFF and not changed. Azure-generated
invisible key columns already exist on cache/password_resets/sessions from the
initial run; the complete migration sequence passed with these present.
Private diagnostic archives are outside Git under
`/Users/heidi/.config/shha-wiki/diagnostics`; container filesystem logging is
enabled for startup troubleshooting. Do not publish raw logs or secrets.

The new preview initially used a temporary `wiki-bootstrap-admin` allow rule and
a deny default while securing the initial administrator. The user changed the
administrator's email/password. After activating and verifying native Microsoft
login, the setup IP rule was removed and the Web App's frontend default action
changed to Allow so organization members and invited guests can reach it.
At initial SSO setup, public reading was disabled and anonymous book requests
redirected to login. On October 13, the user clarified that reading must be
public, with only editing behind Microsoft login; this has now been corrected
as recorded below. Unauthenticated API requests remain rejected (401).
These changes affected only the new wiki Web App.
The user reports successful sign-in with multiple organization members and a
Gmail guest. Human edit-attribution checks, a permanent scoped automation
credential, GitHub deployment wiring and domain cutover remain pending.

### Microsoft SSO setup — in progress

Use BookStack's native OpenID Connect flow so its token API remains usable.
The user created a separate Entra registration, displayed as `SHHA Bookstack`, in SHHA tenant
`4c35fa90-1858-4949-af6d-a5497eb87717`, with single-tenant account audience.
Single-tenant access includes invited guest objects in this directory; guests
must be invited/redeemed under the organization's existing guest process.
Verification confirms application/client ID
`d501fbfd-80ad-41a7-9fdc-26daef256168`, single-tenant audience AzureADMyOrg,
the exact preview callback below, sign-in enabled and assignment required false.
The user then created `Bookstack Azure SSO`, expiring April 11, 2027, and saved
its value directly as OIDC_CLIENT_SECRET in Azure. Microsoft accepted the
client credential during verification; no token or secret values were printed
or retained locally. Record a rotation before expiry in the operating procedure.
The preview Web redirect URI is:

`https://shha-wiki-fsgyhpgtg6gzc5aw.westus3-01.azurewebsites.net/oidc/callback`

Add the production wiki callback when preparing domain cutover. The new
enterprise application's assignment requirement is No to support the
user's requested access for all organization members and invited guests.
Editor is now the BookStack default registration role for ordinary users.
The user explicitly selected `admin@sandiahomeowners.org` as the owner of the
existing administrator profile after the CLI identity did not match that
profile. Its enabled account was resolved in the SHHA directory, and the
existing administrator was linked to its stable tenant object ID before
activation. Administrator role membership was retained; duplicate identity
links were checked. No other account was promoted. The prior mapping/default
role were saved privately in
`/Users/heidi/.config/shha-wiki/sso-before-activation.json` before the database
transaction. Private IDs are not recorded here. BookStack does not automatically
match existing accounts by email; keep `OIDC_EXTERNAL_ID_CLAIM=oid` stable.
Public OIDC settings were
prepared in Azure: this client ID, tenant-specific v2.0 issuer, discovery enabled,
external ID claim `oid`, display-name claim `name`, Microsoft button label,
auto-initiation disabled, claim dumping disabled and group syncing disabled.
AUTH_METHOD is now `oidc`. RP-initiated global Microsoft logout is disabled;
BookStack uses its own logout. Verification confirmed the Microsoft login
button, absence of the local password form, and an authorization-code redirect
to SHHA's tenant with the correct client ID/callback, openid/profile/email scopes,
S256 PKCE and state protection. The directory issuer was also verified.
No BookStack email-domain registration restriction was present, supporting
guest addresses. The user subsequently tested multiple internal users and a
Gmail guest successfully. Per-person editing still requires a live test with
the imported content. Do not expose tokens/claims or
enable claim dumping. Recovery if Microsoft login configuration fails: set
AUTH_METHOD back to `standard` in Azure and sign in with the administrator's
saved local password; preserve APP_KEY, the database and the private mapping
snapshot. Do not change identity claims during rollback.
On October 13, the maintained
LinuxServer.io image tag `version-v26.09.1` was verified in its Docker Hub
repository; its multi-architecture digest was
`sha256:0d66f65417fa667085849bf9b32b412ec9a90420773c4f47a95138c4711876b7`.
Use the matching amd64 image on App Service and retain the verified digest in
the deployment definitions when wiring CI/CD. Base application startup is
verified; Microsoft login has been tested by the user and content has been
imported below. CI/CD, production-domain cutover and recovery tests remain pending.
Use the actual server/resource-group names in later deployment
definitions; do not substitute the earlier proposed `shha-wiki-db` name.

### Content imported to Azure — October 13, 2026

The current DigitalOcean book was captured through its public portable ZIP
export at `/books/shha-it-help-guide/export/zip`. Source API credentials were
not present in this session and its JSON API required authentication; the
native live export avoided needing them or SSH. The source reports version
v26.03.2. Its public book/shelf inventory contains one book and no shelves;
the export contains the same 24 page IDs as the older repository snapshot,
with current live contents rather than the stale Markdown or pending drafts.

BookStack's native Azure import API imported **SHHA IT Help Guide**, seven
chapters and 24 pages. Verification checked every page, book/chapter
descriptions, tags, hierarchy and displayed order. All 45 tables and 225
external-link occurrences were preserved. Internal portable references were
mapped to the new Azure pages; zero cross-page anchor failures were found.
The current Quick Links includes ESComm, GovComm and PNMSTG SharePoint site
paths. No images, attachments or covers required transfer. Page HTML matches
the source after native link mapping, except two literal nonbreaking spaces
on Quick Links represented as equivalent `&nbsp;` entities. Native imports
renumbered sort priorities while preserving displayed sibling order.
The Editor role's view-all and edit-all page permissions were verified, and
no custom entity permission rows restrict the imported book or pages.

The source content was re-exported after import and was unchanged during the
operation. A fresh Azure portable ZIP was downloaded and confirmed to contain
all 24 pages; a converted Markdown book export was also saved privately.
These are content snapshots, not complete database/configuration backups.
Source and Azure archives plus the source/target ID mapping and verification
report are under `/Users/heidi/.config/shha-wiki/migration`, outside Git.

The reusable standard-library script is `scripts/bookstack_migrate.py`. Its
initial import requires an empty target, saves progress before mutations and
will not blindly retry an ambiguous write. Verification can be rerun without
creating duplicate content. It reads private credentials from
`/Users/heidi/.config/shha-wiki/target-api.json`; values are not printed or stored
in this repo. The temporary migration API token belongs to the linked BookStack
administrator and expires October 20, 2026. Prepare a dedicated scoped
automation credential for ongoing API publishing before this token expires.
The script was checked with `python3 -m py_compile` and the live import/readback
verification. No DigitalOcean content or hosting settings were changed.

[Review the guide](https://wiki.sandiahomeowners.org/books/shha-it-help-guide).
The user confirmed Azure content and editing work; production domain cutover
is now complete as recorded below. Microsoft login and edit attribution should
also be checked interactively on the production domain. Recovery testing and
hosting retirement remain pending. Git checkout relocation and GitHub deployment
wiring are also still pending; the migration script is saved in SHHA-wiki, whose
existing README does not by itself establish a Git checkout or CI/CD workflow.

### Production domain cutover — completed October 13, 2026

The user reviewed the Azure content, confirmed editing works, saved the DNS
records and explicitly authorized the domain binding, HTTPS and address update.
Before cutover, InMotion authoritative nameservers served a wiki A record
pointing to `64.23.133.121`, with TTL 14,400 seconds (four hours).
The production OIDC callback
`https://wiki.sandiahomeowners.org/oidc/callback` was added to SHHA Bookstack,
preserving the Azure preview callback. A fresh DigitalOcean export still matched
the source snapshot captured for import. Preserve all Azure edits made since
import; never blindly replace the Azure book with a fresh source ZIP.

Fresh source and Azure content snapshots, each with all 24 pages, were captured
privately before the DNS change. The authoritative and public recursive DNS
checks now confirm a CNAME to the Azure default host and the following TXT
ownership record. The published CNAME TTL remains 14,400 seconds; the TXT TTL
is 300 seconds.

| Type | Name | Value |
| --- | --- | --- |
| TXT | asuid.wiki.sandiahomeowners.org | F055BD8386F820D43FCDD8751B2DED8BEEB82D254F522486F1E662B13BDAB505 |

The CNAME target is
`shha-wiki-fsgyhpgtg6gzc5aw.westus3-01.azurewebsites.net`. Old resolver caches can
retain the prior DigitalOcean address for up to four hours. This computer's
macOS resolver still returned DigitalOcean during verification even though
InMotion, Cloudflare and Google DNS showed the Azure mapping. Azure checks
therefore connected directly to Azure while retaining the production hostname
for HTTP Host, TLS SNI and normal certificate/hostname validation.

Completed and verified:

- Bound `wiki.sandiahomeowners.org` to `shha-wiki`.
- Created and bound the free App Service Managed Certificate with SNI SSL;
  initial certificate expiry April 14, 2027. HTTPS Only remains enabled.
- Set `APP_URL=https://wiki.sandiahomeowners.org`, preserving APP_KEY, database
  credentials and all SSO/account/role settings.
- Applied the pinned BookStack v26.09.1 `bookstack:update-url` replacement rules
  through a parameterized MySQL transaction over the existing Azure data.
  Saved affected rows privately for rollback before committing. Two page HTML
  rows and two image URL rows changed. No old preview URLs remain in any of the
  command's target columns, including JSON-escaped setting values.
- Restarted the container; its startup script clears file caches. The current
  login page serves the production address and Microsoft login button.
- Compared API page/book/chapter data immediately before and after: all 24
  pages, 7 chapters and metadata matched after the intended URL substitution.
  Existing human edits, timestamps and author attribution were preserved.
- Verified production-domain API token reads/ZIP export and anonymous API denial
  (HTTP 401 with JSON Accept). Anonymous reading was initially denied during
  cutover and subsequently enabled as recorded below.
- Verified the Microsoft authorization redirect uses the SHHA tenant, existing
  client ID, production `/oidc/callback`, authorization-code flow and S256 PKCE.
  The Azure preview callback remains registered for recovery.

Fresh before/after API content and portable ZIP snapshots, plus the bounded
URL rollback snapshot, are protected under
`/Users/heidi/.config/shha-wiki/migration`, outside Git. They are not a complete
database backup. The private migration credential configuration retains the
Azure default hostname as its API transport; that endpoint still works. The
initial import script's DigitalOcean-hostname safety guard remains in place;
do not rerun its source comparison against content intentionally edited later.

Next human check: use a private browser window to sign in at the production
domain with an internal member and invited guest, and confirm an edit appears
under that user's name. These Microsoft account/MFA interactions were not
performed by the automated callback checks.

### Public reading, Microsoft editing — corrected October 13, 2026

The user explicitly clarified that the wiki must be publicly readable, with
Microsoft login required only for editing. Enabled BookStack's native
`app-public` setting. The existing Public role already grants content viewing,
export and revision viewing, with no create, edit, delete, comment, API or
administration permissions. No roles, Microsoft settings, user identities or
content were changed. The default role for Microsoft members and invited guests
remains Editor. The previous public-access setting was captured privately before
the change.

Verified without cookies or an account on the Azure production hostname:
homepage, book and all 24 pages return HTTP 200; anonymous editing and settings
requests are denied by redirects; no Edit action appears on anonymous page
views. The Microsoft login page remains available, and anonymous token API
requests still return HTTP 401. Use **Log in**, then **Microsoft**, to make
attributed edits. This corrects the earlier private-reading setup; public
reading is the intended ongoing configuration.

Keep the old wiki A value recorded for rollback. Once Azure receives new edits,
any rollback must preserve them rather than route users to an older content
copy. DigitalOcean retirement remains pending until the domain/auth/content
checks and recovery/workload-retirement requirements are met. No source server
or DigitalOcean hosting actions are authorized by the domain walkthrough.

### Editorial review preparation — October 13, 2026

Checked the user's pasted Quick Links HTML against the current Azure page via
authenticated API reads. All ten SharePoint links match exactly and in the same
order, including `/sites/ESComm`, `/sites/GovComm` and `/sites/PNMSTG`. No content
change was needed. This confirms the stored URLs against the user's known-good
reference, not each committee member's SharePoint access permissions.

The authoritative DNS, Cloudflare and Google resolvers route the wiki to Azure
(`20.118.138.133` at this check). This computer's OS resolver still returned the
old DigitalOcean IP `64.23.133.121`. Both source and Azure returned HTTP 200 with
no redirect for the homepage, book and login paths; the observed old site is a
cached DNS destination rather than a production-origin redirect. The old
four-hour TTL can persist until cached answers expire. Private browsing does
not clear the operating system/network DNS cache.

Actual repository status:

- The existing remote is GitHub
  `Sandia-Heights-Homeowners-Association/IT-help-guide`, not GitLab. GitHub reports
  this repository is public. If wiki pages become restricted, exclude those
  pages from a public mirror or use an appropriately private repository.
- Its remote `codex/board-member-bookstack-revision` branch contains the July 31,
  2026 export: all 24 pages of book 1 in paired Markdown/HTML, combined Markdown
  and manifest metadata. Remote `main` has no `bookstack-current/` tree.
- `IT-help-guide` has uncommitted guide changes and unpublished drafts; preserve
  them separately from a refresh of exported content.
- SHHA-wiki still holds this plan and the migration script, not a migrated Git
  checkout or current committed mirror. Recent Azure content snapshots are
  private, outside Git. No automatic export/sync workflow is installed.

Use BookStack as the canonical content store. Browser WYSIWYG edits and new
pages in book 1 are picked up on the next API export. The existing exporter
does not enumerate additional books or download image binaries. Keep HTML and
metadata with readable Markdown; do not round-trip converted Markdown onto
rich WYSIWYG pages. For reliable ongoing operation, finish repository relocation,
prepare a permanent read-only export token before the temporary token expires
October 20, and implement staged/verified exports before replacing the mirror.
Export before API edits and again after publishing, preserving newer human
changes. A scheduled read-only export plus an explicit refresh action is the
recommended future workflow, not an already configured service.

The content/visibility review should use a separate SHHA-wiki project and a
fresh conversation after repository organization, retaining this README as
handoff context. All current pages are publicly readable. Start by deciding the
audiences for Staff, GRIT Internal Production Reference, Systems Inventory,
Controls & Security, and HR & Personnel Management, then verify instructions,
links and Microsoft member/guest editing per page. Page titles alone do not
establish whether their contents should be restricted; do not change visibility
without the user's decisions. Public wiki access does not grant SharePoint
access. Existing internal API token access and Editor registration remain intact.

### Overall sequence

1. Move the existing repository into SHHA-wiki with Git history and local edits
   intact, incorporating this plan; establish GitHub remote/name and ignore rules.
2. Make source API credentials available securely, inventory capabilities and
   pull current content into private staging without modifying DigitalOcean.
3. Implement/check Azure definitions and workflow configuration, finalize resource
   costs, and deploy/verify a clean BookStack preview.
4. Configure SSO, target API credentials and complete migration of the current
   content. Verify hierarchy, links, visual editing and API control.
5. Complete final sync, hostname cutover, backups and retirement checks.

This folder initially contained no repository and still is not a Git checkout.
Azure BookStack deployment, Microsoft SSO, content import and domain/TLS cutover
are now implemented. Moving the checkout and installing GitHub workflows remain
pending. Source content was obtained through its public native portable ZIP
export because source API credentials were unavailable. The prior
SSH/VM/database-restore plan is superseded.

## References

- [BookStack export/import formats](https://www.bookstackapp.com/docs/user/export-import/)
- [BookStack ZIP API release](https://www.bookstackapp.com/blog/bookstack-release-v25-07/)
- [Portable ZIP scope and format](https://github.com/BookStackApp/BookStack/blob/development/dev/docs/portable-zip-file-format.md)
- [BookStack update requirements](https://www.bookstackapp.com/docs/admin/updates/)
- [Azure container deployment](https://learn.microsoft.com/en-us/azure/app-service/deploy-ci-cd-custom-container)
- [Azure persistent file mounts](https://learn.microsoft.com/en-us/azure/app-service/configure-connect-to-azure-storage)
- [GitHub OIDC authentication to Azure](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-azure)
