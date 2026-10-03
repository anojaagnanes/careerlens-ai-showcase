# CareerLens AI — Architecture

## Overview

CareerLens AI is an AI-assisted resume and job-description analysis platform built as a production-style full-stack application.

The system uses:

- Next.js and React for the frontend
- TypeScript for frontend development
- FastAPI for backend REST APIs
- SQLAlchemy for persistence
- MySQL 8 for relational data
- Redis as supporting infrastructure
- Docker and Docker Compose for containerization
- GitHub Actions for continuous integration

The application follows a **modular monolith architecture**. This provides separation between major application responsibilities without introducing unnecessary distributed-system complexity.

The complete implementation is maintained in a private repository. This document provides a public architectural overview.

---

# High-Level Architecture

```text
                    ┌─────────────────────┐
                    │        User         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Next.js / React UI  │
                    │     TypeScript      │
                    └──────────┬──────────┘
                               │
                         REST API / JWT
                               │
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌──────────┐    ┌─────────────┐   ┌──────────┐
        │  MySQL   │    │  Document   │   │  Redis   │
        │ Database │    │ Processing  │   │ Service  │
        └──────────┘    └─────────────┘   └──────────┘
```

---

# Frontend Architecture

The frontend is implemented using:

- Next.js 16
- React
- TypeScript
- Tailwind CSS

Major frontend areas include:

```text
Landing Page
Authentication
Dashboard
Resume Management
Job Description Management
Analysis
Analysis Results
Profile
Administration
```

The frontend communicates with the FastAPI backend using REST APIs.

Protected requests use JWT authentication.

---

# Backend Architecture

The backend is implemented using FastAPI.

Major responsibilities include:

```text
Authentication
Authorization
Resume Management
Job Description Management
Analysis
PDF Reporting
Administration
Database Access
Validation
Error Handling
```

The backend follows a layered and modular structure so that API routing, persistence, validation, security, and business logic remain separated.

---

# Authentication Architecture

CareerLens AI implements a complete authentication lifecycle.

```text
Register
   ↓
Verify Email
   ↓
Login
   ↓
Access Token + Refresh Token
   ↓
Protected API
   ↓
Access Token Expires
   ↓
Refresh Token
   ↓
New Authentication Session
```

Security mechanisms include:

- Secure password hashing
- JWT authentication
- Access tokens
- Refresh tokens
- Refresh-token rotation
- Refresh-token revocation
- USER and ADMIN roles
- Protected endpoints
- User ownership validation

---

# Resume Processing

CareerLens AI accepts PDF and DOCX resumes.

```text
Upload Resume
      ↓
Validate File
      ↓
Store Resume
      ↓
Extract Text
      ↓
Store Metadata
      ↓
Resume Available for Analysis
```

Document processing uses:

- PyMuPDF for PDF documents
- python-docx for DOCX documents

The extracted text becomes available to the analysis process.

---

# Job Description Processing

Users can create and maintain job descriptions.

Each job description contains information such as:

```text
Title
Company
Description
Owner
Creation Time
```

The saved description can then be selected together with a resume for analysis.

---

# Analysis Architecture

The analysis workflow compares resume information against job-description requirements.

```text
Resume
   +
Job Description
   ↓
Text Processing
   ↓
Requirement Comparison
   ↓
Component Scores
   ↓
Overall Score
   ↓
Explainable Results
   ↓
Recommendations
```

CareerLens generates:

- Skills score
- Experience score
- Education score
- ATS score
- Overall score
- Matched skills
- Missing skills
- Recommended skills
- ATS keywords
- Experience explanation
- Education explanation
- Resume recommendations

The analysis is designed to derive information from the selected resume and job description rather than relying on profession-specific hard-coded skill dictionaries.

---

# Scoring Model

CareerLens AI uses the following application-specific weighting:

| Category | Weight |
|---|---:|
| Skills | 50% |
| Experience | 25% |
| Education | 15% |
| ATS | 10% |

The overall score is calculated as:

