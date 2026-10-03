# CareerLens AI — REST API Overview

## Overview

CareerLens AI provides a versioned REST API implemented using FastAPI.

The primary API prefix is:

```text
/api/v1
```

The API supports:

- Authentication
- Email verification
- Password recovery
- Resume management
- Job-description management
- Resume/job analysis
- PDF reports
- Administrative authorization

The complete backend implementation remains private. This document describes the public API structure.

---

# Authentication API

## Register

```http
POST /api/v1/auth/register
```

Creates a new CareerLens user account.

The registration workflow creates the user and begins the email-verification process.

---

## Verify Email

```http
POST /api/v1/auth/verify-email
```

Completes email verification using the application's verification flow.

---

## Resend Verification

```http
POST /api/v1/auth/resend-verification
```

Requests another email-verification flow.

---

## Forgot Password

```http
POST /api/v1/auth/forgot-password
```

Starts the password-recovery process.

---

## Reset Password

```http
POST /api/v1/auth/reset-password
```

Completes a password reset using a valid reset flow.

---

## Login

```http
POST /api/v1/auth/login
```

Authenticates a user.

After successful authentication, the application issues the tokens required for the authenticated session.

---

## Refresh Authentication

```http
POST /api/v1/auth/refresh
```

Uses a valid refresh token to obtain a renewed authentication session.

CareerLens implements refresh-token rotation as part of the authentication lifecycle.

---

## Logout

```http
POST /api/v1/auth/logout
```

Revokes the supplied refresh token.

---

## Current User

```http
GET /api/v1/auth/me
```

Returns information about the currently authenticated user.

This is a protected endpoint.

---

# Resume API

## Upload Resume

```http
POST /api/v1/resumes/upload
```

Uploads a resume belonging to the authenticated user.

Supported document types include:

```text
PDF
DOCX
```

Resume text is extracted by the backend for later analysis.

---

## List Resumes

```http
GET /api/v1/resumes
```

Returns resumes belonging to the authenticated user.

---

## Get Resume

```http
GET /api/v1/resumes/{resume_id}
```

Returns one resume owned by the authenticated user.

Ownership validation prevents access to another user's resume.

---

## Delete Resume

```http
DELETE /api/v1/resumes/{resume_id}
```

Deletes an owned resume.

---

# Job Description API

## Create Job Description

```http
POST /api/v1/job-descriptions
```

Creates a job description for the authenticated user.

A job description contains information such as:

```text
Job Title
Company Name
Description
```

---

## List Job Descriptions

```http
GET /api/v1/job-descriptions
```

Returns job descriptions belonging to the authenticated user.

---

## Get Job Description

```http
GET /api/v1/job-descriptions/{job_description_id}
```

Returns a specific job description owned by the authenticated user.

---

## Delete Job Description

```http
DELETE /api/v1/job-descriptions/{job_description_id}
```

Deletes an owned job description.

---

# Analysis API

## Create Analysis

```http
POST /api/v1/analyses
```

Creates a resume-to-job-description analysis.

The analysis uses a selected resume and job description.

Generated information includes:

```text
Overall Match Score
Skills Score
Experience Score
Education Score
ATS Score

Matched Skills
Missing Skills
Recommended Skills
ATS Keywords

Experience Match
Education Match
Recommendations
```

---

## List Analyses

```http
GET /api/v1/analyses
```

Returns analysis history belonging to the authenticated user.

---

## Get Analysis

```http
GET /api/v1/analyses/{analysis_id}
```

Returns a specific owned analysis.

---

## Download Analysis Report

```http
GET /api/v1/analyses/{analysis_id}/report
```

Generates and returns a PDF report for the selected analysis.

The report is produced by the backend using ReportLab.

---

## Delete Analysis

```http
DELETE /api/v1/analyses/{analysis_id}
```

Deletes an owned analysis.

---

# Administration API

CareerLens includes role-based administrative protection.

Example endpoint:

```http
GET /api/v1/admin/test
```

This endpoint requires:

```text
ADMIN
```

authorization.

---

