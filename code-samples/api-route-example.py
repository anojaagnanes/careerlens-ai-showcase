"""
CareerLens AI - FastAPI Route Pattern

Simplified public example demonstrating REST resource ownership.

This is not the complete production route implementation.
"""

from dataclasses import dataclass

from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(
    prefix="/api/v1/resumes",
    tags=["resumes"],
)


@dataclass
class CurrentUser:
    id: int
    email: str


@dataclass
class Resume:
    id: int
    user_id: int
    filename: str


def get_current_user() -> CurrentUser:
    """
    Placeholder dependency.

    The real CareerLens application resolves the authenticated user
    from the JWT authentication layer.
    """
    return CurrentUser(
        id=1,
        email="demo@example.com",
    )


def find_resume(resume_id: int) -> Resume | None:
    """
    Placeholder repository operation.

    Production persistence is implemented separately using SQLAlchemy.
    """
    example = Resume(
        id=1,
        user_id=1,
        filename="sample-resume.pdf",
    )

    return example if resume_id == example.id else None


@router.get("/{resume_id}")
def get_resume(
    resume_id: int,
    current_user: CurrentUser = Depends(get_current_user),
):
    resume = find_resume(resume_id)

    if resume is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    # Ownership validation prevents cross-user resource access.
    if resume.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    return {
        "id": resume.id,
        "filename": resume.filename,
    }