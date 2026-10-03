# CareerLens AI

## AI-Assisted Resume & Job Description Analysis Platform

CareerLens AI is a full-stack web application that allows users to upload resumes, save job descriptions, compare a resume against a job description, and receive an explainable compatibility report covering skills, experience, education, ATS keywords, and improvement recommendations.

The application was developed as a production-style portfolio project demonstrating full-stack engineering, REST API development, authentication and authorization, relational database design, document processing, automated testing, Docker, CI/CD, and explainable analysis.

> This repository is the **public portfolio showcase** for CareerLens AI.  
> The complete application source code and development history are maintained separately in a private repository.

---

# Features

## Authentication & Security

CareerLens AI includes a complete authentication lifecycle:

- User registration
- User login
- Email verification
- Resend email verification
- Forgot password
- Reset password
- JWT access tokens
- JWT refresh tokens
- Refresh-token rotation
- Refresh-token revocation
- Secure password hashing
- USER and ADMIN roles
- Protected API endpoints
- User-level data isolation

---

## Resume Management

Users can:

- Upload PDF resumes
- Upload DOCX resumes
- Automatically extract resume text
- View uploaded resumes
- Retrieve individual resume details
- Delete resumes

Resume document processing uses:

- PyMuPDF
- python-docx

---

## Job Description Management

Users can:

- Create job descriptions
- Store job titles
- Store company information
- Save complete job-description content
- View saved job descriptions
- Retrieve individual job descriptions
- Delete job descriptions

---

## Resume vs Job Analysis

Users select a resume and a job description and run an analysis.

CareerLens AI generates:

- Overall compatibility score
- Skills score
- Experience score
- Education score
- ATS score
- Matched skills
- Missing skills
- Recommended skills
- ATS keywords
- Experience-match explanation
- Education-match explanation
- Resume improvement recommendations

The analysis is designed to work from the content of each resume and job description rather than depending on profession-specific hard-coded skill lists.

---

## PDF Analysis Report

CareerLens AI can generate a downloadable PDF report for an analysis.

The report contains:

- Overall compatibility score
- Score breakdown
- Matched skills
- Missing skills
- Recommended skills
- ATS information
- Experience analysis
- Education analysis
- Improvement recommendations

PDF generation is implemented using ReportLab.

---

## Dashboard

The application includes a dashboard for viewing CareerLens activity and analysis history.

The dashboard provides information related to:

- Uploaded resumes
- Saved job descriptions
- Previous analyses
- Analysis scores
- Recent analysis activity

---

# Analysis Methodology

CareerLens AI uses an explainable weighted scoring model.

| Category | Weight |
|---|---:|
| Skills | 50% |
| Experience | 25% |
| Education | 15% |
| ATS | 10% |

The overall score is calculated using:

```text
Overall Score =
(Skills Score × 0.50)
+ (Experience Score × 0.25)
+ (Education Score × 0.15)
+ (ATS Score × 0.10)
```

This is an **application-specific CareerLens methodology** designed to provide an understandable resume-to-job comparison.

It is not presented as the internal scoring formula used by commercial Applicant Tracking Systems.

---

# Technology Stack

## Frontend

- Next.js 16
- React
- TypeScript
- Tailwind CSS

## Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

## Database

- MySQL 8

## Authentication

- JWT
- Access tokens
- Refresh tokens
- Password hashing
- Role-based authorization

## Document Processing

- PyMuPDF
- python-docx

## PDF Generation

- ReportLab

## Infrastructure

- Docker
- Docker Compose
- Redis
- Git
- GitHub
- GitHub Actions

## Testing & Quality

- pytest
- HTTPX
- ESLint
- Next.js production build validation

---

# System Architecture

CareerLens AI follows a modular full-stack architecture.

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

The backend follows a **modular monolith** architecture.

This provides separation between application responsibilities while avoiding unnecessary distributed-system complexity for the current application scale.

---

# Frontend Architecture

The frontend is built using Next.js, React, TypeScript, and Tailwind CSS.

Major application areas include:

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

The frontend communicates with the backend through REST APIs.

Authentication tokens are used when accessing protected endpoints.

---

# Backend Architecture