# API Summary

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/auth/register` | Register user |
| POST | `/api/v1/auth/verify-email` | Verify email |
| POST | `/api/v1/auth/resend-verification` | Resend verification |
| POST | `/api/v1/auth/forgot-password` | Start password reset |
| POST | `/api/v1/auth/reset-password` | Reset password |
| POST | `/api/v1/auth/login` | Login |
| POST | `/api/v1/auth/refresh` | Refresh authentication |
| POST | `/api/v1/auth/logout` | Logout/revoke refresh token |
| GET | `/api/v1/auth/me` | Current user |
| POST | `/api/v1/resumes/upload` | Upload resume |
| GET | `/api/v1/resumes` | List resumes |
| GET | `/api/v1/resumes/{resume_id}` | Resume details |
| DELETE | `/api/v1/resumes/{resume_id}` | Delete resume |
| POST | `/api/v1/job-descriptions` | Create job description |
| GET | `/api/v1/job-descriptions` | List job descriptions |
| GET | `/api/v1/job-descriptions/{job_description_id}` | Job-description details |
| DELETE | `/api/v1/job-descriptions/{job_description_id}` | Delete job description |
| POST | `/api/v1/analyses` | Create analysis |
| GET | `/api/v1/analyses` | Analysis history |
| GET | `/api/v1/analyses/{analysis_id}` | Analysis details |
| GET | `/api/v1/analyses/{analysis_id}/report` | PDF report |
| DELETE | `/api/v1/analyses/{analysis_id}` | Delete analysis |
| GET | `/api/v1/admin/test` | ADMIN-protected endpoint |

---

# Authentication Model

Protected API calls use JWT authentication.

```text
User
  ↓
Login
  ↓
Access Token + Refresh Token
  ↓
Access Protected Endpoint
  ↓
Access Token Expires
  ↓
Refresh
  ↓
Renewed Authentication
```

Protected requests use an access token through the authorization mechanism.

Conceptually:

```http
Authorization: Bearer <access-token>
```

Actual secrets or tokens are never included in this public repository.

---

# Authorization Model

CareerLens applies multiple authorization layers.

```text
Request
   ↓
Authentication
   ↓
Role Validation
   ↓
Ownership Validation
   ↓
Resource Access
```

Users can access only their own:

- Resumes
- Job descriptions
- Analyses

Administrative endpoints require the appropriate role.

---

# Analysis Response Concept

A CareerLens analysis contains both scores and explainable results.

Example structure:

```json
{
  "match_score": 78.5,
  "skills_score": 82.0,
  "experience_score": 75.0,
  "education_score": 80.0,
  "ats_score": 70.0,
  "matched_skills": "...",
  "missing_skills": "...",
  "recommended_skills": "...",
  "ats_keywords": "...",
  "experience_match": "...",
  "education_match": "...",
  "recommendations": "..."
}
```

The example illustrates the type of analysis information returned. It is not intended to represent a specific user's stored result.

---

# Error Handling

The API provides structured handling for scenarios such as:

```text
Invalid Request
Authentication Failure
Authorization Failure
Resource Not Found
Validation Error
Unexpected Server Error
```

The frontend API layer additionally handles:

- Access-token expiration
- Token refresh
- Request timeout
- Authentication retry behavior
- User-facing error messages

---

# User Isolation

Ownership is enforced for user-specific resources.

For example:

```text
User A
 ├── Resume A
 ├── Job Description A
 └── Analysis A

User B
 ├── Resume B
 ├── Job Description B
 └── Analysis B
```

User A cannot retrieve or modify User B's owned resources through the protected application API.

---

# API Design Principles

CareerLens demonstrates:

- RESTful resource design
- Versioned APIs
- Authentication
- Authorization
- Role-based access
- Ownership validation
- Request validation
- File uploads
- Document processing
- Relational persistence
- PDF responses
- Centralized error handling
- Separation between API and business logic

---

# Security

API security considerations include:

- Password hashing
- JWT authentication
- Token expiration
- Refresh-token rotation
- Refresh-token revocation
- Token hashes stored in the database
- Role checks
- Ownership checks
- Input validation
- Environment-managed secrets
- Controlled CORS configuration

Production secrets are not stored in the public repository.

---

# Interactive API Documentation

FastAPI provides automatic API documentation when enabled in the running environment.

During local development, the backend can expose interactive documentation for testing and exploring API contracts.

Production exposure of API documentation can be configured according to deployment requirements.