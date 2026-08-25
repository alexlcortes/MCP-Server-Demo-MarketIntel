# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please **do not** open a public GitHub issue. Instead, please email the maintainers with details about the vulnerability.

### What to include in your report:
- A clear description of the vulnerability
- Steps to reproduce or proof of concept
- Affected versions
- Potential impact

## Security Best Practices

### Using MarketIntel MCP Server

1. **API Key Management**
   - Never commit `.env` files or API keys to version control
   - Use environment variables for sensitive configuration
   - Rotate API keys regularly
   - Restrict API key permissions to minimum required scope

2. **Dependency Management**
   - Keep dependencies updated regularly
   - Review `uv.lock` and `pyproject.toml` for known vulnerabilities
   - Use `pip-audit` or similar tools to scan dependencies:
     ```bash
     pip-audit
     ```

3. **Data Privacy**
   - Be mindful when researching sensitive company information
   - Ensure compliance with applicable data protection regulations
   - Do not store confidential information in logs or outputs

## Supported Versions

Only the latest version receives security updates. Users are encouraged to upgrade promptly.

## Security Updates

Security updates will be released as patch versions and tagged appropriately in git.
