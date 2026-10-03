# CareerLens AI — Database Design

## Overview

CareerLens AI uses a relational database architecture built with:

- MySQL 8
- SQLAlchemy ORM
- Alembic migrations

The current application contains exactly five primary tables:

```text
users
resumes
job_descriptions
analyses
refresh_tokens
```

Skill-analysis information is stored as part of an analysis record. The current implementation does not require separate `skills` or `analysis_skills` tables.

---

# Entity Relationship Overview

```text
                         users
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       resumes      job_descriptions     analyses
          │                │                ▲
          │                │                │
          └────────────────┴────────────────┘

                         users
                           │
                           ▼
                    refresh_tokens
```

Another representation:

```text
users
 ├──< resumes
 ├──< job_descriptions
 ├──< analyses
 └──< refresh_tokens

resumes
 └──< analyses

job_descriptions
 └──< analyses
```

---

# 1. Users

Table:

```text
users
```

The users table stores application account information.

## Fields

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `email` | Unique user email |
| `password_hash` | Secure password hash |
| `role` | USER or ADMIN |
| `is_active` | Account status |
| `is_email_verified` | Email-verification state |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

The `id` field is an auto-incrementing primary key.

The email field is:

- Required
- Unique
- Indexed

---

## User Roles

The application supports:

```text
USER
ADMIN
```

Role information supports role-based authorization.

---

# 2. Resumes

Table:

```text
resumes
```

The resumes table stores metadata and extracted content for uploaded resumes.

## Fields

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `user_id` | Resume owner |
| `original_filename` | Original uploaded filename |
| `stored_filename` | Internal stored filename |
| `file_type` | File type |
| `file_size` | File size |
| `file_path` | Stored file location |
| `extracted_text` | Extracted resume text |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

---

## Resume Ownership

```text
users 1 ─────────── * resumes
```

Each resume belongs to exactly one application user.

The relationship is implemented using:

```text
resumes.user_id → users.id
```

The foreign key uses cascading deletion for the relevant ownership relationship.

---

# 3. Job Descriptions

Table:

```text
job_descriptions
```

This table stores job descriptions created by users.

## Fields

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `user_id` | Owner |
| `title` | Job title |
| `company_name` | Optional company name |
| `description` | Full job-description text |
| `created_at` | Creation timestamp |
| `updated_at` | Last update timestamp |

---

## Job Description Ownership

```text
users 1 ─────────── * job_descriptions
```

Relationship:

```text
job_descriptions.user_id → users.id
```

Each job description belongs to one user.

---

# 4. Analyses

Table:

```text
analyses
```

The analyses table stores resume-to-job-description analysis results.

## Identification Fields

```text
id
user_id
resume_id
job_description_id
```

---

## Score Fields

```text
match_score
skills_score
experience_score
education_score
ats_score
```

`match_score` represents the overall compatibility score.

The other score fields preserve the component-level breakdown.

---

## Explainability Fields

```text
matched_skills
missing_skills
recommended_skills
ats_keywords
experience_match
education_match
recommendations
```

These fields preserve the generated explanation associated with the analysis.

---

## Timestamp

```text
created_at
```

Each analysis records its creation time.

---

## Analysis Relationships

```text
users 1 ─────────────── * analyses

resumes 1 ───────────── * analyses

job_descriptions 1 ──── * analyses
```

Foreign keys:

```text
analyses.user_id
    → users.id

analyses.resume_id
    → resumes.id

analyses.job_description_id
    → job_descriptions.id
```

---

# 5. Refresh Tokens

Table:

```text
refresh_tokens
```

The refresh-token table supports secure authentication lifecycle management.

## Fields

| Field | Purpose |
|---|---|
| `id` | Primary key |
| `user_id` | Token owner |
| `token_hash` | Hash of refresh token |
| `expires_at` | Token expiration |
| `revoked_at` | Revocation timestamp |
| `created_at` | Creation timestamp |

---

## Refresh Token Relationship

```text
users 1 ─────────── * refresh_tokens
```

