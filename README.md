# CareerLens AI

CareerLens AI is a production-deployed, AI-assisted resume and job-description analysis platform built as a professional full-stack portfolio project.

The platform allows users to securely upload resumes, manage job descriptions, analyze resume compatibility against job requirements, identify matched and missing skills, evaluate ATS alignment, receive improvement recommendations, maintain analysis history, and download professional PDF analysis reports.

## Live Demo

https://careerlens-ai-one.vercel.app/

---

## Key Features

### Authentication and Security

- Secure user registration and login
- Email verification
- Resend verification email
- Forgot password workflow
- Password reset workflow
- JWT access and refresh token authentication
- Refresh-token rotation
- Secure password hashing
- Role-based authorization
- User data isolation

### Resume Management

- Upload PDF and DOCX resumes
- File type and size validation
- Resume text extraction
- Persistent production resume storage using Vercel Blob
- Resume listing
- Resume deletion
- Automatic removal of deleted resume files from object storage

### Job Description Management

- Create job descriptions
- Store job requirements
- View saved job descriptions
- Delete job descriptions
- Use saved job descriptions for resume analysis

### Resume Analysis

CareerLens AI compares a selected resume against a selected job description and generates a structured compatibility report.

The analysis includes:

- Overall compatibility score
- Skills score
- Experience score
- Education score
- ATS score
- Matched skills
- Missing skills
- Recommended skills
- ATS keywords
- Experience alignment
- Education alignment
- Resume improvement recommendations

### Analysis History

- Save completed analyses
- View previous analysis results
- Reopen previous reports
- Delete analysis records
- Download analysis reports as PDF

### Dashboard

The dashboard provides an overview of application activity and analysis history.

### PDF Reports

Users can generate and download professional PDF reports containing their resume-job analysis results.

---

## Analysis Scoring

CareerLens AI evaluates resume-job compatibility using the following weighted model:

| Category | Weight |
| --- | ---: |
| Skills | 50% |
| Experience | 25% |
| Education | 15% |
| ATS Alignment | 10% |

The engine evaluates information extracted from the uploaded resume against requirements detected in the job description.

The analysis is designed to remain job-description-driven rather than relying on a fixed profession-specific skill list.

---

## Technology Stack

### Frontend

- Next.js
- React
- TypeScript
- Tailwind CSS

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- JWT authentication

### Database

**Development**
- MySQL 8

**Production**
- Neon PostgreSQL

### File Storage

**Development**
- Local filesystem storage

**Production**
- Vercel Blob

### Email Delivery

- Resend
- Email verification
- Password reset emails

### Testing

- Pytest
- Automated backend tests
- API integration testing

### DevOps and Development Tools

- Docker
- Docker Compose
- Git
- GitHub
- GitHub Actions
- Redis
- Postman

### Production Deployment

- Vercel
- Neon PostgreSQL
- Vercel Blob
- Resend

---

## Production Architecture

```text
                         CareerLens AI

                              User
                               |
                               v
                     Next.js / React Frontend
                               |
                               v
                         FastAPI REST API
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
      Neon PostgreSQL     Vercel Blob        Resend
              |                |                |
       Application Data    Resume Files       Emails
              |
              v
       Analysis Engine
              |
              v
       Analysis Results
              |
              v
         PDF Reports
```

---

## Resume Upload Flow

```text
User selects PDF/DOCX resume
          |
          v
Next.js Frontend
          |
          v
POST /api/v1/resumes/upload
          |
          v
FastAPI validates file
          |
          v
Temporary file created for text extraction
          |
          v
PDF/DOCX text extracted
          |
          +--------------------------+
          |                          |
          v                          v
    Vercel Blob                Neon PostgreSQL
Permanent resume file       Metadata + extracted text
```

The production application stores the original resume permanently in Vercel Blob.

Extracted resume text and resume metadata are stored in PostgreSQL so the analysis engine does not need to download and parse the original document every time an analysis is performed.

---

## Resume Analysis Flow

```text
User selects Resume
        +
User selects Job Description
          |
          v
Next.js Frontend
          |
          v
FastAPI Analysis API
          |
          v
Resume text + Job Description
          |
          v
CareerLens Analysis Engine
          |
          +-----------------------------+
          |             |               |
          v             v               v
       Skills       Experience       Education
          |
          v
     ATS Analysis
          |
          v
Weighted Compatibility Score
          |
          v
Matched / Missing / Recommended Skills
          |
          v
Recommendations
          |
          v
Analysis stored in Neon PostgreSQL
          |
          v
Result displayed to user
```

---

## Email Verification Flow

```text
User registers
      |
      v
Next.js Frontend
      |
      v
FastAPI Auth API
      |
      v
Password securely hashed
      |
      v
User stored in Neon PostgreSQL
      |
      v
Verification token generated
      |
      v
Resend Email API
      |
      v
Verification email
      |
      v
User clicks verification link
      |
      v
FastAPI validates token
      |
      v
Email marked as verified
      |
      v
User can log in
```

