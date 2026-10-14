# Systems Inventory

This page lists the technology systems SHHA uses. For each system, we document what it does, who administers it, and how it is accessed.

*Items marked **TODO** need information filled in by someone with direct knowledge of that system.*

## 1. Microsoft 365

Microsoft 365 is SHHA's primary platform for email, mailing lists (Microsoft Groups), shared role mailboxes, and file storage (SharePoint).

<table id="bkmrk-typecloud-based-%28mic"><tbody><tr><td>**Type**</td><td>Cloud-based (Microsoft-hosted)</td></tr><tr><td>**Primary admin**</td><td>Anna (office staff) handles day-to-day membership changes; IT admin handles mailbox permissions and configuration</td></tr><tr><td>**Backup admin**</td><td>**TODO:** Identify and document a backup administrator</td></tr><tr><td>**Login**</td><td>[admin.microsoft.com](https://admin.microsoft.com) (admin), [outlook.com](https://outlook.com) (email), SharePoint links (files)</td></tr><tr><td>**Licensing**</td><td>Only office staff and IT admin need paid licenses; volunteers are free external guests</td></tr></tbody></table>

## 2. QuickBooks

Used for SHHA financial accounting.

<table id="bkmrk-typecloud-based-prim"><tbody><tr><td>**Type**</td><td>Cloud-based</td></tr><tr><td>**Primary admin / user**</td><td>**TODO:** Who is the primary user? (Treasurer? Office staff?)</td></tr><tr><td>**Backup**</td><td>**TODO:** Is there a backup user with access?</td></tr><tr><td>**Login**</td><td>**TODO:** URL and login method</td></tr><tr><td>**Notes**</td><td>**TODO:** Version (Online vs Desktop), billing, who pays for the subscription</td></tr></tbody></table>

## 3. Membership Database

The association website's **MariaDB database** owns homeowner, property and resident-link records. Corrections belong in the website, through its authorized staff or maintainer. The public dashboard and staff toolbox read approved data through dedicated SELECT-only access; neither writes changes back to this database.

Confirm website administration, backups and responsible contacts with the office. Detailed connection, permissions and recovery information belong in private operating documentation.

## 4. Gusto

Used for payroll and employee benefits administration.

<table id="bkmrk-typecloud-based-prim-1"><tbody><tr><td>**Type**</td><td>Cloud-based</td></tr><tr><td>**Primary admin**</td><td>**TODO:** Who manages Gusto? (Office manager? Treasurer?)</td></tr><tr><td>**Backup**</td><td>**TODO:** Is there a backup admin?</td></tr><tr><td>**Login**</td><td>[app.gusto.com](https://app.gusto.com)</td></tr><tr><td>**Notes**</td><td>**TODO:** How many employees are on payroll? Billing responsibility?</td></tr></tbody></table>

## 5. SHHA Website

The public-facing website at [sandiahomeowners.org](https://sandiahomeowners.org).

<table id="bkmrk-typetodo%3A-what-platf"><tbody><tr><td>**Type**</td><td>**TODO:** What platform/CMS runs the website? (WordPress, Squarespace, custom?)</td></tr><tr><td>**Hosting**</td><td>**TODO:** Where is it hosted? Cloud-based?</td></tr><tr><td>**Primary owner**</td><td>**TODO:** Who manages content updates?</td></tr><tr><td>**Backup owner**</td><td>**TODO:** Is there a backup person?</td></tr><tr><td>**Outside consultant**</td><td>**TODO:** Is there a web consultant? If so, who? How are they paid?</td></tr><tr><td>**Login**</td><td>**TODO:** Admin URL and login method</td></tr></tbody></table>

## 6. GRIT Newsletter

The GRIT is SHHA's community newsletter, currently produced monthly.

<table id="bkmrk-production-tooltodo%3A"><tbody><tr><td>**Production tool**</td><td>**TODO:** What software is used for layout? (InDesign, Canva, Google Docs, etc.)</td></tr><tr><td>**Distribution method**</td><td>**TODO:** Print, email, or both?</td></tr><tr><td>**Editor / layout person**</td><td>**TODO:** Who currently does layout and editing?</td></tr><tr><td>**Gmail account**</td><td>shhagrit@gmail.com — **TODO:** document what this Gmail is used for (submissions? Google Drive access? legacy?)</td></tr><tr><td>**Related page**</td><td>See the *GRIT Layout Monthly Guide* in the Specialty Topics chapter for the step-by-step production process</td></tr></tbody></table>

## 7. Square

Used for Sandia Tram ticket sales and advertising payments.

<table id="bkmrk-typecloud-based-prim-2"><tbody><tr><td>**Type**</td><td>Cloud-based</td></tr><tr><td>**Primary user**</td><td>**TODO:** Who manages Square transactions?</td></tr><tr><td>**Backup**</td><td>**TODO:** Is there a backup?</td></tr><tr><td>**Login**</td><td>[squareup.com](https://squareup.com)</td></tr><tr><td>**Notes**</td><td>**TODO:** What specific transactions go through Square? Revenue amounts?</td></tr></tbody></table>

## 8. Public Utilities, Staff Toolbox and Wiki Hosting

SHHA now maintains public statistics, a public neighborhood map, GRIT submissions and a Microsoft-authenticated staff toolbox. See [Public Utilities and SHHA Toolbox](https://wiki.sandiahomeowners.org/books/shha-it-help-guide/page/public-utilities-and-shha-toolbox) for working links and audiences.

The toolbox and separate statistics dashboard run on Azure App Service. BookStack runs in its own Azure container with MySQL and persistent file storage. The map runs on GitHub Pages. The public GRIT domain still uses its existing Vercel host while its Azure version is maintained separately; its domain cutover must be verified before describing the public site as Azure-hosted.

Email Reminders is part of the **SHHA Toolbox**; its standalone web address is retired. Do not use the former DigitalOcean app-directory or reverse-proxy instructions as the current deployment guide. Retirement of any remaining legacy hosting/state is a separate operational check.

[IT Infrastructure and Handover](https://wiki.sandiahomeowners.org/books/shha-it-help-guide/page/it-infrastructure-and-handover) explains ownership, repositories, hosting/data boundaries, deployments and recovery responsibilities for the next IT professional.

## SHHA GitHub

SHHA's GitHub organization is [https://github.com/Sandia-Heights-Homeowners-Association](https://github.com/Sandia-Heights-Homeowners-Association).

This is where SHHA stores source code and local documentation backups for technical projects. For approved individual access, contact office staff or IT Help; confirm organizational ownership and recovery arrangements.

## 9. Other Systems

**TODO:** Are there additional systems not listed above? Examples might include:

- Bulk email / email blast service (Mailchimp, Constant Contact, etc.)
- Google Workspace (shared Google Calendar for Board reminders uses Gmail — is there a full Google account?)
- Domain registrar for sandiahomeowners.org — **TODO:** who manages DNS and domain renewal?
- Any other SaaS tools or vendor portals
