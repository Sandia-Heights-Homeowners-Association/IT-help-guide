# M365 Email Groups, Role Inboxes & Responsibilities

*Operational reference for office staff, IT admin, and future volunteers — mailing lists, shared mailboxes, licensing, SOPs, and governance.*

---

<a id="bkmrk--1"></a>## Quick Overview

SHHA uses two different patterns for email collaboration:

 <table id="bkmrk-patterntechnologyexa"> <thead><tr><th>Pattern</th><th>Technology</th><th>Examples</th></tr></thead> <tbody> <tr> <td>**Committee mailing lists**</td> <td>Microsoft Groups</td> <td>`shha-all@`, `csc@`, `acc@`</td> </tr> <tr> <td>**Role-based addresses**</td> <td>Shared mailboxes</td> <td>`president@`, `cscchair@`, `accchair@`</td> </tr> </tbody> </table>

---

<a id="bkmrk--3"></a>## Design Principles

- **Role continuity over individual ownership** — email addresses stay constant when people rotate in/out.
- **Least cost for volunteers** — external volunteers do not require paid M365 licenses.
- **Operational traceability** — group membership changes trigger Power Automate notifications.
- **Institutional archive** — `admin@` is included in all groups as a permanent archive recipient.
 
---

<a id="bkmrk--5"></a>## Microsoft Groups (Mailing Lists)

Each committee has a Microsoft Group that acts as its mailing list.

 <table id="bkmrk-groupaddress-all-mem"> <thead><tr><th>Group</th><th>Address</th></tr></thead> <tbody> <tr><td>All members</td><td>`shha-all@sandiahomeowners.org`</td></tr> <tr><td>CSC</td><td>`csc@sandiahomeowners.org`</td></tr> <tr><td>ACC</td><td>`acc@sandiahomeowners.org`</td></tr> <tr><td>Others</td><td>One group per committee</td></tr> </tbody> </table>

**Behavior:** Sending to the group distributes to all members. Membership is maintained by staff (primary owner: Anna). External participants can be included.

---

<a id="bkmrk--7"></a>## Shared Mailboxes (Role Inboxes)

Only six officer role addresses are shared mailboxes tied to positions, not people: President, Vice President, Secretary, Treasurer, ACC Chair, and CSC Chair. Other committee chairs and task-force leads use their own account and the committee mailing list.

 <table id="bkmrk-roleaddress-csc-chai"> <thead><tr><th>Role</th><th>Address</th></tr></thead> <tbody> <tr><td>CSC Chair</td><td>`cscchair@sandiahomeowners.org`</td></tr> <tr><td>ACC Chair</td><td>`accchair@sandiahomeowners.org`</td></tr> <tr><td>President</td><td>`president@sandiahomeowners.org`</td></tr> <tr><td>Vice President</td><td>`vicepresident@sandiahomeowners.org`</td></tr> <tr><td>Secretary</td><td>`secretary@sandiahomeowners.org`</td></tr> <tr><td>Treasurer</td><td>`treasurer@sandiahomeowners.org`</td></tr> </tbody> </table>

Each incoming officer receives both **Full Access** and **Send As** permission through the officer's own licensed SHHA account. Officers cannot log in directly to the shared mailbox and must add it manually in Outlook because it may not appear automatically. For official role correspondence, send from the role mailbox or copy it so the shared mailbox remains the archive.

### Access model

- People do **not** log in directly as the role mailbox.
- Authorized users open the shared mailbox from their own licensed account.
- Example: `phil.krehbiel@sandiahomeowners.org` can open `accchair@sandiahomeowners.org`.
 
### When leadership changes

1. Remove predecessor access.
2. Grant successor access.
3. Keep the role mailbox address unchanged.
 
---

<a id="bkmrk--9"></a>## Archive Mailbox (`admin@`)

- `admin@` is a member of **all** groups.
- Purpose: permanent archive and continuity.
- `admin@` is **not actively monitored** for normal operations.
 
---

<a id="bkmrk--11"></a>## Power Automate Membership Notifications

A Power Automate flow sends email notifications whenever group membership changes.

- Provides audit visibility.
- Alerts staff to unexpected changes.
- Supports handoffs and troubleshooting.
 
---

<a id="bkmrk--13"></a>## Licensing and External Volunteers

 <table id="bkmrk-user-typelicense-nee"> <thead><tr><th>User type</th><th>License needed?</th><th>Capabilities</th></tr></thead> <tbody> <tr><td>External volunteers</td><td>**No**</td><td>Group email delivery, SharePoint guest access</td></tr> <tr><td>Licensed staff / admin</td><td>Yes (paid M365)</td><td>Group administration, shared mailbox access, full portal</td></tr> </tbody> </table>

---

