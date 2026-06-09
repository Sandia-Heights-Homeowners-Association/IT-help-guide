# Controls & Security

This page documents access controls, cybersecurity practices, and data backup procedures for SHHA systems.

*Items marked **TODO** need information filled in. These questions originated from Andrea's controls review.*

## Access Controls — Who Has Access to What?

### Microsoft 365 Admin Access

<table id="bkmrk-global-administrator"><tbody><tr><td>**Global Administrator**</td><td>**TODO:** Who currently has Global Admin access? (There should be a primary and a backup.)</td></tr><tr><td>**User / Group management**</td><td>Anna (office staff) manages day-to-day membership. IT admin handles mailbox permissions.</td></tr><tr><td>**Who manages access?**</td><td>**TODO:** Is there a documented process for granting/revoking admin access? Who approves changes?</td></tr></tbody></table>

### Other System Access

<table id="bkmrk-systemprimary-access"><thead><tr><th>System</th><th>Primary Access</th><th>Backup Access</th></tr></thead><tbody><tr><td>QuickBooks</td><td>**TODO**</td><td>**TODO**</td></tr><tr><td>Membership Database</td><td>**TODO**</td><td>**TODO**</td></tr><tr><td>Gusto (Payroll)</td><td>**TODO**</td><td>**TODO**</td></tr><tr><td>SHHA Website (admin)</td><td>**TODO**</td><td>**TODO**</td></tr><tr><td>Square</td><td>**TODO**</td><td>**TODO**</td></tr><tr><td>Domain registrar</td><td>**TODO**</td><td>**TODO**</td></tr><tr><td>Google accounts</td><td>**TODO**</td><td>**TODO**</td></tr></tbody></table>

## Cybersecurity

### Current Practices

- **TODO:** Do we enforce multi-factor authentication (MFA) for Microsoft 365 admin accounts?
- **TODO:** Do we enforce MFA for all licensed users?
- **TODO:** How do we handle password policies? (complexity requirements, rotation schedule)
- **TODO:** Is there an incident response plan if an account is compromised?
- **TODO:** Do we have phishing awareness guidelines for staff and volunteers?

### Data Access

- **TODO:** How do we manage overall data access security? (e.g., conditional access policies, device restrictions)
- **TODO:** Are there any data classification policies (confidential vs. public)?
- **TODO:** How is sensitive financial data protected? (QuickBooks access, payroll data in Gusto)

## Data Backup

### Cloud-Based Systems

Most SHHA data resides in cloud services. Each provider has its own backup/redundancy:

<table id="bkmrk-systembackup-approac"><thead><tr><th>System</th><th>Backup Approach</th></tr></thead><tbody><tr><td>Microsoft 365 (email, SharePoint)</td><td>Microsoft provides built-in redundancy and retention policies. **TODO:** Do we have a separate backup solution (e.g., third-party M365 backup)? What are our retention policy settings?</td></tr><tr><td>QuickBooks Online</td><td>Intuit maintains backups. **TODO:** Do we also export periodic backups locally?</td></tr><tr><td>Gusto</td><td>Gusto maintains payroll records. **TODO:** Do we keep local copies of payroll reports?</td></tr><tr><td>SHHA Website</td><td>**TODO:** Who backs up the website? How often? Where are backups stored?</td></tr><tr><td>Membership Database</td><td>**TODO:** How is the membership database backed up?</td></tr></tbody></table>

### Local Data

- **TODO:** Is any critical data stored only on local computers (office PCs) and not in the cloud?
- **TODO:** If so, how is that data backed up?

## Other Security Considerations

- **TODO:** Do we have cyber liability insurance?
- **TODO:** When was the last security review or audit of our systems?
- **TODO:** Are there any compliance requirements (e.g., state HOA data retention laws)?