```text
Overall Score =
(Skills × 0.50)
+ (Experience × 0.25)
+ (Education × 0.15)
+ (ATS × 0.10)
```

This methodology is designed for CareerLens AI to provide an explainable comparison.

It is not presented as the internal scoring formula used by every commercial Applicant Tracking System.

---

# PDF Reporting

CareerLens AI allows users to generate a PDF report for an analysis.

The backend generates reports using ReportLab.

Reports can contain:

- Overall score
- Component scores
- Matched skills
- Missing skills
- Recommended skills
- ATS information
- Experience analysis
- Education analysis
- Recommendations

---

# Database Architecture

CareerLens AI uses:

- MySQL 8
- SQLAlchemy ORM
- Alembic migrations

The current database contains five primary tables:

```text
users
resumes
job_descriptions
analyses
refresh_tokens
```

High-level relationships:

```text
users
 ├── resumes
 ├── job_descriptions
 ├── analyses
 └── refresh_tokens

resumes
 └── analyses

job_descriptions
 └── analyses
```

Analysis skill results are stored with the analysis record rather than using separate `skills` or `analysis_skills` tables.

---

# User Data Isolation

CareerLens AI implements ownership-based resource protection.

User-owned resources include:

- Resumes
- Job descriptions
- Analyses

The backend checks the authenticated user's identity before allowing access to these resources.

Conceptually:

```text
Authenticated User
       ↓
Requested Resource
       ↓
Ownership Check
       ↓
Authorized?
   ┌───┴────┐
   │        │
  Yes       No
   │        │
Access    Reject
```

This prevents one user from accessing another user's private application data.

---

# Error Handling

The backend provides centralized exception handling.

The frontend API layer handles scenarios including:

- Authentication failures
- Authorization failures
- Expired access tokens
- Token refresh
- Invalid requests
- Missing resources
- Request timeouts
- Backend failures
- Unexpected errors

---

# Docker Architecture

The local application can run using Docker Compose.

Four services are provisioned:

```text
frontend
backend
mysql
redis
```

High-level container flow:

```text
Browser
   │
   ▼
Frontend Container
   │
   ▼
Backend Container
   │
   ├──────────► MySQL
   │
   └──────────► Redis
```

Typical local endpoints:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
```

Docker volumes provide persistence where required by the local environment.

---

# Continuous Integration

GitHub Actions validates backend and frontend changes.

```text
                  Git Push
                     │
                     ▼
               GitHub Actions
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
       Backend               Frontend
          │                     │
          ▼                     ▼
Install Dependencies         npm ci
          │                     │
          ▼                     ▼
        pytest                ESLint
                                │
                                ▼
                         Production Build
```

---

# Testing

The backend currently contains:

```text
31 passing tests
```

The project has also passed:

- Backend pytest validation
- Frontend ESLint validation
- Next.js production build
- Docker integration smoke testing
- Manual end-to-end testing

---

# Design Principles

CareerLens AI demonstrates:

- Separation of concerns
- Modular architecture
- RESTful API design
- Authentication and authorization
- User data isolation
- Relational database modelling
- Document processing
- Explainable analysis
- Environment-based configuration
- Automated testing
- Containerization
- Continuous integration
- Production-oriented error handling

---

# Deployment Architecture

The application is currently fully runnable locally and through Docker Compose.

The intended public deployment architecture is:

```text
Internet
   │
   ▼
Frontend Hosting
   │
   │ HTTPS / REST
   ▼
Backend Hosting
   │
   ├──────────► Production MySQL
   │
   ├──────────► Persistent File Storage
   │
   └──────────► Redis when required
```

Production configuration will use environment variables and restricted CORS settings.

---

# Repository Strategy

The complete implementation remains in a private repository.

The public CareerLens AI showcase contains:

- Architecture documentation
- API information
- Database design
- Screenshots
- Selected portfolio-safe code samples
- Live application link after deployment

This allows the engineering approach to be demonstrated publicly without publishing the complete application implementation.