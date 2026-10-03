"""
CareerLens AI - Analysis Service Example

Simplified public example showing the weighted scoring approach used
by CareerLens AI.

The production analysis implementation remains private.
"""

from dataclasses import dataclass


@dataclass
class ScoreBreakdown:
    skills: float
    experience: float
    education: float
    ats: float


@dataclass
class AnalysisResult:
    overall_score: float
    scores: ScoreBreakdown


class AnalysisService:
    """
    Simplified example of CareerLens AI's explainable scoring model.

    Weights:
        Skills      50%
        Experience  25%
        Education   15%
        ATS          10%
    """

    SKILLS_WEIGHT = 0.50
    EXPERIENCE_WEIGHT = 0.25
    EDUCATION_WEIGHT = 0.15
    ATS_WEIGHT = 0.10

    @staticmethod
    def _normalize(score: float) -> float:
        """Keep component scores within the expected 0-100 range."""
        return max(0.0, min(100.0, score))

    def calculate_overall_score(
        self,
        skills_score: float,
        experience_score: float,
        education_score: float,
        ats_score: float,
    ) -> AnalysisResult:

        scores = ScoreBreakdown(
            skills=self._normalize(skills_score),
            experience=self._normalize(experience_score),
            education=self._normalize(education_score),
            ats=self._normalize(ats_score),
        )

        overall = (
            scores.skills * self.SKILLS_WEIGHT
            + scores.experience * self.EXPERIENCE_WEIGHT
            + scores.education * self.EDUCATION_WEIGHT
            + scores.ats * self.ATS_WEIGHT
        )

        return AnalysisResult(
            overall_score=round(overall, 2),
            scores=scores,
        )


if __name__ == "__main__":
    service = AnalysisService()

    result = service.calculate_overall_score(
        skills_score=80,
        experience_score=72,
        education_score=90,
        ats_score=75,
    )

    print(f"Overall score: {result.overall_score}")
    print(result.scores)