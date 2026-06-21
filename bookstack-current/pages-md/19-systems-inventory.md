# Systems Inventory

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

**TODO:** Document the membership database system.

<table id="bkmrk-system-nametodo%3A-wha"><tbody><tr><td>**System name**</td><td>**TODO:** What system/software is used?</td></tr><tr><td>**Type**</td><td>**TODO:** Cloud-based or local?</td></tr><tr><td>**Primary admin**</td><td>**TODO:** Is Ryan the primary outside admin?</td></tr><tr><td>**Backup admin**</td><td>**TODO:** Is there a backup?</td></tr><tr><td>**Data stored**</td><td>**TODO:** What member data is in this system? (names, addresses, dues status, etc.)</td></tr></tbody></table>

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


## 8. DigitalOcean Productivity App Hosting

SHHA has a DigitalOcean droplet for hosting ad-hoc productivity apps: small internal tools that help office staff or volunteers with specific workflows but are not the public website and are not Microsoft 365 itself.

SHHA Reminders is one of these apps. It runs in Docker on the droplet, uses Caddy for HTTPS reverse proxying, and is available at [https://reminders.sandiahomeowners.org](https://reminders.sandiahomeowners.org). The app listens internally on port `3030`, with Caddy proxying public HTTPS traffic to `127.0.0.1:3030`.

<table><tbody><tr><td>**Hosting**</td><td>DigitalOcean droplet</td></tr><tr><td>**Current app**</td><td>SHHA Reminders</td></tr><tr><td>**Production URL**</td><td>[https://reminders.sandiahomeowners.org](https://reminders.sandiahomeowners.org)</td></tr><tr><td>**App directory**</td><td>`/opt/shha/SHHA-emailer`</td></tr><tr><td>**Internal port**</td><td>`3030`</td></tr><tr><td>**Reverse proxy**</td><td>Caddy</td></tr><tr><td>**Operational files to back up**</td><td>`.env`, `data/state.json`, and `/etc/caddy/Caddyfile`</td></tr><tr><td>**Secrets note**</td><td>Do not commit the production `.env` file to git.</td></tr></tbody></table>

## 9. Other Systems

**TODO:** Are there additional systems not listed above? Examples might include:

- Bulk email / email blast service (Mailchimp, Constant Contact, etc.)
- Google Workspace (shared Google Calendar for Board reminders uses Gmail — is there a full Google account?)
- Domain registrar for sandiahomeowners.org — **TODO:** who manages DNS and domain renewal?
- Any other SaaS tools or vendor portals
