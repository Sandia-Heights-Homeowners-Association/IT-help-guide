# SOP: New Users, Mailboxes & Groups

This SOP is written for SHHA staff who are comfortable with basic Microsoft admin work and need a reliable step-by-step process for setting up new groups, shared mailboxes, and related addresses.

**Start here every time:** [admin.microsoft.com](https://admin.microsoft.com)

---

## Quick Start: What Are You Trying to Set Up?

<table id="bkmrk-if-you-need...go-to-"><thead><tr><th>If you need...</th><th>Go to this section</th></tr></thead><tbody><tr><td>A new task-force or committee mailing address that sends to all members</td><td>[SOP A: Create a Microsoft 365 Group (Mailing List)](#bkmrk-sop-a%3A-create-a-micr)</td></tr><tr><td>A SharePoint document site for a new committee or task force</td><td>[SOP: Create a Committee SharePoint Site](/books/shha-it-help-guide/page/sop-create-a-committee-sharepoint-site)</td></tr><tr><td>A role inbox for a chair or lead (keeps history when people rotate)</td><td>[SOP B: Create a Shared Mailbox](#bkmrk-sop-b%3A-create-a-shar)</td></tr><tr><td>A friendly one-off address like wildfire@sandiahomeowners.org</td><td>[SOP C: Add an Alias](#bkmrk-sop-c%3A-add-an-alias-)</td></tr><tr><td>An internal staff account with first.last@sandiahomeowners.org login</td><td>[SOP D: Add a Licensed User](#bkmrk-sop-d%3A-add-a-new-lic)</td></tr><tr><td>An external volunteer using Gmail/Yahoo/etc.</td><td>[SOP E: Add an External Guest](#bkmrk-sop-e%3A-add-an-extern)</td></tr></tbody></table>

---

## Task Force Fast Path (Most Common New Setup)

For a new short-term task force, the normal pattern is:

1. Create a **Microsoft 365 Group** for the task-force mailing list.
2. Add members (including external guests) and always include `itadmin@sandiahomeowners.org`.
3. Create a **Shared Mailbox** for the task-force lead/chair if they need role continuity.
4. Add an optional **Alias** (for example, `wildfire@sandiahomeowners.org`) if a friendlier address is useful.
5. Confirm the Microsoft 365 group-connected **SharePoint site** exists; do not create a duplicate.
6. Configure document permissions using [SOP: Create a Committee SharePoint Site](/books/shha-it-help-guide/page/sop-create-a-committee-sharepoint-site) and send members the [Committee SharePoint Guide](/books/shha-it-help-guide/page/committee-sharepoint-guide).
7. Test email delivery and update the Quick Links directory.

If you only need one address that emails the whole task force, do **SOP A** only.

---

## SOP A: Create a Microsoft 365 Group (Mailing List)

**Use this for:** any committee/task-force address that should email all members.

**Menu path:** [admin.microsoft.com](https://admin.microsoft.com) → **Teams &amp; groups** → **Active teams &amp; groups** → **Add a group**

### Step-by-step

1. Open [admin.microsoft.com](https://admin.microsoft.com) and sign in.
2. In the left menu, click **Teams &amp; groups**.
3. Click **Active teams &amp; groups**.
4. Click **Add a group**.
5. Select **Microsoft 365** as the group type, then click **Next**.
6. Enter: 
    - **Name**: Full task-force name (example: Wildfire Preparedness Task Force)
    - **Description**: Short purpose statement
    
    Click **Next**.
7. Add at least one **Owner** (usually office staff), then click **Next**.
8. Set: 
    - **Group email address** (example: `wildfiretf` → `wildfiretf@sandiahomeowners.org`)
    - **Privacy**: usually **Private**
    - Leave "Create a team for this group" **off** unless Teams is explicitly needed
    
    Click **Next** then **Create group**.
9. Open the new group, then go to **Settings**.
10. **Enable external email:** turn on **Let people outside the organization email this group**.
11. **Enable inbox delivery:** turn on **Send copies of team emails and events to team members' inboxes**.
12. Go to **Members** → **Add members**.
13. Add all task-force members (internal and external as available).
14. **Required:** Add `itadmin@sandiahomeowners.org` as a member for archive continuity.
15. Send a test email to the new group address and confirm delivery.

### Done checklist

- Group exists
- Owners added
- All members added
- External email enabled
- Inbox delivery enabled
- `itadmin@` added
- Test email delivered

---

## SOP B: Create a Shared Mailbox (Chair/Lead Inbox)

**Use this for:** role inboxes that must persist when people rotate (chair, lead, coordinator).

**Menu path:** [admin.microsoft.com](https://admin.microsoft.com) → **Teams &amp; groups** → **Shared mailboxes** → **Add a shared mailbox**

### Step-by-step

1. In admin center, go to **Teams &amp; groups** → **Shared mailboxes**.
2. Click **Add a shared mailbox**.
3. Enter: 
    - **Name** (example: Wildfire Task Force Lead)
    - **Email** (example: `wildfirelead` → `wildfirelead@sandiahomeowners.org`)
4. Click **Save changes**.
5. Open the mailbox details and click **Members** → **Edit** → **Add members**.
6. Add licensed users who should access the mailbox (usually current lead/chair and optional backup).
7. Set **Send As** (or delegation) permissions for the same users.
8. Ask one user to verify in [outlook.com](https://outlook.com) that: 
    - The mailbox appears (or can be manually added)
    - They can receive mail
    - They can send with the shared mailbox in the From field

### Important notes

- Shared mailboxes are role-based, not person-based.
- Do not create separate personal accounts for each chair unless they truly need their own licensed login.

---

## SOP C: Add an Alias (One-Off Friendly Address)

**Use this for:** addresses like `wildfire@sandiahomeowners.org` that should route to an existing group or mailbox.

**Menu path:** [admin.microsoft.com](https://admin.microsoft.com) → select target group/mailbox → **Email aliases** / **Email address** settings

### Step-by-step

1. Decide destination first: should alias route to the **group** or the **shared mailbox**?
2. For group destination: 
    - Go to **Teams &amp; groups** → **Active teams &amp; groups**.
    - Select the group.
    - Open email settings and add alias address.
3. For shared mailbox destination: 
    - Go to **Teams &amp; groups** → **Shared mailboxes**.
    - Select mailbox.
    - Open email settings and add alias address.
4. Save changes.
5. Send test email to alias and verify it arrives in the expected destination.

---

## SOP D: Add a New Licensed User (Internal Staff)

**Use this for:** staff/admin accounts that need a personal Microsoft login (`first.last@sandiahomeowners.org`).

**Menu path:** [admin.microsoft.com](https://admin.microsoft.com) → **Users** → **Active users** → **Add a user**

### Step-by-step

1. Go to **Users** → **Active users** → **Add a user**.
2. Enter name and username (`first.last` format).
3. Generate temporary password and require password change at first sign-in.
4. Assign correct M365 license.
5. Finish adding user.
6. Add user to appropriate groups/shared mailbox access as needed.

---

## SOP E: Add an External Guest (Volunteer)

**Use this for:** most volunteers; avoids paid license cost.

**Menu path:** [admin.microsoft.com](https://admin.microsoft.com) → **Users** → **Guest users** (or Entra invite flow)

### Step-by-step

1. Invite external user with personal email address.
2. Ask them to accept Microsoft invitation email.
3. After acceptance, add them to needed Microsoft Groups.
4. Verify they receive test group email.

---

## Send The Onboarding Email

After setup and testing are complete, choose the matching message from [Office Onboarding Email Templates](/books/shha-it-help-guide/page/office-onboarding-email-templates). Replace every placeholder and test every link before sending.

## Final Validation (Do This Before You Close the Ticket)

- Group email tested
- Shared mailbox tested (if created)
- Alias tested (if created)
- `itadmin@` included in group
- Quick Links directory updated with new addresses
- Requester notified that setup is complete

---

## Where To Go Next

- [M365 Email Building Blocks](/books/shha-it-help-guide/page/m365-email-building-blocks) for choosing the right pattern first
- [M365 Email Groups, Role Inboxes &amp; Responsibilities](/books/shha-it-help-guide/page/m365-email-groups-role-inboxes-responsibilities) for governance and handoff rules
- [SOP: Create a Committee SharePoint Site](/books/shha-it-help-guide/page/sop-create-a-committee-sharepoint-site) for document-library setup and permissions
- [Quick Links &amp; Directory](/books/shha-it-help-guide/page/quick-links-directory) to keep the address list current
