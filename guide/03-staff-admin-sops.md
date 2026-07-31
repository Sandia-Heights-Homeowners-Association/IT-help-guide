# Staff and Admin SOPs

This page is for office staff and IT administrators who maintain Microsoft 365
access.

## Ownership

| Responsibility | Primary | Backup / next action |
| --- | --- | --- |
| Maintain committee group membership | Anna / office staff | IT admin |
| Manage shared mailbox permissions | Anna plus IT admin | IT admin |
| Keep `admin@` in all groups | IT admin | Anna / office staff |
| Monitor membership-change notifications | Anna / office staff | IT admin |
| Troubleshoot access and delivery issues | IT admin | Anna / office staff |

Update this table whenever ownership changes.

## Monthly Checklist

- Review committee membership changes from chairs.
- Confirm the six active officer roles have correct shared mailbox access.
- Remove stale permissions from former role holders.
- Confirm `admin@sandiahomeowners.org` remains in every group.
- Confirm Power Automate membership-change notifications are working.
- Confirm Board reminder workflow is sending as expected.
- Record unresolved access issues with the account, group or site, exact error,
  and last successful test. Then check the relevant Microsoft 365 setting before
  handing the issue to the next person listed in the ownership table.

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
6. Finish creating the group.
7. Open the new group and go to its **Settings** pane. You **must** check both of these settings:
   - **Let people outside the organization email this team**.
   - **Send copies of team emails and events to team members' inboxes**.
8. Add owners and members.
9. Add `admin@sandiahomeowners.org`.
10. Test the group before announcing it. Send a test email and confirm delivery to the intended members.

After any later change to the group, test again. For a quick check, add yourself
temporarily as a member, send a test message, and remove yourself when finished.
If external delivery matters, you can also add a personal Gmail account
temporarily, test it, and remove it afterward.

Done checklist:

- Group exists.
- Owners added.
- External email enabled.
- Inbox delivery enabled.
- Members added.
- `admin@` added.
- Test email delivered after setup and after any later change.

## Setup Decision Flow

Use this quick decision path before creating anything:

| Question | Yes | No |
| --- | --- | --- |
| Does a committee or task force need one address that emails its members? | Create a Microsoft 365 Group using **SOP A**. | Continue. |
| Is the role one of the six officers: President, Vice President, Secretary, Treasurer, ACC Chair, or CSC Chair? | Create the role mailbox using **SOP B**, then send the [Officer Shared Mailbox Access](https://wiki.sandiahomeowners.org/books/shha-it-help-guide/page/office-onboarding-email-templates) email. | Do **not** create a shared mailbox. Use the person's own account and the committee mailing list. |
| Does the committee need a document library? | Follow [SOP: Create a Committee SharePoint Site](https://wiki.sandiahomeowners.org/books/shha-it-help-guide/page/sop-create-a-committee-sharepoint-site), then use the matching [Office Onboarding Email Template](https://wiki.sandiahomeowners.org/books/shha-it-help-guide/page/office-onboarding-email-templates). | Finish the email setup and test it. |

## Create A Shared Mailbox

Use this **only** for the six officer roles listed in the decision flow. Shared
mailboxes are a little fussy to administer, but officer history is important
enough that SHHA keeps it this way.

1. Confirm the mailbox is for President, Vice President, Secretary, Treasurer,
   ACC Chair, or CSC Chair. For any other chair or task-force lead, use the
   committee mailing-list procedure instead.
2. Go to **Teams and groups** > **Shared mailboxes** > **Add a shared mailbox**.
3. Create the role address, such as `president@sandiahomeowners.org`.
4. Add the incoming officer's licensed `@sandiahomeowners.org` account.
5. Grant that account both **Full Access** and **Send As**.
6. Send [Officer Shared Mailbox Access](https://wiki.sandiahomeowners.org/books/shha-it-help-guide/page/office-onboarding-email-templates) with the direct role address and [wiki link](https://wiki.sandiahomeowners.org/books/shha-it-help-guide/page/volunteer-with-shha-email).
7. Have the officer sign in to Outlook with their own account and add the
   shared mailbox manually. It will not appear automatically in every Outlook
   setup.
8. Test all three things: the officer can open the mailbox, can read an
   incoming test message, and can send with the role address in **From**.
9. Tell the officer to send official role correspondence from the role mailbox
   or copy the role mailbox. The shared mailbox is the role's archive; a
   personal inbox is not.

Do not create a shared mailbox for an ordinary committee chair, task-force lead,
or external volunteer. They use their own account and the committee mailing
list.

For Microsoft's current Outlook instructions, see [Open and use a shared
mailbox in Outlook](https://support.microsoft.com/en-us/outlook/sharing/open-and-use-a-shared-mailbox-in-outlook).

## Create A Committee SharePoint Site

Use the BookStack page **SOP: Create a Committee SharePoint Site** for the full
walkthrough. The standard setup is:

1. Find the SharePoint site already connected to the existing Microsoft 365
   group. Do not create a duplicate site or group.
2. Keep office staff as Owners / Full Control.
3. Change the site's Members group from **Edit** to **Contribute** so committee
   members can work with documents without editing the home page.
4. Use the existing **Documents** library; do not create a second one.
5. Create **Documents Shared with Board**.
6. Keep the home page and navigation limited to the useful basics.
7. Add OneDrive shortcuts only for internal office accounts.
8. Test document access with a real external member using SharePoint in a
   browser.
9. Send members the general **Committee SharePoint Guide**.

External committee members should never use OneDrive for committee documents.

## Send The Welcome Email

After setup and testing are complete, use the BookStack page **Office
Onboarding Email Templates**. These are copy-and-send messages from Office or IT
Help to the newly onboarded users:

1. New internal licensed staff user.
2. New external volunteer using a personal email address.
3. Members of a newly formed committee or task force.
4. Members of an existing committee receiving a SharePoint site later.
5. An incoming officer receiving access to a shared role mailbox.

Replace every bracketed placeholder, include the direct SharePoint and wiki
links, and test the links before sending. Never send external users OneDrive
instructions.

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
- Shared mailbox tested, if an officer mailbox was created or changed.
- Alias tested, if created.
- `admin@` included in the group.
- Directory updated with any new address.
- Office contact told setup is complete.