---

## Resume Deletion Flow

```text
User deletes resume
       |
       v
FastAPI Resume API
       |
       +------------------+
       |                  |
       v                  v
Vercel Blob Delete    Neon PostgreSQL
       |                  |
       v                  v
File removed          Record removed
```

---

## Database

CareerLens AI uses SQLAlchemy for ORM-based database access and Alembic for schema migrations.

Primary application tables:

1. `users`
2. `resumes`
3. `job_descriptions`
4. `analyses`
5. `refresh_tokens`

Alembic maintains the database migration version through the `alembic_version` table.

---

## API Overview

### Authentication

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/verify-email`
- `POST /api/v1/auth/resend-verification`
- `POST /api/v1/auth/forgot-password`
- `POST /api/v1/auth/reset-password`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `POST /api/v1/auth/logout`
- `GET /api/v1/auth/me`

### Resumes

- `POST /api/v1/resumes/upload`
- `GET /api/v1/resumes`
- `GET /api/v1/resumes/{resume_id}`
- `DELETE /api/v1/resumes/{resume_id}`

### Job Descriptions

- `POST /api/v1/job-descriptions`
- `GET /api/v1/job-descriptions`
- `GET /api/v1/job-descriptions/{job_description_id}`
- `DELETE /api/v1/job-descriptions/{job_description_id}`

### Analyses

- `POST /api/v1/analyses`
- `GET /api/v1/analyses`
- `GET /api/v1/analyses/{analysis_id}`
- `GET /api/v1/analyses/{analysis_id}/report`
- `DELETE /api/v1/analyses/{analysis_id}`

---

## Local Development Architecture

The project supports a Docker-based local development environment.

```text
Next.js Frontend
Port 3000
      |
      v
FastAPI Backend
Port 8000
      |
      +------> MySQL 8
      |
      +------> Redis
```

Docker Compose is used to coordinate the local application services.

---

## Production Environment

```text
Next.js + FastAPI
        |
      Vercel
        |
        +------> Neon PostgreSQL
        |
        +------> Vercel Blob
        |
        +------> Resend
```

Production secrets and credentials are managed through environment variables and are not committed to the source repository.

---

## Testing

The backend includes an automated Pytest test suite covering important application functionality.

Current backend test status:

```text
31 passed
```

Production functionality has also been manually verified end-to-end.

---

## Production Verification

The following production flows have been successfully tested:

- User registration
- Real email verification
- Login and logout
- Forgot password
- Password reset
- Resume PDF/DOCX upload
- Persistent Vercel Blob storage
- Resume text extraction
- Job description creation
- Resume-job analysis
- Score generation
- Analysis history
- PDF report generation
- Resume deletion
- Vercel Blob file deletion
- Production database persistence

---

## CI/CD

The project includes a GitHub Actions CI workflow for automated validation.

Production deployments are connected to the GitHub repository through Vercel.

---

## Repository Structure

This public repository is a portfolio showcase for CareerLens AI.

```text
careerlens-ai-showcase/
|
|-- code-samples/
|-- docs/
|-- screenshots/
|-- README.md
```

### code-samples

Contains selected implementation examples demonstrating the application's engineering approach.

### docs

Contains technical and architectural documentation.

### screenshots

Contains screenshots demonstrating application functionality and user interfaces.

---

## Full Source Code Access

The complete CareerLens AI source code is maintained in a separate private GitHub repository.

The private repository contains the complete implementation, including:

- Next.js / React frontend
- FastAPI backend
- Authentication and authorization
- JWT access and refresh token implementation
- Resume PDF/DOCX processing
- Vercel Blob integration
- Resume-job analysis engine
- SQLAlchemy database layer
- Alembic migrations
- Neon PostgreSQL production configuration
- Resend email integration
- PDF report generation
- Automated backend tests
- Docker configuration
- GitHub Actions CI workflow
- Vercel production deployment configuration
- Technical documentation

Private source access can be provided to recruiters, hiring managers, or interviewers for recruitment and technical review purposes.

---

## Project Purpose

CareerLens AI was developed as a full-stack engineering portfolio project demonstrating practical experience with:

- Full-stack application architecture
- REST API development
- Authentication and authorization
- Relational database design
- Database migrations
- Document processing
- Object storage
- Email integration
- Backend testing
- Dockerized development
- CI/CD concepts
- Cloud deployment
- Production debugging
- Error handling
- Application security
- Modern frontend development

---

## Live Application

CareerLens AI is available at:

https://careerlens-ai-one.vercel.app/

---

## Contact

**Anojaa Gnaneswaran**

**Email:** anojaa16@yahoo.com

**LinkedIn:**
https://www.linkedin.com/in/anojaa-gnaneswaran-664755149/
