# SHHA Microsoft 365: Email Groups, Role Inboxes, and Responsibilities

## Purpose
This document explains how SHHA uses Microsoft 365 for:
- committee mailing lists (Microsoft Groups)
- shared role inboxes (chair and executive role addresses)
- external volunteers who do not have paid Microsoft 365 licenses
- staff responsibilities for maintaining group membership
- automated membership-change notifications from Power Automate

Use this as the operational reference for office staff, IT admin, and future volunteers.

---

## Quick Overview
SHHA uses two different patterns for email collaboration:

1. **Committee mailing lists = Microsoft Groups**
   - Examples: `shha-all@sandiahomeowners.org`, `csc@sandiahomeowners.org`, `acc@sandiahomeowners.org`
   - One group exists for each committee.
   - External volunteers can receive messages without needing paid M365 user licenses.

2. **Role-based public addresses = Shared mailboxes**
   - Examples: `cscchair@sandiahomeowners.org`, `accchair@sandiahomeowners.org`
   - Executive role inboxes include:
     - `president@`
     - `vicepresident@`
     - `secretary@`
     - `treasurer@`
     - `accchair@`
     - `cscchair@`
   - These are role accounts, not personal accounts.

---

## Design Principles
- **Role continuity over individual ownership**: Email addresses stay constant when people rotate in/out of positions.
- **Least cost for volunteers**: External volunteers should not require paid M365 licenses.
- **Operational traceability**: Group membership changes trigger notifications via Power Automate.
- **Institutional archive**: `itadmin@` is included in all groups as a permanent archive recipient.

---

## Core Components

### 1) Microsoft Groups (Mailing Lists)
Microsoft Groups are used as SHHA committee mailing lists.

Examples:
- `shha-all@sandiahomeowners.org`
- `csc@sandiahomeowners.org`
- `acc@sandiahomeowners.org`
- additional group for each committee

Behavior:
- Sending to the group distributes to all members.
- Membership is maintained by staff (primary owner: Anna).
- External participants can be included as needed.

### 2) Shared Mailboxes (Role Inboxes)
Chair and executive role addresses are shared mailboxes tied to positions, not people.

Examples:
- `cscchair@sandiahomeowners.org`
- `accchair@sandiahomeowners.org`
- `president@...`, `vicepresident@...`, `secretary@...`, `treasurer@...`

Access model:
- People do **not** log in directly as the role mailbox.
- Authorized users open the shared mailbox from their own licensed account.
- Example: `phil.krehbiel@sandiahomeowners.org` can open `accchair@sandiahomeowners.org`.

When leadership changes:
- remove predecessor access
- grant successor access
- keep the role mailbox address unchanged

### 3) Archive Mailbox (`itadmin@`)
- `itadmin@` is a member of **all** groups.
- Purpose: permanent archive and continuity.
- `itadmin@` is **not actively monitored** for normal operations.

### 4) Power Automate Membership Notifications
A Power Automate flow sends email notifications whenever group membership changes.

Purpose:
- provide audit visibility
- alert staff to unexpected changes
- support handoffs and troubleshooting

---

## Licensing and External Volunteers

### External volunteers
- External volunteers should be added in ways that do not require paid SHHA M365 user licenses.
- They can participate through group email delivery.

### Licensed staff/admin users
- Office staff and IT admin have full licensed accounts.
- These licensed accounts perform group administration and shared mailbox access.

---

## Responsibilities Matrix

| Responsibility | Primary | Backup | Notes |
|---|---|---|---|
| Maintain committee group membership | Anna (staff) | IT admin | Add/remove members, verify accuracy |
| Manage shared mailbox permissions for role transitions | Anna + IT admin | IT admin | Remove predecessor, add successor |
| Ensure `itadmin@` remains in all groups | IT admin | Anna | Required for archive continuity |
| Monitor membership-change notifications | Anna | IT admin | Power Automate emails are operational signal |
| Troubleshoot delivery/access issues | IT admin | Anna | Includes mailbox permissions and group settings |

---

## Standard Operating Procedures

### SOP 1: Add a person to a committee mailing list
1. Confirm committee and target group address.
2. Verify whether person is internal staff or external volunteer.
3. Add to the correct Microsoft Group membership.
4. Confirm `itadmin@` remains a member.
5. Verify Power Automate sends membership-change notification.
6. Ask requester to test delivery (or send a test message).

### SOP 2: Remove a person from a committee mailing list
1. Confirm removal request and effective date.
2. Remove member from the Microsoft Group.
3. Verify Power Automate notification is received.
4. If person held a role, check related shared mailbox permissions.

### SOP 3: Leadership transition for role inbox
1. Identify affected role mailbox (for example, `accchair@`).
2. Remove outgoing person’s mailbox permissions.
3. Grant incoming person’s mailbox permissions.
4. Validate that incoming person can open the shared mailbox from their own account.
5. Keep address and historical content in place for continuity.

### SOP 4: New committee creation
1. Create new Microsoft Group for the committee.
2. Add initial committee members.
3. Add `itadmin@` as member for archiving.
4. Ensure membership-change notifications are active.
5. Record the group in the committee/group inventory.

---

## Governance Rules
- Every committee must have exactly one official mailing-list group.
- Every committee group must include `itadmin@`.
- Shared mailbox addresses represent roles and must not be treated as personal identities.
- Access to shared role inboxes must be updated promptly on leadership change.
- Membership changes should be performed by staff owner (Anna) or IT admin only.

---

## Recommended Recordkeeping
Maintain a simple inventory table (in the wiki or internal operations file) with:
- committee name
- group email address
- current chair role mailbox (if applicable)
- current permission holders
- last membership review date
- last updated by

This makes volunteer/staff handoff much easier.

---

## Common Issues and Checks

### Issue: Person does not receive committee emails
Check:
- member exists in correct Microsoft Group
- email address is correct
- sender used the correct group address
- recent change triggered notification (confirms update happened)

### Issue: New chair cannot open role mailbox
Check:
- shared mailbox permission was granted to the person’s licensed account
- user is opening mailbox from their own account context
- predecessor access was removed (to avoid confusion)

### Issue: Missing archive history
Check:
- `itadmin@` is still a member of the affected group
- group delivery settings have not been altered

---

## Handoff Checklist (Staff/Volunteer Transition)
- [ ] Review all committee group memberships for accuracy.
- [ ] Verify all active chairs/executive roles have correct shared mailbox access.
- [ ] Remove stale permissions from former role holders.
- [ ] Confirm `itadmin@` is in every group.
- [ ] Confirm membership-change notification flow is working.
- [ ] Update inventory table and date-stamp the review.

---

## Key Contacts and Ownership
- **Group membership owner**: Anna (staff)
- **Technical owner / escalation**: IT admin
- **Archive mailbox**: `itadmin@` (not actively monitored)

If ownership changes, update this section immediately.