The FastAPI backend handles:

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

Responsibilities are separated into API, service, model, schema, and supporting application layers.

---

# Authentication Architecture

The authentication lifecycle follows this general flow:

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

- Password hashing
- JWT authentication
- Short-lived access tokens
- Refresh tokens
- Refresh-token rotation
- Refresh-token revocation
- Role validation
- User ownership validation

---

# Resume Processing Architecture

```text
Upload PDF / DOCX
       ↓
Validate File
       ↓
Store Resume
       ↓
Extract Text
       ↓
Store Resume Metadata
       ↓
Resume Available for Analysis
```

PDF extraction is handled using PyMuPDF.

DOCX extraction is handled using python-docx.

---

# Analysis Architecture

```text
Resume
   +
Job Description
   ↓
Text Processing
   ↓
Resume / Requirement Comparison
   ↓
Component Scores
   ↓
Overall Score
   ↓
Explainable Results
   ↓
Recommendations
```

The result includes numerical scores together with human-readable information so users can understand why improvements may be needed.

---

# Application Flow

```text
Create Account
      ↓
Verify Email
      ↓
Login
      ↓
Upload Resume
      ↓
Create Job Description
      ↓
Select Resume + Job Description
      ↓
Run Analysis
      ↓
View Score Breakdown
      ↓
Review Matched / Missing Skills
      ↓
Review Recommendations
      ↓
Download PDF Report
```

---

# Database Design

CareerLens AI uses:

- MySQL 8
- SQLAlchemy ORM
- Alembic migrations

The current application contains **five primary tables**:

```text
users
resumes
job_descriptions
analyses
refresh_tokens
```

---

## Database Relationships

```text
                       users
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
       resumes     job_descriptions   analyses
          │              │              ▲
          └──────────────┴──────────────┘

                       users
                         │
                         ▼
                  refresh_tokens
```

---

## Users

Table:

```text
users
```

Important fields:

```text
id
email
password_hash
role
is_active
is_email_verified
created_at
updated_at
```

Supported roles:

```text
USER
ADMIN
```

Email addresses are unique.

---

## Resumes

Table:

```text
resumes
```

Important fields:

```text
id
user_id
original_filename
stored_filename
file_type
file_size
file_path
extracted_text
created_at
updated_at
```

Relationship:

```text
users 1 ──────── * resumes
```

Each resume belongs to one user.

---

## Job Descriptions

Table:

```text
job_descriptions
```

Important fields:

```text
id
user_id
title
company_name
description
created_at
updated_at
```

Relationship:

```text
users 1 ──────── * job_descriptions
```

Each job description belongs to one user.

---

## Analyses

Table:

```text
analyses
```

Important fields:

```text
id
user_id
resume_id
job_description_id

match_score
skills_score
experience_score
education_score
ats_score

matched_skills
missing_skills
recommended_skills
ats_keywords

experience_match
education_match
recommendations

created_at
```

Relationships:

```text
users            1 ─── * analyses
resumes          1 ─── * analyses
job_descriptions 1 ─── * analyses
```

The analysis record contains both numerical scoring information and explainable analysis results.

---

## Refresh Tokens

Table:

```text
refresh_tokens
```

Important fields:

```text
id
user_id
token_hash
expires_at
revoked_at
created_at
```

Relationship:

```text
users 1 ──────── * refresh_tokens
```

Refresh tokens are persisted as token hashes rather than storing the original token value directly.

---

# Database Foreign Keys

Primary relationships include:

```text
resumes.user_id
    → users.id

job_descriptions.user_id
    → users.id

analyses.user_id
    → users.id

analyses.resume_id
    → resumes.id

analyses.job_description_id
    → job_descriptions.id

refresh_tokens.user_id
    → users.id
```

Cascade deletion is used for relevant ownership relationships.

---

# Database Indexing

Important indexed fields include:

```text
users.email

resumes.user_id

job_descriptions.user_id

analyses.user_id
analyses.resume_id
analyses.job_description_id

refresh_tokens.user_id
refresh_tokens.token_hash
```

---

# Skill Result Storage

The current database does **not** use separate `skills` or `analysis_skills` tables.

Results including:

