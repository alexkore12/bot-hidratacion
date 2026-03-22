# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please send an email to the repository owner. All security vulnerabilities will be promptly addressed.

## Security Best Practices

- Never commit secrets or API keys to the repository
- Use environment variables for sensitive configuration
- Follow the principle of least privilege
- Keep dependencies updated and monitor for vulnerabilities
- Use secure communication protocols (HTTPS, SSH)

## Dependency Scanning

This project uses automated dependency scanning:
- npm audit / pip-audit for vulnerable packages
- Consider using tools like Snyk, Dependabot, or Trivy

## Incident Response

1. Confirm the vulnerability
2. Assess impact and severity
3. Develop and test the fix
4. Release the patch
5. Communicate to users

---

## ⚠️ CVE-2026-28500 - ONNX Supply Chain Attack

**Fecha:** Marzo 2026 | **Severidad:** HIGH (CVSS 8.6)

### Descripción
Se descubrió una vulnerabilidad crítica en la biblioteca ONNX que permite ataques a la cadena de suministro (supply chain attack).

### Vulnerabilidad
- **Vector:** `onnx.hub.load()` con parámetro `silent=True`
- **Problema:** El parámetro silent=True salta las advertencias de seguridad, permitiendo que cargas maliciosas se ejecuten sin notificación
- **Impacto:** Exfiltración de archivos sensibles (SSH keys, credenciales cloud, tokens)

### Referencias
- NVD: https://nvd.nist.gov/vuln/detail/CVE-2026-28500
- Reddit r/pwnhub: Discusión original

### Acción Recomendada
Si tu proyecto usa ONNX, verifica la versión y considera actualizar cuando hay parche disponible. Evita usar `silent=True` en producción.
