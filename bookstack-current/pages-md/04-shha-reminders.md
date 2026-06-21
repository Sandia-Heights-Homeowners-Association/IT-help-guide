# SHHA Reminders

SHHA Reminders is the Sandia Heights Homeowners Association tool for sending automated reminder emails for meetings and events.

The app does **not** replace Outlook, Teams, or Google Calendar. Office staff should keep creating and editing meetings in the existing calendar system. SHHA Reminders reads events from the Microsoft 365 calendar for `admin@sandiahomeowners.org`, then uses its own reminder rules, recipient groups, and email templates to send the right nudge at the right time.

Production URL: [https://reminders.sandiahomeowners.org](https://reminders.sandiahomeowners.org)

## Who Can Log In

Any valid Microsoft account ending in `@sandiahomeowners.org` can log in.

The app uses Microsoft sign-in. There is no shared app password, which is good because shared app passwords tend to become office folklore with a login prompt attached.

## What Calendar Events Appear

SHHA Reminders reads events from the calendar for `admin@sandiahomeowners.org`.

To make a meeting appear in SHHA Reminders:

1. Create or edit the meeting in Outlook or Teams.
2. Invite `admin@sandiahomeowners.org` to the event.
3. Open SHHA Reminders.
4. Click **Sync Calendar**.

If the meeting is not on the `admin@sandiahomeowners.org` calendar, it will not appear in SHHA Reminders.

## What The App Does

SHHA Reminders lets staff:

- View upcoming synced calendar events.
- Attach reminder rules to individual events.
- Attach reminder rules to recurring meeting series.
- Manage recipient groups.
- Manage email templates.
- Send test emails for templates.
- View upcoming scheduled reminders.
- View logs as sending automation is expanded.

## Basic Workflow

1. Confirm the meeting exists in Outlook or Teams.
2. Confirm `admin@sandiahomeowners.org` is invited.
3. Open [SHHA Reminders](https://reminders.sandiahomeowners.org).
4. Click **Sync Calendar**.
5. Open **Set Up Reminders**.
6. Select the event.
7. Choose whether the rule applies to **All Future** occurrences or **This Event** only.
8. Choose when to send the reminder, such as 7 days before or 1 day before.
9. Choose the recipient group and email template.
10. Click **Add Reminder Rule**.
11. Use **Send Test** before relying on a new or edited template.

Recurring events, such as regular Board meetings, can have rules that apply to all future occurrences. Ad-hoc meetings can have one-time reminder rules.

## Recipient Groups

Use **Recipient Group** to manage lists of email recipients, such as Board, committee members, office staff, or CPC members.

Reminder rules send to recipient groups, not to one-off typed addresses. This keeps the reminder rule tidy when people rotate on or off a committee.

## Templates

Use **Templates** to manage the text of reminder emails.

Templates support variables, including:

```text
{{event.subject}}
{{event.date}}
{{event.time}}
{{event.location}}
{{event.joinUrl}}
```

Those variables are replaced with details from the selected calendar event when the email is sent.

Example:

```text
Hello,

This is a reminder that {{event.subject}} is scheduled for {{event.date}} at {{event.time}}.

{{event.location}}
{{event.joinUrl}}

Thank you,
SHHA
```

## Teams Meeting Links

Teams links are available through `{{event.joinUrl}}`.

The link comes from the Microsoft calendar event. If a Teams link is missing from a reminder, check the original Outlook or Teams event first.

## CPC And Irregular Meetings

For irregular meetings such as CPC meetings, the recommended workflow is:

1. Manually create the event in Outlook or Teams.
2. Invite `admin@sandiahomeowners.org`.
3. Sync SHHA Reminders.
4. Use a reminder rule for the matching event or meeting title.

The Microsoft calendar remains the source of truth.

## Important Operating Rules

- Do not create events directly in SHHA Reminders.
- Change meeting dates, cancellations, titles, and Teams links in Outlook or Teams.
- After changing calendar events, click **Sync Calendar** in SHHA Reminders.
- Use **Send Test** before relying on a new or edited template.
- Keep recipient groups up to date.

## Troubleshooting

### Event Does Not Appear

Check:

- Was `admin@sandiahomeowners.org` invited?
- Has the app been synced?
- Is the event within the configured sync window?
- Is the event on the Microsoft calendar, not only Google Calendar?

### Reminder Email Looks Wrong

Check:

- The selected template.
- The calendar event title, date, location, and Teams link.
- The recipient group.
- Send a test email.

### User Cannot Log In

Check:

- The user has a Microsoft account ending in `@sandiahomeowners.org`.
- The site is being accessed through HTTPS: [https://reminders.sandiahomeowners.org](https://reminders.sandiahomeowners.org).

### Emails Are Not Sending

Ask IT to check Microsoft Graph mail permissions, the `admin@sandiahomeowners.org` sending mailbox, and whether the Microsoft Entra client secret has expired.

## Ownership

Office staff own:

- Calendar event creation and edits.
- Reminder rules.
- Recipient groups.
- Email templates.
- Test sends.

IT owns:

- Hosting.
- Microsoft Entra app registration.
- Graph permissions.
- Docker deployment.
- Backups.
- Secrets and environment configuration.
- Caddy/reverse proxy configuration.
