# SOP: Create a Committee SharePoint Site

**Audience:** SHHA office staff and IT administrators. This is not a committee-member task.

**Goal:** connect an existing committee Microsoft 365 group to its group-owned SharePoint document library, keep site-page administration with office staff, and give committee members read/write access to documents.

## Before You Start

Write down these values before opening Microsoft 365:

<table id="bkmrk-committee-namethe-fu"><tbody><tr><td>**Committee name**</td><td>The full display name</td></tr><tr><td>**Microsoft 365 group**</td><td>The existing group/mailing-list name</td></tr><tr><td>**Group email**</td><td>The committee mailing-list address</td></tr><tr><td>**Expected site address**</td><td>`https://shha.sharepoint.com/sites/[GROUP-NAME]`</td></tr><tr><td>**Office owners**</td><td>Primary and backup office/admin accounts</td></tr></tbody></table>

The finished site should be **Private**. Office staff are Owners / Full Control. Committee members have **Contribute** access to documents and do not administer the home page.

## Step 1: Find The Existing Group-Connected Site

A Microsoft 365 group normally provisions a connected SharePoint team site. If the mailing list already exists, **do not begin by creating another site or group**.

1. Try `https://shha.sharepoint.com/sites/[GROUP-NAME]`.
2. If that does not open, go to [admin.microsoft.com](https://admin.microsoft.com) → **Show all** → **Admin centers** → **SharePoint**.
3. Open **Sites** → **Active sites**.
4. Search for both the committee's full name and group name.
5. In the Microsoft 365 admin center, open **Teams &amp; groups** → **Active teams &amp; groups**, select the group, and confirm its type is **Microsoft 365**.

If the group-connected site appears in Active sites, open it and continue.

**If the Microsoft 365 group exists but no connected site can be found:** do not create a similarly named standalone site. Recheck that the group is a **Microsoft 365** group and search the SharePoint admin center's **Active sites** by both the group name and the full committee name. If the site is still not listed, record the group name and leave site setup pending until Microsoft finishes provisioning it. A duplicate would separate mailing-list membership from document access.

## Step 2: Confirm Office Staff Are Owners

1. In the SharePoint admin center, open **Sites** → **Active sites**.
2. Select the committee site.
3. Select **Membership**.
4. Confirm the primary and backup office/admin accounts are Owners or site admins.
5. Add a backup office/admin owner if needed.
6. Do not make the committee chair or ordinary committee members Owners.

Owners may edit the home page, navigation, permissions, and site settings. Keep that role with office staff.

## Step 3: Give Members Document Access Without Site Editing

Microsoft normally gives group-connected team-site members **Edit** permission. SHHA uses **Contribute** so members can work with documents without managing lists or editing the site page.

1. Open the committee SharePoint site.
2. Select **Settings** → **Site permissions**.
3. Select **Advanced permissions settings**.
4. Select the SharePoint group whose name ends in **Members**. Do not select Owners or Visitors.
5. Select **Edit User Permissions**.
6. Clear **Edit**.
7. Select **Contribute**.
8. Select **OK**.

Do not remove the committee Microsoft 365 group from the site. Group membership keeps the mailing list and document access synchronized.

## Step 4: Keep The Site Simple

A team site already includes a default **Documents** library. Do not create a second Documents library.

1. Open **Documents** and confirm it works.
2. Create a folder named **Documents Shared with Board**.
3. If folder colors are available, apply the standard SHHA committee-folder color.
4. Edit the left navigation and remove unused links. Keep the useful experience limited to **Home** and **Documents**.
5. Do not delete the system **Site Pages** library; it supports the home page.

## Step 5: Make The Home Page Minimal

Only office staff should edit the home page.

1. From the home page, select **Edit**.
2. Use the committee's full name as the title.
3. Add: “Use the Documents library for committee files and enduring reference materials.”
4. Add or keep an obvious link to **Documents**.
5. Remove unnecessary news, activity, and decorative web parts.
6. Republish the page.

## Step 6: Add The Library To Office OneDrive

**This is only for internal office users with SHHA Microsoft accounts.** External users should never use OneDrive for committee documents; they use SharePoint in their browser.

1. Sign in as the office user who needs the shortcut.
2. Open the committee SharePoint site and then **Documents**.
3. Select **Add shortcut to OneDrive** or **Add shortcut to My files**.
4. Open that user's OneDrive and confirm the committee folder appears under **My files**.
5. If the desktop OneDrive app is used, confirm the shortcut appears on that computer.
6. Repeat while signed in as each internal office user who needs the shortcut.

The shortcut points to the group-owned SharePoint library. It does not copy files into a personal OneDrive.

## Step 7: Test With An External Member

1. Ask one existing external group member to open the committee SharePoint site using the same personal email address that received the Microsoft invitation.
2. Confirm the member can open **Documents**.
3. Have the member upload a temporary file named **TEST - delete me**.
4. Confirm the member can edit, rename, move, and delete the test file.
5. Confirm the member cannot edit the home page, navigation, permissions, or membership.
6. Confirm someone outside the group cannot open the private site.
7. Remind the external tester to bookmark the SharePoint site and not use OneDrive.

## Step 8: Publish The Member Instructions

1. Send members the [Committee SharePoint Guide](/books/shha-it-help-guide/page/committee-sharepoint-guide).
2. Add the committee mailing list and SharePoint URL to [Quick Links &amp; Directory](/books/shha-it-help-guide/page/quick-links-directory).
3. Tell external members to bookmark the SharePoint site. Do not give them OneDrive instructions.
4. Send the matching [New Committee Or Task Force](/books/shha-it-help-guide/page/office-onboarding-email-templates) or [New SharePoint Site For An Existing Committee](/books/shha-it-help-guide/page/office-onboarding-email-templates) email.

## Final Checklist

- Existing group-connected site found; no duplicate created
- Site is Private
- Office staff are Owners / Full Control
- Committee members use Contribute permissions
- Documents library works
- Documents Shared with Board folder created
- Home page and navigation simplified
- Office-user OneDrive shortcuts added separately
- External member document test passed through SharePoint
- External member cannot edit the site page
- Directory updated
- General member guide sent
- Matching onboarding email sent

## Microsoft References

- [Create a team site in SharePoint](https://support.microsoft.com/en-US/SharePoint/sites-in-sharepoint/create-a-team-site-in-sharepoint)
- [Manage sites in the SharePoint admin center](https://learn.microsoft.com/en-us/sharepoint/manage-sites-in-new-admin-center)
- [Permission levels in SharePoint](https://learn.microsoft.com/en-us/sharepoint/understanding-permission-levels)
- [Add shortcuts to shared folders in OneDrive](https://support.microsoft.com/en-US/onedrive/add-shortcuts-to-shared-folders-in-onedrive)
