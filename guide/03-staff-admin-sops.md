# Staff and Admin SOPs

This page is for office staff, IT helpers, and trained admins who maintain
Microsoft 365 access.

## Ownership

| Responsibility | Primary | Backup / escalation |
| --- | --- | --- |
| Maintain committee group membership | Anna / office staff | IT admin |
| Manage shared mailbox permissions | Anna plus IT admin | IT admin |
| Keep `itadmin@` in all groups | IT admin | Anna / office staff |
| Monitor membership-change notifications | Anna / office staff | IT admin |
| Troubleshoot access and delivery issues | IT admin | Anna / office staff |

Update this table whenever ownership changes.

## Monthly Checklist

- Review committee membership changes from chairs.
- Confirm active officers and chairs have correct shared mailbox access.
- Remove stale permissions from former role holders.
- Confirm `itadmin@sandiahomeowners.org` remains in every group.
- Confirm Power Automate membership-change notifications are working.
- Confirm Board reminder workflow is sending as expected.
- Escalate unresolved access issues to IT.

## Add An External Volunteer

Use this for most volunteers.

1. Invite the external user with their personal email address.
2. Ask them to accept the Microsoft invitation email.
3. After acceptance, add them to needed Microsoft Groups.
4. Provide the direct committee SharePoint link.
5. Verify they receive a test group email.

## Add A Licensed User

Use this for staff or admins who need a personal Microsoft login such as
`first.last@sandiahomeowners.org`.

1. Go to [admin.microsoft.com](https://admin.microsoft.com).
2. Open **Users** > **Active users** > **Add a user**.
3. Enter name and username.
4. Generate a temporary password and require change at first sign-in.
5. Assign the correct Microsoft 365 license.
6. Add the user to needed groups and shared mailbox permissions.

## Create A Microsoft 365 Group

Use this for a committee or task-force mailing list.

1. Go to **Teams and groups** > **Active teams and groups** > **Add a group**.
2. Choose **Microsoft 365** group.
3. Enter the group name, description, and email address.
4. Set privacy to **Private** unless there is a reason to do otherwise.
5. Leave "Create a team for this group" off unless Teams is truly needed.
6. Enable external email to the group.
7. Enable copies of group email to members' inboxes.
8. Add owners and members.
9. Add `itadmin@sandiahomeowners.org`.
10. Send a test email and confirm delivery.

Done checklist:

- Group exists.
- Owners added.
- External email enabled.
- Inbox delivery enabled.
- Members added.
- `itadmin@` added.
- Test email delivered.

## Create A Shared Mailbox

Use this for a role inbox that must keep history when people rotate.

1. Go to **Teams and groups** > **Shared mailboxes** > **Add a shared mailbox**.
2. Enter the role name and address.
3. Add licensed users who should access the mailbox.
4. Grant Send As permission to the same users.
5. Ask one user to verify in Outlook that the mailbox appears, receives mail,
   and can send from the role address.

Do not create personal accounts for chairs unless they truly need their own
licensed login.

## Add An Alias

Use this for a friendly one-off address that routes to an existing group or
mailbox.

1. Decide whether the alias should route to a group or a shared mailbox.
2. Open the destination group or mailbox in the admin center.
3. Add the alias in email-address settings.
4. Save changes.
5. Send a test email to the alias and verify the destination.

## Role Transition

1. Identify the affected role mailbox.
2. Remove the outgoing person's permissions.
3. Grant the incoming person's permissions.
4. Validate that the incoming person can open the mailbox from their own account.
5. Keep the role mailbox address and history unchanged.

## Final Validation

- Group email tested.
- Shared mailbox tested, if created or changed.
- Alias tested, if created.
- `itadmin@` included in the group.
- Directory updated with any new address.
- Requester notified that setup is complete.

