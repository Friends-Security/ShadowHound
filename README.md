![Logo](./logo.png)

# ShadowHound

ShadowHound is a set of PowerShell scripts for Active Directory enumeration without the need for introducing known-malicious binaries like SharpHound. It leverages native PowerShell capabilities to minimize detection risks and offers two methods for data collection:

- **ShadowHound-ADM.ps1**: Uses the Active Directory module (ADWS).
- **ShadowHound-DS.ps1**: Utilizes direct LDAP queries via `DirectorySearcher`.

## Blog Post

For more details and context, check out the [blog post](https://blog.fndsec.net/2024/11/25/shadowhound/).

## Scripts Overview

### ShadowHound-ADM.ps1

- **Method**: Active Directory module (`Get-ADObject` via ADWS).
- **Usage Scenario**: When the AD module is available and ADWS is accessible.
- **Features**:
  - Handles large domains with `-SplitSearch`, `-Recurse`, and `-LetterSplitSearch` options.
  - Enumerates certificates with the `-Certificates` flag.

### ShadowHound-DS.ps1

- **Method**: Direct LDAP queries using `DirectorySearcher`.
- **Usage Scenario**: Environments where the AD module isn't available or LDAP is preferred.
- **Features**:
  - Enumerates certificates with the `-Certificates` flag.
  - Supports alternate credentials with the `-Credential` parameter.

## Usage Examples

### Basic Enumeration

#### ShadowHound-ADM.ps1

```powershell
# Basic usage
ShadowHound-ADM -OutputFilePath "C:\Results\ldap_output.txt"

# Specify a domain controller and custom LDAP filter
ShadowHound-ADM -Server "dc.domain.local" -OutputFilePath "C:\Results\ldap_output.txt" -LdapFilter "(objectClass=user)"

# Use alternate credentials
$cred = Get-Credential
ShadowHound-ADM -OutputFilePath "C:\Results\ldap_output.txt" -Credential $cred -SearchBase "DC=domain,DC=local"
```

#### ShadowHound-DS.ps1

```powershell
# Basic usage
ShadowHound-DS -OutputFile "C:\Results\ldap_output.txt"

# Specify a domain controller
ShadowHound-DS -Server "dc.domain.local" -OutputFile "C:\Results\ldap_output.txt"

# Use a custom LDAP filter
ShadowHound-DS -OutputFile "C:\Results\ldap_output.txt" -LdapFilter "(objectClass=computer)"
```

### Enumerating Certificates

Both scripts support enumerating certificate-related objects for those juicy ADCS vectors:

```powershell
# Using ShadowHound-ADM.ps1
ShadowHound-ADM -OutputFilePath "C:\Results\cert_output.txt" -Certificates

# Using ShadowHound-DS.ps1
ShadowHound-DS -OutputFile "C:\Results\cert_output.txt" -Certificates
```

### Handling Large Domains (ShadowHound-ADM.ps1)

```powershell
# Split search across top-level containers with letter splitting
ShadowHound-ADM -OutputFilePath "C:\Results\ldap_output.txt" -SplitSearch -LetterSplitSearch
```

- **`-SplitSearch`**: Splits the search across top-level containers.
- **`-Recurse`**: Recurses into containers that fail to return results.
- **`-LetterSplitSearch`**: Further splits searches by the first letter of CN.

## Converting Data for BloodHound

After collecting data, use [BofHound](https://github.com/coffeegist/bofhound) to convert it into BloodHound-compatible JSON files:

```bash
python3 bofhound.py -i ldap_output.txt -p All --parser ldapsearch
```

For large JSON files (>100MB), consider splitting them with tools like [ShredHound](https://github.com/ustayready/ShredHound).

## Author

- **Yehuda Smirnov**
  - Twitter: [@yudasm_](https://twitter.com/yudasm_)
  - BlueSky: [@yudasm.bsky.social](https://bsky.app/profile/yudasm.bsky.social)