<a id="bkmrk--15"></a>## Responsibilities Matrix

 <table id="bkmrk-responsibilityprimar"> <thead><tr><th>Responsibility</th><th>Primary</th><th>Backup</th><th>Notes</th></tr></thead> <tbody> <tr><td>Maintain committee group membership</td><td>Anna (staff)</td><td>IT admin</td><td>Add/remove members, verify accuracy</td></tr> <tr><td>Manage shared mailbox permissions</td><td>Anna + IT admin</td><td>IT admin</td><td>Remove predecessor, add successor</td></tr> <tr><td>Ensure `admin@` in all groups</td><td>IT admin</td><td>Anna</td><td>Required for archive continuity</td></tr> <tr><td>Monitor membership-change notifications</td><td>Anna</td><td>IT admin</td><td>Power Automate emails = operational signal</td></tr> <tr><td>Troubleshoot delivery/access issues</td><td>IT admin</td><td>Anna</td><td>Includes mailbox permissions and group settings</td></tr> </tbody> </table>

---

<a id="bkmrk--17"></a>## SOP: Add a Person to a Committee Mailing List

1. Confirm committee and target group address.
2. Verify whether person is internal staff or external volunteer.
3. Add to the correct Microsoft Group membership.
4. Confirm `admin@` remains a member.
5. Verify Power Automate sends membership-change notification.
6. Ask requester to test delivery (or send a test message).
 
---

<a id="bkmrk--19"></a>## SOP: Remove a Person from a Committee Mailing List

1. Confirm removal request and effective date.
2. Remove member from the Microsoft Group.
3. Verify Power Automate notification is received.
4. If person held one of the six officer roles, check related shared mailbox permissions.
 
---

<a id="bkmrk--21"></a>## SOP: Leadership Transition for Role Inbox

1. Identify affected role mailbox (e.g., `accchair@`).
2. Remove outgoing person's mailbox permissions.
3. Grant incoming person's mailbox permissions.
4. Validate that incoming person can open the shared mailbox from their own account.
5. Keep address and historical content in place for continuity.
 
---

<a id="bkmrk--23"></a>## SOP: New Committee Creation

1. Create new Microsoft Group for the committee.
2. Add initial committee members.
3. Add `admin@` as member for archiving.
4. Ensure membership-change notifications are active.
5. Record the group in the committee/group inventory.
 
---

<a id="bkmrk--25"></a>## Governance Rules

- Every committee must have exactly one official mailing-list group.
- Every committee group must include `admin@`.
- Shared mailbox addresses represent roles and must not be treated as personal identities.
- Access to shared role inboxes must be updated promptly on leadership change.
- Membership changes should be performed by staff owner (Anna) or IT admin only.
 
---

<a id="bkmrk--27"></a>## Recommended Recordkeeping

Maintain a simple inventory table (in the wiki or internal operations file) with:

- Committee name
- Group email address
- Current chair role mailbox (if applicable)
- Current permission holders
- Last membership review date
- Last updated by
 
<div id="bkmrk-this-makes-volunteer">This makes volunteer/staff handoff much easier.</div>---

<a id="bkmrk--29"></a>## Common Issues and Checks

### Person does not receive committee emails

- Member exists in correct Microsoft Group
- Email address is correct
- Sender used the correct group address
- Recent change triggered notification (confirms update happened)
 
### New officer cannot open role mailbox

- Shared mailbox permission was granted to the person's licensed account
- User is opening mailbox from their own account context
- Predecessor access was removed (to avoid confusion)
 
### Missing archive history

- `admin@` is still a member of the affected group
- Group delivery settings have not been altered
 
---

<a id="bkmrk--31"></a>## Handoff Checklist (Staff / Volunteer Transition)

- Review all committee group memberships for accuracy.
- Verify all six active officer roles have correct shared mailbox access.
- Remove stale permissions from former role holders.
- Confirm `admin@` is in every group.
- Confirm membership-change notification flow is working.
- Update inventory table and date-stamp the review.
 
---

<a id="bkmrk--33"></a>## Key Contacts and Ownership

 <table id="bkmrk-rolecontact-group-me"> <thead><tr><th>Role</th><th>Contact</th></tr></thead> <tbody> <tr><td>Group membership owner</td><td>Anna (staff)</td></tr> <tr><td>Technical owner / escalation</td><td>IT admin</td></tr> <tr><td>Archive mailbox</td><td>`admin@` (not actively monitored)</td></tr> </tbody> </table>

<div id="bkmrk-if-ownership-changes">**If ownership changes, update this section immediately.**</div>---

## Related Resources

- [M365 Email Building Blocks](/books/shha-it-help-guide/page/m365-email-building-blocks) — understand the four email patterns (personal mailbox, shared mailbox, mailing list, alias) and when to use each
- [SOP: New Users, Mailboxes &amp; Groups](/books/shha-it-help-guide/page/sop-new-users-mailboxes-groups) — step-by-step admin procedures for creating users, shared mailboxes, groups, and aliases
- [Office Onboarding Email Templates](/books/shha-it-help-guide/page/office-onboarding-email-templates) — copy-and-send messages for the people who receive new access
