# Security policy

## Reporting a vulnerability

**Do not open a GitHub issue for security vulnerabilities.**

Please report security issues by emailing [general@61418.io](mailto:general@61418.io). Include as much of the following as you can:

- A description of the vulnerability and its potential impact
- The affected version(s)
- Steps to reproduce or a proof of concept
- Any suggested fix, if you have one

You should receive an acknowledgement within 72 hours. We will keep you informed as we investigate and, where appropriate, credit you in the release notes when a fix is published.

## Scope

Areas of particular concern for this project given its nature as a credential management tool:

- Credential exposure through the UNIX socket or log files
- Insecure socket file permissions allowing unauthorized clients to retrieve credentials
- Config file handling that could leak AWS credentials or session tokens
- Stale socket or lock file conditions exploitable for privilege escalation
- Dependency vulnerabilities in `boto3-refresh-session`, `pydantic`, or other runtime dependencies

## Supported versions

Only the latest published release receives security fixes. If you are running an older version, please upgrade before reporting.

## Disclosure policy

We follow coordinated disclosure. We ask that you give us reasonable time to investigate and release a fix before making a vulnerability public. We aim to resolve confirmed vulnerabilities within 90 days of the initial report.
