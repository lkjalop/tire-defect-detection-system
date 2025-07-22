# 🔐 Threat Model – Tire Defect Detection System

This document outlines a comprehensive security and threat model for the `tire-defect-detection-system` project, integrating principles from OWASP Top 10 for APIs and known AI/ML-specific attack vectors. The goal is to demonstrate that this AI Edge/IoT system has been designed with an awareness of realistic security risks and mitigations.

---

## 🔍 1. Security Scope

- **System:** Tire Defect Detection using YOLOv8
- **Architecture:** Edge AI system with FastAPI backend
- **Deployment:** Containerized (Docker), designed for local + cloud-ready infrastructure

---

## ⚠️ 2. AI-Specific Threat Vectors

### 🧠 2.1 Prompt Injection
- **Risk:** If AI models (e.g., LLMs) are later integrated, prompt injection could allow attackers to manipulate model behavior.
- **Mitigation:** Input sanitization and use of predefined prompts/templates for critical operations.

### 📷 2.2 Input-Based Attacks (CV Payloads)
- **Risk:** Malicious camera input (crafted ASCII/image noise) could trigger model misbehavior or system compromise.
- **Mitigation:** Validate and preprocess images. Sanitize data at ingestion. Use fail-safes for invalid input.

### 📤 2.3 Output Manipulation & Hallucination
- **Risk:** AI model produces unexpected or unsafe output.
- **Mitigation:** Implement output confidence thresholds and logging. Validate results against known defect criteria.

### 📊 2.4 Model Drift
- **Risk:** Over time, model behavior drifts from expected output, increasing false negatives/positives.
- **Mitigation:** Monitor performance and implement retraining cycles using updated datasets.

---

## 🧱 3. OWASP API Security Top 10 Mapping

### 🔐 3.1 Broken Object Level Authorization
- **Risk:** APIs expose endpoints without validating user-level permissions.
- **Mitigation:** Implement RBAC (Role-Based Access Control) and auth tokens.

### 🔑 3.2 Broken Authentication
- **Risk:** Weak or absent auth allows unauthorized access.
- **Mitigation:** Use FastAPI OAuth2/JWT-based authentication. Enforce token expiration and refresh cycles.

### 📦 3.3 Excessive Data Exposure
- **Risk:** API returns internal model metadata or debug info.
- **Mitigation:** Limit response fields. Strip internal logs or headers in production.

### 🔄 3.4 Lack of Rate Limiting
- **Risk:** Brute-force or inference probing attacks.
- **Mitigation:** Apply middleware rate limiting. Monitor for abuse patterns.

### ⚙️ 3.5 Security Misconfiguration
- **Risk:** Docker containers, debug mode, or CORS exposed.
- **Mitigation:** Harden Docker, disable debug mode, restrict CORS origins.

### 🛠️ 3.6 Injection (SQL, OS, etc.)
- **Risk:** Query or command injection via FastAPI parameters.
- **Mitigation:** Use Pydantic models for strict type validation. Sanitize all user input.

### 📜 3.7 Improper Asset Management
- **Risk:** Exposing deprecated or unprotected endpoints.
- **Mitigation:** Maintain up-to-date API documentation. Use OpenAPI schema enforcement.

---

## 📊 4. Logging, Monitoring & Audit

- Use structured logging (e.g., loguru, Python `logging`)
- Track all authentication and defect analysis activity
- Log unusual or rejected requests (rate limit, auth failures)

---

## 🧪 5. Compliance Considerations

- Foundation for compliance with:
  - **SOC 2**: Logging, access control, change management
  - **NIST**: Principle of least privilege, secure defaults
- Future addition: Endpoint behavior validation, encrypted ML models at rest

---

## ✅ 6. Summary

This threat model illustrates a **security-conscious approach** to Edge AI system development. While this is a simulated project, all security controls were selected to reflect **enterprise-grade practices** aligned with real-world expectations.

---

**Author:** Leomark Kevin Jalop  
**Reviewers:** [AI Security Expert Placeholder]