Foreign key:

```text
refresh_tokens.user_id → users.id
```

---

# Refresh Token Security

The original refresh-token value is not stored directly.

Instead, CareerLens persists:

```text
token_hash
```

This reduces exposure of reusable authentication credentials if database information is compromised.

Tokens also support:

```text
Expiration
Revocation
Rotation
```

---

# Complete Relationship Model

```text
┌──────────────────┐
│      users       │
├──────────────────┤
│ id               │
│ email            │
│ password_hash    │
│ role             │
│ is_active        │
│ verified         │
└───────┬──────────┘
        │
        ├──────────────────────┐
        │                      │
        ▼                      ▼
┌──────────────────┐   ┌──────────────────────┐
│     resumes      │   │   job_descriptions   │
├──────────────────┤   ├──────────────────────┤
│ id               │   │ id                   │
│ user_id          │   │ user_id              │
│ filename         │   │ title                │
│ extracted_text   │   │ company_name         │
└────────┬─────────┘   │ description          │
         │             └──────────┬───────────┘
         │                        │
         └───────────┬────────────┘
                     │
                     ▼
             ┌──────────────────┐
             │     analyses     │
             ├──────────────────┤
             │ id               │
             │ user_id          │
             │ resume_id        │
             │ job_description  │
             │ match_score      │
             │ skills_score     │
             │ experience_score │
             │ education_score  │
             │ ats_score        │
             │ analysis results │
             └──────────────────┘

users
  │
  ▼
┌──────────────────┐
│  refresh_tokens  │
├──────────────────┤
│ id               │
│ user_id          │
│ token_hash       │
│ expires_at       │
│ revoked_at       │
│ created_at       │
└──────────────────┘
```

---

# Foreign Keys

The current database uses the following primary relationships:

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

---

# Cascade Deletion

Relevant ownership relationships use cascade deletion.

For example, deleting an owning user can remove dependent records according to the configured foreign-key relationships.

This helps prevent orphaned application records.

---

# Indexing

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

Indexes support efficient lookup for frequently accessed ownership and authentication relationships.

---

# Skill Storage Strategy

The current implementation intentionally does not use:

```text
skills
analysis_skills
```

as separate database tables.

Instead, generated analysis information is stored directly in the analysis record:

```text
matched_skills
missing_skills
recommended_skills
ats_keywords
```

This keeps the current data model relatively simple while preserving analysis history.

The schema can later be normalized further if the application requires skill-level analytics, search, reporting, or cross-analysis aggregation.

---

# Database Migrations

CareerLens uses Alembic to manage schema evolution.

Typical workflow:

```text
SQLAlchemy Model Change
          ↓
Alembic Migration
          ↓
Migration Review
          ↓
Apply Migration
          ↓
Updated Database Schema
```

This provides version-controlled database schema changes.

---

# User Data Isolation

Database ownership fields support application-level user isolation.

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

The backend verifies ownership before allowing access to user-specific resources.

Therefore, knowing another resource ID alone does not authorize access to that resource.

---

# Data Integrity

CareerLens uses:

- Primary keys
- Foreign keys
- Unique constraints
- Required fields
- Indexed ownership fields
- Cascade relationships
- ORM validation
- API validation

to maintain application data integrity.

---

# Security Considerations

Sensitive authentication data is handled carefully.

The database stores:

```text
password_hash
token_hash
```

rather than plaintext passwords or original refresh tokens.

Application secrets such as JWT signing secrets and database credentials are provided through environment configuration and are not stored in this public repository.

---

# Design Goals

The CareerLens database architecture focuses on:

- Clear ownership
- Referential integrity
- User isolation
- Authentication security
- Analysis history
- Relational modelling
- Migration support
- Maintainability
- Future extensibility

---

# Future Evolution

As CareerLens grows, possible database improvements include:

- Normalized skill entities
- Skill taxonomy
- Analysis audit information
- Additional analytics data
- File-storage metadata
- Application event history
- Reporting-oriented indexes

These are future architectural options rather than requirements of the current implementation.