```text
matched_skills
missing_skills
recommended_skills
ats_keywords
```

are stored with each analysis record.

This keeps the current persistence model straightforward while preserving historical analysis results.

---

# REST API

All main application APIs are versioned under:

```text
/api/v1
```

---

## Authentication API

```text
POST /api/v1/auth/register
POST /api/v1/auth/verify-email
POST /api/v1/auth/resend-verification
POST /api/v1/auth/forgot-password
POST /api/v1/auth/reset-password
POST /api/v1/auth/login
POST /api/v1/auth/refresh
POST /api/v1/auth/logout
GET  /api/v1/auth/me
```

---

## Resume API

```text
POST   /api/v1/resumes/upload
GET    /api/v1/resumes
GET    /api/v1/resumes/{resume_id}
DELETE /api/v1/resumes/{resume_id}
```

---

## Job Description API

```text
POST   /api/v1/job-descriptions
GET    /api/v1/job-descriptions
GET    /api/v1/job-descriptions/{job_description_id}
DELETE /api/v1/job-descriptions/{job_description_id}
```

---

## Analysis API

```text
POST   /api/v1/analyses
GET    /api/v1/analyses
GET    /api/v1/analyses/{analysis_id}
GET    /api/v1/analyses/{analysis_id}/report
DELETE /api/v1/analyses/{analysis_id}
```

---

## Administration API

Example protected administrative endpoint:

```text
GET /api/v1/admin/test
```

This endpoint requires the ADMIN role.

---

# API Authentication

Protected API calls use JWT authentication.

```text
Client
   ↓
Login
   ↓
Access Token
   ↓
Authorization: Bearer <token>
   ↓
Protected API
```

When an access token expires, the refresh-token flow can obtain a new authentication session.

---

# Authorization & User Isolation

CareerLens AI validates both authentication and ownership.

```text
Authentication
      ↓
Role Validation
      ↓
Ownership Validation
      ↓
Resource Access
```

Authenticated users can access only their own:

- Resumes
- Job descriptions
- Analyses

Administrative functionality additionally requires the ADMIN role.

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

CareerLens AI can run locally using Docker Compose.

The environment contains four services:

```text
frontend
backend
mysql
redis
```

Architecture:

```text
Browser
   │
   ▼
Frontend Container
   │
   ▼
Backend Container
   │
   ├────────► MySQL
   │
   └────────► Redis
```

Typical local URLs:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
```

---

# Testing

The backend currently has:

```text
31 passing tests
```

The project has also passed:

- Backend pytest suite
- Frontend ESLint validation
- Next.js production build
- Docker integration smoke testing
- Manual end-to-end functional testing

Important tested behavior includes:

- Registration
- Login
- Authentication
- Email verification
- Password reset
- Resume operations
- Job-description operations
- Analysis operations
- User isolation
- Authorization

---

# CI/CD

CareerLens AI uses GitHub Actions for automated validation.

The CI workflow validates both backend and frontend.

```text
                 Git Push
                    │
                    ▼
              GitHub Actions
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
       Backend             Frontend
          │                   │
          ▼                   ▼
Install Dependencies    npm ci
          │                   │
          ▼                   ▼
       pytest              ESLint
                              │
                              ▼
                       Production Build
```

---

# Security

Security practices demonstrated by the project include:

- Secure password hashing
- JWT authentication
- Access-token expiration
- Refresh-token management
- Refresh-token rotation
- Refresh-token revocation
- Token hashes stored in the database
- Role-based authorization
- Resource ownership checks
- Environment-based configuration
- Git-ignored environment files
- Request validation
- Controlled CORS configuration
- Protected administrative routes

Secrets and production credentials are not included in this public repository.

---

# Environment Configuration

Application configuration is managed through environment variables.

Examples include:

```text
APP_NAME
APP_VERSION
ENVIRONMENT
DEBUG

DATABASE_URL

JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS

REDIS_URL

MAX_RESUME_SIZE_MB
STORAGE_PATH

AI_PROVIDER

FRONTEND_URL
EMAIL_PROVIDER
```

Frontend configuration includes:

```text
NEXT_PUBLIC_API_URL
```

Actual credentials and secrets are intentionally excluded from this public showcase.

---

# Engineering Concepts Demonstrated

CareerLens AI demonstrates practical implementation of:

- Full-stack development
- React application development
- Next.js
- TypeScript
- FastAPI
- REST API design
- JWT authentication
- Authorization
- RBAC
- User data isolation
- SQLAlchemy ORM
- Relational database design
- Database migrations
- MySQL
- File uploads
- PDF parsing
- DOCX parsing
- PDF generation
- Error handling
- Modular application architecture
- Docker
- Docker Compose
- Automated testing
- CI/CD
- GitHub Actions
- Environment configuration
- Production-oriented application design

---

# Screenshots

Application screenshots will be added to:

```text
/screenshots
```

The public showcase will include important screens such as:

- Landing page
- Login
- Registration
- Dashboard
- Resume management
- Job-description management
- Analysis page
- Analysis results
- PDF report

---

# Selected Code Samples

Selected implementation examples may be published under:

```text
/code-samples
```

Only portfolio-safe examples will be included.

The complete production implementation remains in the private CareerLens AI repository.

---

# Repository Structure

```text
careerlens-ai-showcase/
│
├── README.md
│
├── screenshots/
│
└── code-samples/
```

This public repository intentionally focuses on demonstrating the system rather than duplicating the entire private source repository.

---

# Development Status

## Completed

- User registration
- Login
- JWT authentication
- Refresh-token lifecycle
- Email verification
- Resend verification
- Forgot password
- Reset password
- Role-based authorization
- Resume upload
- PDF parsing
- DOCX parsing
- Resume management
- Job-description management
- Resume/job analysis
- Explainable score breakdown
- Analysis history
- Dashboard analytics
- PDF analysis report
- User data isolation
- Production-style error handling
- Docker environment
- Backend automated testing
- Frontend lint validation
- Production frontend build
- GitHub Actions CI
- Technical documentation

---

# Deployment Status

The application is currently fully runnable locally and through Docker Compose.

Public deployment is the next project milestone.

Production deployment will require:

- Production frontend hosting
- Production backend hosting
- Production MySQL
- Production environment variables
- Production CORS configuration
- Persistent resume storage
- Production email integration
- HTTPS
- Production logging and monitoring

---

# Live Demo

**Coming soon.**

A public CareerLens AI deployment is being prepared.

The production URL will be added here after deployment.

---

# Repository Strategy

CareerLens AI uses two repositories.

## Private Application Repository

Contains:

- Complete frontend source
- Complete backend source
- Database migrations
- Docker configuration
- Automated tests
- CI configuration
- Complete technical documentation
- Development history

## Public Showcase Repository

Contains:

- Project overview
- Architecture
- Database design
- API overview
- Security approach
- Testing information
- Screenshots
- Selected portfolio-safe code samples
- Live demo link after deployment

This allows the project to be demonstrated publicly without publishing the complete implementation.

---

# Why I Built CareerLens AI

CareerLens AI was created to demonstrate the development of a realistic full-stack product rather than a basic CRUD application.

The project combines:

```text
Frontend Engineering
        +
Backend Engineering
        +
Authentication & Security
        +
Database Engineering
        +
Document Processing
        +
Analysis Logic
        +
Testing
        +
Docker
        +
CI/CD
        +
Production Preparation
```

It demonstrates how multiple software-engineering concerns can be integrated into one maintainable application.

---

# Future Improvements

Potential future enhancements include:

- Production deployment
- Production email provider
- Cloud object storage for resumes
- Additional dashboard analytics
- More advanced analysis explainability
- Enhanced analysis algorithms
- Improved observability
- Additional automated tests
- Performance optimization
- Expanded administration capabilities

---

# Author

**Anojaa Gnaneswaran**

Software Engineer / Senior Software Engineer

Technical focus:

```text
Java
Spring Boot
React
Python
FastAPI
Next.js
TypeScript
MySQL
Microservices
Kafka
Docker
AWS
CI/CD
```

---

# License

This repository is provided for **portfolio and demonstration purposes**.

The complete CareerLens AI implementation is maintained separately in a private repository.

No secrets, production credentials, or private configuration are included in this public showcase.